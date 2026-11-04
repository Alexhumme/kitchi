from rest_framework import serializers

from .models import CatalogOption, Pose


class CatalogOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogOption
        fields = ["category", "code", "label", "asset_path", "z_order", "is_premium"]


class PoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pose
        fields = ["code", "name", "asset_path"]
