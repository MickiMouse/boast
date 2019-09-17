from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activation_notification
from main.utilities import get_timestamp_path

user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(**kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


class BoastUser(AbstractUser):
    is_activated = models.BooleanField(verbose_name='Activated email?', default=False)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)
    avatar = models.ImageField(verbose_name='Avatar', upload_to=get_timestamp_path,
                               blank=True, null=True)

    class Meta(AbstractUser.Meta):
        pass
