from django.shortcuts import render
from django.http.response import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET,require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from webpush import send_user_notification


@require_GET
def home(request):
   webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
   vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
   user = request.user
   print(webpush_settings)
   print(vapid_key)
   print(user)
   return render(request, 'home.html', {user: user, 'vapid_key': vapid_key})


@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'id' not in data:
            return JsonResponse(status=400, data ={ "message": "Invalid data format"})
        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {"head": "My heard", "body": "This is my test"}
        send_user_notification(user=user, payload=payload, ttl=1000)
        return JsonResponse(status=200, data={ "message": "sucessfully pushed"})
    except TypeError:
        return JsonResponse(status=500, data= {"message": "failed"})
