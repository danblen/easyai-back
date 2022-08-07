from django.test import TestCase
from django.urls import reverse
from backend_app.models import UserImage
from django.core.files.uploadedfile import SimpleUploadedFile

class UserImageTestCase(TestCase):

    def test_upload_image_and_process(self):
        # 模拟用户上传图像
        # with open('/home/ubuntu/src/media/user_images/微信图片_20230815011359_vBoSeXR.jpg', 'rb') as first_image, open('/home/ubuntu/src/media/user_images/微信图片_20230815011359_ve7hJut.jpg', 'rb') as second_image:
        #     response = self.client.post(reverse('upload_image'), {
        #         'user_id': 1,
        #         'first_image': first_image,
        #         'second_image': second_image
        #     })
        # 模拟用户上传图像
        # first_image = SimpleUploadedFile("/home/ubuntu/src/media/user_images/微信图片_20230815011359_vBoSeXR.jpg", b"file_content", content_type="image/jpeg")
        # second_image = SimpleUploadedFile("/home/ubuntu/src/media/user_images/微信图片_20230815011359_ve7hJut.jpg", b"file_content", content_type="image/jpeg")
        # 使用 SimpleUploadedFile 来模拟上传图像文件
        first_image_path = "/home/ubuntu/src/media/user_images/微信图片_20230815011359_vBoSeXR.jpg"
        second_image_path = "/home/ubuntu/src/media/user_images/微信图片_20230815011359_ve7hJut.jpg"

        # 读取第一个图像文件内容
        with open(first_image_path, 'rb') as first_image_file:
            first_image_content = first_image_file.read()

        # 读取第二个图像文件内容
        with open(second_image_path, 'rb') as second_image_file:
            second_image_content = second_image_file.read()

        # 创建 SimpleUploadedFile 对象并使用读取的内容
        first_image = SimpleUploadedFile(first_image_path, first_image_content, content_type="image/jpeg")
        second_image = SimpleUploadedFile(second_image_path, second_image_content, content_type="image/jpeg")

        response = self.client.post(reverse('upload_image'), {
            'user_id': "123",
            'first_image': first_image_content,
            'second_image': second_image_content
        })
        print(response)
        # 检查是否成功上传图像
        # self.assertEqual(response.status_code, 200)  # 302是重定向的状态码
        # self.assertEqual(UserImage.objects.count(), 1)

        # 获取上传的图像对象
        user_image = UserImage.objects.first()

        # 模拟触发任务
        from backend_app.tasks import process_and_save_image
        task_result = process_and_save_image.apply_async(args=[user_image.id])

        # 等待任务完成
        task_result.wait()

        # 检查任务是否成功
        self.assertTrue(task_result.successful())

        # 检查是否成功创建了处理后的图像
        user_image.refresh_from_db()
        self.assertIsNotNone(user_image.processed_image)

        # 可以继续编写其他检查逻辑，例如检查图像是否符合预期
