from django.urls import path

from .views import PublicationDetailView, PublicationListCreateView

urlpatterns = [
    path("", PublicationListCreateView.as_view(), name="publication-list-create"),
    path("<int:pk>/", PublicationDetailView.as_view(), name="publication-detail"),
]
