import datetime
from random import randint
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel


class User(models.Model):
    class Meta:
        db_table = 'user'
    name = models.CharField(max_length=15)
    nickname = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class UserAuth(TimeStampedModel):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_auth'

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        super().save(*args, **kwargs)

    @classmethod
    def check_auth_number(cls, p_num, c_num):
        time_limit = timezone.now() - datetime.timedelta(minutes=5)
        result = cls.objects.filter(
            phone_number=p_num,
            auth_number=c_num,
            modified__gte=time_limit
        )

        if result:
            return True

        return False
