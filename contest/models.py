from django.db import models


class Contest(models.Model):
    title = models.CharField(max_length=50, help_text='대회 이름')
    image_url = models.URLField(max_length=200, default='', help_text='대회 이미지 주소')
    content = models.TextField(max_length=300, help_text='대회 내용')

