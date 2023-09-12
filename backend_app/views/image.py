from django.shortcuts import render
from ..forms import UploadImageForm,FirstImageForm,SecondImageForm
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

@require_GET
def image_list(request):
    tag = request.GET.get('tag', None)
    tag =  unquote(tag)
    order_by = request.GET.get('order_by', None)
    search = request.GET.get('search', None)

    images = Image.objects.all()
    if tag:
        images = images.filter(tag=tag)

    if order_by == 'time':
        images = images.order_by('-time')
    elif order_by == 'views':
        images = images.order_by('-views')

    if search:
        images = images.filter(title__icontains=search)
    
    image_urls = []
    
    for image in images:
        if image.image:
            image_urls.append(image.image.url)
    return JsonResponse({'image_urls':image_urls})

    
@require_GET
def tag_cloud(request):
    """
    Retrieve a list of tags with usage counts.
    """
    tags = Tag.objects.annotate(num_images=Count('image'))
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)