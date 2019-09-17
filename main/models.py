from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from easy_thumbnails.files import get_thumbnailer

from .utilities import get_timestamp_path


class BoastPost(models.Model):
    author = models.ForeignKey('boast_auth.BoastUser', on_delete=models.CASCADE,
                               related_name='posts')
    created_at = models.DateTimeField(verbose_name='Created', default=timezone.now)
    last_change = models.DateTimeField(verbose_name='Changed', auto_now=True, null=True)
    header = models.CharField(verbose_name='Header', max_length=100, default='I brag about...')
    content = models.TextField(verbose_name='Text')
    likes = models.ManyToManyField('boast_auth.BoastUser', related_name='likes', blank=True)
    image = models.ImageField(verbose_name='Image', upload_to=get_timestamp_path, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('main:detail_post', args=[self.pk])

    def delete(self, *args, **kwargs):
        thumb = get_thumbnailer(self.image)
        thumb.delete_thumbnails()
        super().delete(*args, **kwargs)


class Comment(models.Model):
    message = models.TextField(verbose_name='Comment', max_length=255)
    owner = models.ForeignKey('boast_auth.BoastUser', on_delete=models.CASCADE,
                              related_name='comments')
    post = models.ForeignKey(BoastPost, on_delete=models.CASCADE,
                             related_name='comments')
    created_at = models.DateTimeField(verbose_name='Created', auto_now_add=True,
                                      db_index=True)
