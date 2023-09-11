from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()  # 添加一个自定义字段

    class Meta:
        model = Image
        fields = ['image_url']  # 只包含图像URL字段

    def get_image_url(self, obj):
        # 在这里返回图像的URL，假设图像字段名为 'image_field'
        if obj.image_field:
            return obj.image_field.url
        return None
