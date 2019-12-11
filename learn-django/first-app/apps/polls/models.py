import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    # models.CASCADE: 删除主表记录的时候删除子表纪录
    # models.SET_NULL: 删除主表记录的时候子表关联列设为NULL
    # models.PROTECT: 删除主表记录的时候子表存在记录，报完整性错误
    # models.SET_DEFAULT: 删除主表记录的时候子表关联列设为默认值
    # models.SET:
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.question.question_text + '@@@ ' + self.choice_text
