from django.urls import path

from .views import CatDetailView, CatListCreateView

urlpatterns = [
    path("", CatListCreateView.as_view(), name="cat-list-create"),
    path("<int:pk>/", CatDetailView.as_view(), name="cat-detail"),
]
