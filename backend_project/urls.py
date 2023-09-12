#url.py
from django.urls import path
from django.views.generic import RedirectView
from backend_app.views import upload,image,user
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='upload_image'), name='default_redirect'),
    path('upload_image/', upload.upload_image, name='upload_image'),
    path('upload_first_image/', upload.upload_first_image, name='upload_first_image'),
    path('upload_second_image/', upload.upload_second_image, name='upload_second_image'),
    path('admin/', admin.site.urls),
    path('check_task_status_on_taskid/<str:task_id>/', upload.check_task_status_on_taskid, name='check_task_status_on_taskid'),
    path('check_task_status_on_userid/<str:user_id>/', upload.check_task_status_on_userid, name='check_task_status_on_userid'),
    path('get_completed_tasks_on_user/<str:user_id>/', upload.get_completed_tasks_on_user, name='get_completed_tasks_on_user'),
    path('get_pending_tasks_on_user/<str:user_id>/', upload.get_pending_tasks_on_user, name='get_pending_tasks_on_user'),
    path('getInitData/', user.get_init_data, name='get_init_data'),
    path('get_points_by_check', user.get_points_by_check, name='get_points_by_check'),
    path('get_user', user.get_user, name='get_user'),
    path('wechat_login', user.wechat_login, name='wechat_login'),
    path('image_list/', image.image_list, name='image_list'),
    path('tags/', image.tag_cloud, name='tag_cloud'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
