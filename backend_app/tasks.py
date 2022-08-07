# backend_app/tasks.py
from celery import shared_task
from .models import UserImage
from .image_utils import process_image
from django.core.files.base import ContentFile
import cv2

from django.core.files.storage import default_storage

@shared_task(retry_kwargs={'max_retries': 0})
def process_and_save_image(user_image_id):
    print("任务_1已运行！")
    try:
        user_image_model = UserImage.objects.get(id=user_image_id)

        print("user_image_model", user_image_model)
        user_image = UserImage.objects.get(id=user_image_id)
        input_face_index = user_image.src_face_index
        output_face_index = user_image.dst_face_index
        print("user_image ", user_image, input_face_index, output_face_index)
        fir_image_path = user_image.first_image.path
        sec_image_path = user_image.second_image.path
        first_image_absolute_path = default_storage.path(fir_image_path)
        second_image_absolute_path = default_storage.path(sec_image_path)
        print('***********first_image_absolute_path:', first_image_absolute_path)
        print('***********second_image_absolute_path:', second_image_absolute_path)

        processed_image = process_image(first_image_absolute_path, second_image_absolute_path, input_face_index, output_face_index)
        if processed_image is None:
            print("process image failed")
            return None

        # 将 OpenCV 图像数据保存到数据库中
        _, img_encoded = cv2.imencode('.jpg', processed_image)
        processed_image_content = ContentFile(img_encoded.tostring())
        processed_image_name = user_image_model.first_image.name.split('.')[0] + '_processed.' + user_image_model.first_image.name.split('.')[-1]
        user_image_model.processed_image.save(processed_image_name, processed_image_content, save=True)
        print("Processed image saved successfully.")

        return user_image_model.id

    except Exception as e:
        print(f"process_and_save_image:An error occurred while processing the image: {e}")
        return None

# process_image_complete 视图函数:该函数无效！！
# def process_image_complete(request, user_image_id):
#     user_image = UserImage.objects.get(id=user_image_id)
#     # 在这里处理任务完成后的操作，例如更新数据库或发送通知等
#     print(f"Image processing completed for UserImage {user_image_id}")
#     context = {
#         'uploaded_image_url': user_image.image.url,
#         'processed_image_url': user_image.processed_image.url  # 添加这一行
#     }
#     print("render image_display")
#     return render(request, 'image_display.html', context)

# process_image_callback 任务函数
@shared_task
def process_image_callback(result, *args, **kwargs):
    print("任务_3已运行！")
    # if result:
    #     user_image_id = result
    #     return process_image_complete(None, user_image_id)  # 返回视图函数的结果
