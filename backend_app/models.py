# models.py
from django.db import models


class UserImage(models.Model):
    user_id = models.CharField(max_length=100)
    task_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    src_face_index = models.IntegerField()
    dst_face_index = models.IntegerField()
    first_image = models.ImageField(
        upload_to="user_images/", blank=True, null=True, default=None
    )
    second_image = models.ImageField(
        upload_to="user_images/", blank=True, null=True, default=None
    )
    processed_image = models.ImageField(
        upload_to="processed_images/", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id

    class Meta:
        app_label = "backend_app"


class User(models.Model):
    user_id = models.CharField(max_length=100)
    points = models.IntegerField()
    is_check = models.BooleanField(default=False)
    last_check_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id

    class Meta:
        app_label = "backend_app"


class Image(models.Model):
    image = models.ImageField(
        upload_to="user_images/", blank=True, null=True, default=None
    )
    tag = models.CharField(max_length=100)
    status = models.CharField(max_length=255, null=True, blank=True)
    index = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.tag

    def get_image_url(self):
        # 检查图像字段是否为空
        if self.image:
            return self.image.url
        return None

    class Meta:
        app_label = "backend_app"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class InitData(models.Model):
    # 存储图片的URL路径
    image_urls = models.TextField(blank=True)

    def set_image_urls(self, urls):
        # 将多个值以逗号分隔存储为字符串
        self.image_urls = ",".join(urls)

    def get_image_urls(self):
        # 从存储的字符串中拆分多个值
        return self.image_urls.split(",")

    # 存储应用版本号
    app_version = models.CharField(max_length=20, blank=True)

    # 存储应用名称
    app_name = models.CharField(max_length=100, blank=True)

    # 存储应用描述
    app_description = models.TextField(blank=True)

    # 存储其他配置信息，可以使用 JSONField 存储复杂的配置数据
    other_config = models.JSONField(blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.app_name  # 返回应用名称作为字符串表示

    class Meta:
        app_label = "backend_app"
