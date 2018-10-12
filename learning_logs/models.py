from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """topic은 사용자가 공부하고 있는 주제이다."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        """모델에 관한 정보를 문자열 형태로 변환한다."""
        return self.text

class Entry(models.Model):
    """주제에 관해 공부한 내용"""
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """모델에 관한 정보를 문자열 형태로 반환한다."""
        if self.text[:] > self.text[:50]:
            return self.text[:50] + "..."
        else:
            return self.text[:]
