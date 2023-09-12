from ..models import User
import traceback
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
import requests


@require_POST
def wechat_login(request):
    if request.method == 'POST':
        # 这样拿不到code
        # code = request.POST.get('code')
        request_data = request.body.decode('utf-8')
        data = json.loads(request_data)
        code = data.get('code')
        # 向微信服务器发送请求以获取访问令牌和用户信息 小程序 js_code  公众号 code
        wechat_params = {
            'appid': 'wx119cd856b94e2022',
            'secret': '1d680a99f50a791d44180dac063001d8',
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        wechat_response = requests.get(
            'https://api.weixin.qq.com/sns/jscode2session', params=wechat_params)
        wechat_data = wechat_response.json()

        # 在这里处理微信服务器返回的数据，包括访问令牌和用户信息
        session_key = wechat_data.get('session_key')
        openid = wechat_data.get('openid')
        # if not exist in database,  insert into database otherwise update database
        user = User.objects.filter(user_id=openid)
        if not user:
            user = User(user_id=openid,
                        points=5,
                        is_check=False,
                        )
            user.save()
            response_data = {
                'session_key': session_key,
                'user': {
                    'user_id': openid,
                    'points': 5,
                    'is_check': False,
                }
            }
        else:
            user = user[0]
            user.last_check_date = date.today()
            user.save()
            response_data = {
                'session_key': session_key,
                'user': {
                    'user_id': openid,
                    'points': user.points,
                    'is_check': user.is_check,
                }
            }

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'})


@require_POST
def get_points_by_check(request):
    today = date.today()
    request_data = request.body.decode('utf-8')
    data = json.loads(request_data)
    user_id = data.get('user_id')
    # user_id = request.user_id

    if user_id:
        user = User.objects.get(user_id=user_id)
        today = date.today()

        if user.last_check_date != today:
            # 用户可以签到，更新最后签到日期
            user.last_check_date = today
            user.is_check = True
            user.points += 1
            user.save()
            return JsonResponse({
                'user': {
                    'user_id': user_id,
                    'points': user.points,
                    'is_check': user.is_check,
                },
                'message': '签到成功'})
        else:
            return JsonResponse({'message': '今天已经签到过了'})
    else:
        return JsonResponse({'message': '用户未登录'})


def get_user(request):
    request_data = request.body.decode('utf-8')
    data = json.loads(request_data)
    user_id = data.get('user_id')
    # user_id = request.POST.user_id

    if user_id:
        user = User.objects.get(user_id=user_id)
        return JsonResponse({
            'user': {
                'user_id': user_id,
                'points': user.points,
                'is_check': user.is_check,
            },
            'message': 'SUCCESS'})
    else:
        return JsonResponse({'message': 'FAILURE'})
# @require_POST
# def getPointByCheck(request):
#     user_id = request.POST.get('user_id')
#     # request_data = request.body.decode('utf-8')
#     # data = json.loads(request_data)
#     # user_id = data.get('user_id')

#     if user_id is None:
#         return HttpResponseBadRequest('Invalid request. "user_id" parameter is missing.')
#     try:
#         user = User(user_id=user_id,
#                                  )

#         # 立即返回响应，告知前端任务已启动
#         response_data = {
#             'status': 'SUCCESS',
#             'user_id': user_id,
#             'urls': user_id,
#         }
#         if DEBUG:
#             return redirect('check_task_status', task_id=task.id)
#         else:
#             return JsonResponse(response_data)
#     except Exception as e:
#         error_message = f"upload_image: An error occurred while processing the image: {e}"
#         traceback.print_exc()
#         return JsonResponse({'status': 'FAILURE', 'error_message': error_message}, status=500)


@csrf_exempt
@require_POST
def get_init_data(request):
    # data = request.POST  # 获取 POST 请求中的数据
    # user_id = data.get('user_id')
    # print(f"user_id: {data}")
    # chinese need decode
    request_data = request.body.decode('utf-8')
    data = json.loads(request_data)
    user_id = data.get('user_id')

    # if user_id is None:
    #     return HttpResponseBadRequest('Invalid request. "user_id" parameter is missing.')
    try:
        user_image = UserImage(user_id=user_id,
                               )
        user_image.save()

        # 立即返回响应，告知前端任务已启动
        response_data = {
            'status': 'SUCCESS',
            'user_id': user_id,
            'urls': user_id,
        }
        if DEBUG:
            return redirect('check_task_status', task_id=task.id)
        else:
            return JsonResponse(response_data)
    except Exception as e:
        error_message = f"upload_image: An error occurred while processing the image: {e}"
        traceback.print_exc()
        return JsonResponse({'status': 'FAILURE', 'error_message': error_message}, status=500)
