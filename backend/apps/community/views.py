from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import RoleBasedAccessPermission
from apps.cats.models import Cat
from apps.core.errors import APIError

from .models import Publication
from .serializers import (
    PublicationCatSerializer,
    PublicationReadSerializer,
    PublicationWriteSerializer,
)


def visible_publications_for(request):
    user = request.user if request.user.is_authenticated else None
    return Publication.objects.visible_for(user).select_related("user", "cat")


class PublicationListCreateView(ListCreateAPIView):
    """`GET/POST /api/publications/`: feed público paginado y publicación autenticada (P18).

    `GET` lo ve cualquiera (busca con `q=` sobre título, descripción y autor;
    `user=` filtra por autor). `POST` requiere sesión y publica un gato propio;
    um gato ya publicado responde 409.
    """

    rbac_public = True
    rbac_resource = "publication"
    permission_classes = [RoleBasedAccessPermission]
    serializer_class = PublicationReadSerializer

    def get_queryset(self):
        queryset = visible_publications_for(self.request)
        query = self.request.query_params.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(user__username__icontains=query)
            )
        username = self.request.query_params.get("user", "").strip()
        if username:
            queryset = queryset.filter(user__username__iexact=username)
        return queryset.order_by("-created_at")

    def create(self, request, *args, **kwargs):
        payload = PublicationWriteSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        cat = Cat.objects.filter(pk=payload.validated_data["cat_id"]).select_related("user").first()
        if cat is None:
            raise APIError("CAT_NOT_FOUND", "El gato solicitado no existe.", http_status=404)
        if cat.user_id != request.user.id:
            raise APIError("FORBIDDEN_CAT", "No puedes publicar el gato de otra persona.", http_status=403)
        try:
            publication = Publication.objects.create(
                user=request.user,
                cat=cat,
                title=payload.validated_data["title"],
                description=payload.validated_data.get("description", ""),
                visibility=payload.validated_data["visibility"],
            )
        except IntegrityError as exc:
            raise APIError(
                "PUBLICATION_ALREADY_EXISTS",
                "Este gato ya está publicado en el hub.",
                http_status=409,
            ) from exc
        return Response(PublicationReadSerializer(publication).data, status=status.HTTP_201_CREATED)


class PublicationDetailView(APIView):
    """`GET /api/publications/{id}/`: pública; las privadas solo las ve su autor o un admin."""

    rbac_public = True
    rbac_resource = "publication"

    def get(self, request, pk):
        publication = visible_publications_for(request).filter(pk=pk).first()
        if publication is None:
            raise APIError("PUBLICATION_NOT_FOUND", "La publicación solicitada no existe.", http_status=404)
        return Response(PublicationReadSerializer(publication).data)


class PublicProfileView(APIView):
    """`GET /api/profiles/{username}/`: tarjeta pública de un usuario con sus gatos y publicaciones.

    Sin sesión también es público. Los gatos y publicaciones se derivan de las
    publicaciones visibles para el solicitante (público para todos; lo privado
    solo lo ve su autor).
    """

    rbac_public = True

    def get(self, request, username):
        user = User.objects.filter(username__iexact=username).select_related("profile").first()
        if user is None:
            raise APIError("PROFILE_NOT_FOUND", "El perfil solicitado no existe.", http_status=404)

        requester = request.user if request.user.is_authenticated else None
        publications = list(
            Publication.objects.visible_for(requester)
            .filter(user=user)
            .select_related("user", "cat")
            .order_by("-created_at")[:24]
        )
        return Response(
            {
                "username": user.username,
                "joined_at": user.date_joined.date().isoformat(),
                "publication_count": Publication.objects.filter(
                    user=user, visibility=Publication.Visibility.PUBLIC
                ).count(),
                "cats": PublicationCatSerializer([pub.cat for pub in publications], many=True).data,
                "publications": PublicationReadSerializer(publications, many=True).data,
            }
        )
