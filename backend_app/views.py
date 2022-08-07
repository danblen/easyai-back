# backend_app/views.py
from django.shortcuts import render
from .forms import UploadImageForm
from .models import UserImage
from .tasks import process_and_save_image
import traceback
from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import redirect

DEBUG = False

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            print("start upload_image...")
            user_id = form.cleaned_data['user_id']
            input_face_index = form.cleaned_data['src_face_index']
            output_face_index = form.cleaned_data['dst_face_index']
            first_image = form.clean_first_image()
            second_image = form.clean_second_image()

            print(f"user_id: {user_id}")
            print(f"input_face_index: {input_face_index}")
            print(f"output_face_index: {output_face_index}")
            print(f"first_image: {first_image}")
            print(f"second_image: {second_image}")

            # first_image_size = len(first_image.read())
            # second_image_size = len(second_image.read())
            # print(f"First Image Size: {first_image_size} bytes")
            # print(f"Second Image Size: {second_image_size} bytes")
            try:
                user_image = UserImage(user_id=user_id,
                                       src_face_index=input_face_index,
                                       dst_face_index=output_face_index,
                                       first_image=first_image,
                                       second_image=second_image)
                user_image.save()
                print("start process_and_save_image...")

                # 将图像处理任务添加到Celery队列中，不等待任务完成
                task = process_and_save_image.apply_async(args=[user_image.id])

                # 立即返回响应，告知前端任务已启动
                response_data = {
                    'status': 'PENDING',
                    'task_id': task.id,
                }
                if DEBUG:
                    return redirect('check_task_status', task_id=task.id)
                else:
                    return JsonResponse(response_data)
            except Exception as e:
                error_message = f"upload_image: An error occurred while processing the image: {e}"
                traceback.print_exc()
                return JsonResponse({'status': 'FAILURE', 'error_message': error_message}, status=500)
        else:
            print(form.errors)
            return JsonResponse({'status': 'FAILURE', 'error_message': form.errors}, status=400)
    else:
        form = UploadImageForm()
        return render(request, 'upload_image.html', {'form': form})

def check_task_status(request, task_id):
    task = AsyncResult(task_id)
    if task.ready():
        if task.successful():
            result = task.result  # 获取任务结果
            if result is not None:
                user_image = UserImage.objects.get(id=result)
                if DEBUG:
                    context = {
                        'uploaded_image_url': user_image.second_image.url,
                        'processed_image_url': user_image.processed_image.url  # 添加这一行
                    }
                    return render(request, 'image_display.html', context)
                else:
                    response_data = {
                        'status': 'SUCCESS',
                        'uploaded_image_url': user_image.second_image.url,
                        'processed_image_url': user_image.processed_image.url
                    }
                    return JsonResponse(response_data)
            else:
                error_message = "Image processing failed."
                return JsonResponse({'status': 'FAILURE', 'error_message': error_message}, status=500)
        else:
            error_message = "Image processing failed."
            return JsonResponse({'status': 'FAILURE', 'error_message': error_message}, status=500)
    else:
        return JsonResponse({'status': 'PENDING'})  # 任务仍在进行中

