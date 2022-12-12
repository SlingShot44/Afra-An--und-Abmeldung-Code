from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Tour
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from zoneinfo import ZoneInfo
from BackendSchluesselKasten.settings import TIME_ZONE, LANGUAGE_CODE
from .json_tools import house_list
from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=Tour)
def ready(sender, instance, *args, **kwargs):
    channel_layer = get_channel_layer()
    data = {
        "type": "DB_Tour_U",
        "id": instance.id,
        "name": instance.owner.get_full_name(),
        "house": instance.owner.house,
        "target": house_list()[int(instance.target)],
        "start": instance.start.astimezone(ZoneInfo(TIME_ZONE)).isoformat(),
        "end": instance.end.astimezone(ZoneInfo(TIME_ZONE)).isoformat(),
        "back": instance.back,
        "lang_code": LANGUAGE_CODE
    }
    async_to_sync(channel_layer.group_send)(
        "WS", {"type": "WS.Send", "data": data})


@receiver(pre_save, sender=Tour)
def changeState(sender, instance, *args, **kwargs):
    if instance.back:
        instance.mutable = False

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and instance.is_superuser:
        Token.objects.create(user=instance)
