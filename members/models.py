from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# AbstractBaseUser: Django의 기본 인증 시스템에서 제공하는 클래스, 사용자 모델을 직접 정의할 때
# 확장할 수 있는 추상 클래스로 비번, 인증 관련 메서드 등을 포함
# BaseUserManager: 사용자 객체를 생성하고 관리하기 위해 사용하는 클래스, 사용자 모델을 커스터마이징할 때
# 반드시 커스터마이징 된 Manager를 정의
from django.db import models


# User에서 기존의 username을 email로 바꿔줬기 때문에
# UserManager를 오버라이딩 해줘야됨
class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('올바른 이메일을 입력하세요.')

        user = self.model(
            email = self.normalize_email(email),
        )
        # 패스워드 암호화
        user.set_password(password)
        user.is_active = False
        # using=self._db : 다중 DB 환경에서 기본 DB를 사용하라는 것
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email', # verbose_name : 필드의 이름으로 관리자 페이지나 메시지에서 사용됨
        unique=True
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    nickname = models.CharField('nickname', max_length=20, unique=True)

    objects = UserManager() # 커스터마이징 된 UserManager를 연결함. 사용자 생성 로직은 이 객체를 통해 이루어짐
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

    def __str__(self): # 객체를 문자열로 표현할 때 반환값, 여기서는 닉네임을 반환
        return self.nickname

    def has_perm(self, perm, obj=None): # 권한 검사 메서드, 관리자 페이지나 특정 작업에 대한 접근 권한이 필요한 경우 실행
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    # @property
    # 원래 user.is_superuser() 라고 써야되는데
    # user.is_speruser로 써도 되게 만들어줌