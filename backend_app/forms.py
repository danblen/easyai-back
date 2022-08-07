# backend_app/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UploadImageForm(forms.Form):
    user_id = forms.CharField(max_length=100)
    src_face_index = forms.IntegerField()
    dst_face_index = forms.IntegerField()
    first_image = forms.ImageField(label='First Image')
    second_image = forms.ImageField(label='Second Image')

    # 数据有效性判断,image/png,image/jpeg,image/gif等等
    def clean_first_image(self):
        image = self.cleaned_data.get('first_image')
        if not image.content_type.startswith('image'):
            raise ValidationError(_('File is not an image.'))
        return image

    def clean_second_image(self):
        image = self.cleaned_data.get('second_image')
        if not image.content_type.startswith('image'):
            raise ValidationError(_('File is not an image.'))
        return image
