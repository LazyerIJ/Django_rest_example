import datetime
from random import randint
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel


class UserLogin(models.Model):
    # 사용자 로그인 정보 테이블
    class Meta:
        db_table = 'user_login'
    phone_number = models.CharField(max_length=11, primary_key=True)
    password = models.CharField(max_length=30)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

class UserInfo(models.Model):
    # 사용자 정보 테이블
    class Meta:
        db_table = 'user_info'
    name = models.CharField(max_length=15)
    nickname = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=11)
    email = models.CharField(max_length=30, unique=True)
    verified = models.BooleanField(default=False)
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