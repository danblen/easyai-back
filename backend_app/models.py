#models.py
from django.db import models

class UserImage(models.Model):
    user_id = models.CharField(max_length=100)
    src_face_index = models.IntegerField()
    dst_face_index = models.IntegerField()
    first_image = models.ImageField(upload_to='user_images/', blank=True, null=True, default=None)
    second_image = models.ImageField(upload_to='user_images/', blank=True, null=True, default=None)
    processed_image = models.ImageField(upload_to='processed_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id

    class Meta:
        app_label = 'backend_app'
