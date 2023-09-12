# backend_app/views/upload.py
from django.shortcuts import render
from ..forms import UploadImageForm, FirstImageForm, SecondImageForm
from ..models import UserImage, Image, Tag
from ..tasks import process_and_save_image
import traceback
from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from urllib.parse import unquote

DEBUG = False


# 原方案
def upload_image(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            print("start upload_image...")
            user_id = form.cleaned_data["user_id"]
            input_face_index = form.cleaned_data["src_face_index"]
            output_face_index = form.cleaned_data["dst_face_index"]
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
                user_image = UserImage(
                    user_id=user_id,
                    src_face_index=input_face_index,
                    dst_face_index=output_face_index,
                    first_image=first_image,
                    second_image=second_image,
                )
                user_image.save()

                # 将图像处理任务添加到Celery队列中，不等待任务完成
                task = process_and_save_image.apply_async(args=[user_image.id])
                user_image.task_id = task.id
                user_image.status = "PENDING"
                user_image.save()
                print("start process_and_save_image...")

                # 立即返回响应，告知前端任务已启动
                response_data = {
                    "status": "PENDING",
                    "task_id": task.id,
                    "user_id": user_id,
                }
                if DEBUG:
                    return redirect("check_task_status", task_id=task.id)
                else:
                    return JsonResponse(response_data)
            except Exception as e:
                error_message = (
                    f"upload_image: An error occurred while processing the image: {e}"
                )
                traceback.print_exc()
                return JsonResponse(
                    {"status": "FAILURE", "error_message": error_message}, status=500
                )
        else:
            print(form.errors)
            return JsonResponse(
                {"status": "FAILURE", "error_message": form.errors}, status=400
            )
    else:
        form = UploadImageForm()
        return render(request, "upload_image.html", {"form": form})


def upload_first_image(request):
    if request.method == "POST":
        form = FirstImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = form.cleaned_data["user_id"]
            input_face_index = form.cleaned_data["src_face_index"]
            output_face_index = form.cleaned_data["dst_face_index"]
            first_image = form.clean_first_image()
            try:
                user_image = UserImage(
                    user_id=user_id,
                    src_face_index=input_face_index,
                    dst_face_index=output_face_index,
                    first_image=first_image,
                )
                user_image.save()
                saved_id = user_image.id

                # 立即返回响应，告知前端任务已启动
                response_data = {
                    "user_id": user_id,
                    "saved_id": saved_id,
                }
                if DEBUG:
                    return redirect("check_task_status", user_id=user_id)
                else:
                    return JsonResponse(response_data)
            except Exception as e:
                error_message = (
                    f"upload_image: An error occurred while processing the image: {e}"
                )
                traceback.print_exc()
                return JsonResponse(
                    {"status": "FAILURE", "error_message": error_message}, status=500
                )
        else:
            print(form.errors)
            return JsonResponse(
                {"status": "FAILURE", "error_message": form.errors}, status=400
            )
    else:
        form = FirstImageForm()
        return render(request, "upload_image.html", {"form": form})


def upload_second_image(request):
    if request.method == "POST":
        form = SecondImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = form.cleaned_data["user_id"]
            saved_id = form.cleaned_data["saved_id"]
            second_image = form.clean_second_image()
            try:
                updated_user_image = UserImage.objects.get(id=saved_id)
                # 进行数据更新
                updated_user_image.second_image = second_image
                # 将图像处理任务添加到Celery队列中，不等待任务完成
                updated_user_image.status = "PENDING"
                task = process_and_save_image.apply_async(args=[updated_user_image.id])
                print("start process_and_save_image...")
                updated_user_image.task_id = task.id
                updated_user_image.save()

                # 立即返回响应，告知前端任务已启动
                response_data = {
                    "status": "PENDING",
                    "task_id": task.id,
                    "user_id": user_id,
                }
                if DEBUG:
                    return redirect("check_task_status", task_id=task.id)
                else:
                    return JsonResponse(response_data)
            except Exception as e:
                error_message = (
                    f"upload_image: An error occurred while processing the image: {e}"
                )
                traceback.print_exc()
                return JsonResponse(
                    {"status": "FAILURE", "error_message": error_message}, status=500
                )
        else:
            print(form.errors)
            return JsonResponse(
                {"status": "FAILURE", "error_message": form.errors}, status=400
            )
    else:
        form = SecondImageForm()
        return render(request, "upload_image.html", {"form": form})


# base64方案
# def upload_image(request):
#     if request.method == 'POST':
#         form = UploadImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             print("start upload_image...")
#             user_id = form.cleaned_data['user_id']
#             input_face_index = form.cleaned_data['src_face_index']
#             output_face_index = form.cleaned_data['dst_face_index']
#             print(f"user_id: {user_id}")
#             print(f"input_face_index: {input_face_index}")
#             print(f"output_face_index: {output_face_index}")
#             first_image = form.clean_first_image_base64()
#             second_image = form.clean_second_image_base64()
#             # first_image_data = form.cleaned_data['first_image_base64']
#             # second_image_data = form.cleaned_data['second_image_base64']

#             print(f"first_image: {first_image}")
#             print(f"second_image: {second_image}")

#             first_image_size = len(first_image.read())
#             second_image_size = len(second_image.read())
#             print(f"First Image Size: {first_image_size} bytes")
#             print(f"Second Image Size: {second_image_size} bytes")
#             try:
#                 user_image = UserImage(user_id=user_id,
#                                        src_face_index=input_face_index,
#                                        dst_face_index=output_face_index,
#                                        first_image=first_image,
#                                        second_image=second_image)
#                 user_image.save()

#                 # 将图像处理任务添加到Celery队列中，不等待任务完成
#                 task = process_and_save_image.apply_async(args=[user_image.id])
#                 user_image.task_id = task.id
#                 user_image.status = 'PENDING'
#                 user_image.save()
#                 print("start process_and_save_image...")

#                 # 立即返回响应，告知前端任务已启动
#                 response_data = {
#                     'status': 'PENDING',
#                     'task_id': task.id,
#                     'user_id': user_id,
#                 }
#                 if DEBUG:
#                     return redirect('check_task_status', task_id=task.id)
#                 else:
#                     return JsonResponse(response_data)
#             except Exception as e:
#                 error_message = f"upload_image: An error occurred while processing the image: {e}"
#                 traceback.print_exc()
#                 return JsonResponse({'status': 'FAILURE', 'error_message': error_message}, status=500)
#         else:
#             print(form.errors)
#             return JsonResponse({'status': 'FAILURE', 'error_message': form.errors}, status=400)
#     else:
#         form = UploadImageForm()
#         return render(request, 'upload_image.html', {'form': form})


def get_completed_tasks_on_user(request, user_id):
    try:
        # 查询当前用户的所有已完成的任务
        completed_task = UserImage.objects.filter(user_id=user_id, status="SUCCESS")

        print("start completed_task...", completed_task)
        # 构造响应数据，包括已完成任务的信息
        task_list = []
        for task in completed_task:
            task_info = {
                "user_id": task.user_id,
                "task_id": task.task_id,
                "status": task.status,
                "uploaded_image_url": task.second_image.url,
                "processed_image_url": task.processed_image.url,
            }
            task_list.append(task_info)

        response_data = {
            "status": "GET_SUCCESS",
            "completed_tasks": task_list,
        }

        return JsonResponse(response_data)
    except UserImage.DoesNotExist:
        # 如果找不到已完成的任务，返回相应的状态信息
        return JsonResponse({"status": "NO_COMPLETED_TASKS", "completed_tasks": []})


def get_pending_tasks_on_user(request, user_id):
    try:
        # 查询当前用户的所有未完成的任务
        pending_tasks = UserImage.objects.filter(user_id=user_id, status="PENDING")

        print("start pending_tasks...", pending_tasks)
        # 构造响应数据，包括未完成任务的信息
        task_list = []
        for task in pending_tasks:
            task_info = {
                "user_id": task.user_id,
                "task_id": task.task_id,
                "status": task.status,
                "uploaded_image_url": task.second_image.url,
                "processed_image_url": task.processed_image.url,
            }
            task_list.append(task_info)

        response_data = {
            "status": "GET_SUCCESS",
            "pending_tasks": task_list,
        }

        return JsonResponse(response_data)
    except UserImage.DoesNotExist:
        # 如果找不到未完成的任务，返回相应的状态信息
        return JsonResponse({"status": "NO_PENDING_TASKS", "pending_tasks": []})


def check_task_status_on_userid(request, user_id):
    try:
        # 查询该用户的最新完成任务
        pending_tasks = UserImage.objects.filter(user_id=user_id, status="PENDING")
        print("start check_task_status_on_userid user_image...", pending_tasks)
        task_list = []
        for task in pending_tasks:
            # 获取任务的 task_id
            task_id = task.task_id

            # 创建 AsyncResult 对象来获取任务状态
            task_status = AsyncResult(task_id)

            if task_status.ready():  # 如果任务已完成
                # 获取处理后的图像 URL
                second_image_url = task.second_image.url
                processed_image_url = task.processed_image.url
                task_status = "SUCCESS"
            else:
                # 如果任务还在进行中
                task_status = "PENDING"
                second_image_url = None
                processed_image_url = None

            task_info = {
                "user_id": task.user_id,
                "task_id": task.task_id,
                "status": task_status,
                "uploaded_image_url": second_image_url,
                "processed_image_url": processed_image_url,
            }
            task.status = task_status
            task.processed_image = processed_image_url
            task.save()
            print("user{task} task.status", task.status)
            task_list.append(task_info)

        response_data = {
            "status": "GET_SUCCESS",
            "tasks": task_list,
        }
        return JsonResponse(response_data)
    except UserImage.DoesNotExist:
        # 如果找不到该用户的任务，返回相应的状态信息
        response_data = {
            "status": "NO_TASK",  # 可以定义一个特殊的状态表示没有任务
            "user_id": user_id,
            "uploaded_image_url": None,
            "processed_image_url": None,
        }
        return JsonResponse(response_data)


def check_task_status_on_taskid(request, task_id):
    task = AsyncResult(task_id)
    if task.ready():
        if task.successful():
            result = task.result  # 获取任务结果
            if result is not None:
                user_image = UserImage.objects.get(id=result)
                if DEBUG:
                    context = {
                        "uploaded_image_url": user_image.second_image.url,
                        "processed_image_url": user_image.processed_image.url,  # 添加这一行
                    }
                    return render(request, "image_display.html", context)
                else:
                    response_data = {
                        "status": "SUCCESS",
                        "uploaded_image_url": user_image.second_image.url,
                        "processed_image_url": user_image.processed_image.url,
                    }
                    return JsonResponse(response_data)
            else:
                error_message = "Image processing failed."
                return JsonResponse(
                    {"status": "FAILURE", "error_message": error_message}, status=500
                )
        else:
            error_message = "Image processing failed."
            return JsonResponse(
                {"status": "FAILURE", "error_message": error_message}, status=500
            )
    else:
        return JsonResponse({"status": "PENDING"})  # 任务仍在进行中
