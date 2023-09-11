#url.py
from django.urls import path
from django.views.generic import RedirectView
from backend_app import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='upload_image'), name='default_redirect'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('upload_first_image/', views.upload_first_image, name='upload_first_image'),
    path('upload_second_image/', views.upload_second_image, name='upload_second_image'),
    path('admin/', admin.site.urls),
    path('check_task_status_on_taskid/<str:task_id>/', views.check_task_status_on_taskid, name='check_task_status_on_taskid'),
    path('check_task_status_on_userid/<str:user_id>/', views.check_task_status_on_userid, name='check_task_status_on_userid'),
    path('get_completed_tasks_on_user/<str:user_id>/', views.get_completed_tasks_on_user, name='get_completed_tasks_on_user'),
    path('get_pending_tasks_on_user/<str:user_id>/', views.get_pending_tasks_on_user, name='get_pending_tasks_on_user'),
    path('getInitData/', views.getInitData, name='getInitData'),
    path('image_list/', views.image_list, name='image_list'),
    # path('tags/', views.tag_cloud, name='tag-cloud'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
