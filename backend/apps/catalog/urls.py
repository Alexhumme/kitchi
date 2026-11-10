from django.urls import path

from .views import CatalogListView, PoseListView

urlpatterns = [
    path("catalog/", CatalogListView.as_view(), name="catalog"),
    path("poses/", PoseListView.as_view(), name="poses"),
]
