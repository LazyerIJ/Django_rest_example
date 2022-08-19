import datetime
from random import randint
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

from config.utils import get_config_value


class AblyUserManager(BaseUserManager):
    def create_user(self, email, password, phone_number, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not phone_number:
            raise ValueError(_('The Email must be set'))
        user = self.model(email=email, phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user
    
    
class User(AbstractBaseUser):
    # 사용자 로그인 정보 테이블
    class Meta:
        db_table = 'user'
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, primary_key=True)
    verified = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    
    objects = AblyUserManager()
    
    @staticmethod
    def is_exists_phone_number(phone_number):
        users = User.objects.filter(phone_number=phone_number)
        return (True, users[0]) if users else (False, None)
    
    def is_login(self, request):
        return request.session.get(self.phone_number, False)
    
    def login(self, request):
        try:
            request.session[self.phone_number] = True
            return True
        except Exception as e:
            return False
    
    def logout(self, request):
        try:
            del request.session[self.phone_number]
            return True
        except Exception as e:
            return False
    

class UserInfo(models.Model):
    # 사용자 정보 테이블
    class Meta:
        db_table = 'user_info'
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=AnonymousUser)
    name = models.CharField(max_length=15)
    nickname = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


class UserAuth(TimeStampedModel):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_auth'

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        if get_config_value("ACCESS_TYPE") == "dev":
            self.auth_number = "0000"
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