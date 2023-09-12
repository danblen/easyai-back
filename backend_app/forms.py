# backend_app/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import base64


class UploadImageForm(forms.Form):
    user_id = forms.CharField(max_length=100)
    src_face_index = forms.IntegerField()
    dst_face_index = forms.IntegerField()
    first_image = forms.ImageField(label="First Image")
    second_image = forms.ImageField(label="Second Image")

    # 数据有效性判断,image/png,image/jpeg,image/gif等等
    def clean_first_image(self):
        image = self.cleaned_data.get("first_image")
        if not image.content_type.startswith("image"):
            raise ValidationError(_("File is not an image."))
        return image

    def clean_second_image(self):
        image = self.cleaned_data.get("second_image")
        if not image.content_type.startswith("image"):
            raise ValidationError(_("File is not an image."))
        return image


class FirstImageForm(forms.Form):
    user_id = forms.CharField(max_length=100)
    src_face_index = forms.IntegerField()
    dst_face_index = forms.IntegerField()
    first_image = forms.ImageField(label="First Image")

    # 数据有效性判断,image/png,image/jpeg,image/gif等等
    def clean_first_image(self):
        image = self.cleaned_data.get("first_image")
        if not image.content_type.startswith("image"):
            raise ValidationError(_("File is not an image."))
        return image


class SecondImageForm(forms.Form):
    user_id = forms.CharField(max_length=100)
    saved_id = forms.CharField(max_length=100)
    second_image = forms.ImageField(label="Second Image")

    # 数据有效性判断,image/png,image/jpeg,image/gif等等

    def clean_second_image(self):
        image = self.cleaned_data.get("second_image")
        if not image.content_type.startswith("image"):
            raise ValidationError(_("File is not an image."))
        return image


# class UploadImageForm(forms.Form):
#     user_id = forms.CharField(max_length=100)
#     src_face_index = forms.IntegerField()
#     dst_face_index = forms.IntegerField()
#     first_image_base64 = forms.CharField()  # 用于接收Base64数据
#     second_image_base64 = forms.CharField()  # 用于接收Base64数据

#     def clean_first_image_base64(self):
#         base64_data = self.cleaned_data.get('first_image_base64')
#         print(f"base64_data: {base64_data[:50]}")  # 打印前50个字符
#         try:
#             # 解码Base64数据并返回原始二进制数据
#             decoded_data = base64.b64decode(base64_data)
#             print(f"base64_data: {base64_data[:50]}")  # 打印前50个字符
#             print(f"decoded_data: {decoded_data[:50]}")
#             return decoded_data
#         except Exception as e:
#             raise ValidationError(_('Invalid Base64 data.'))

#     def clean_second_image_base64(self):
#         base64_data = self.cleaned_data.get('second_image_base64')
#         try:
#             # 解码Base64数据并返回原始二进制数据
#             decoded_data = base64.b64decode(base64_data)
#             return decoded_data
#         except Exception as e:
#             raise ValidationError(_('Invalid Base64 data.'))
