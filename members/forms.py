from django.contrib.auth import get_user_model
# 현재 설정된 사용자 모델을 가져옴, 커스터마이징한 사용자 모델을 가져올 경우
# get_use_model()을 사용해야 올바른 모델을 참조함
from django.contrib.auth.forms import UserCreationForm
# django가 제공하는 기본 사용자 생성 폼
# 비번 확인 등의 로직이 이미 구현되어 있어서, 이를 상속받아 커스터마이징함

User = get_user_model() # 사용 중인 사용자 모델 User를 변수로 저장

class SignupForm(UserCreationForm):
    # 기본 사용자 생성 폼(UserCreationForm)을 확장한 커스터마이징 된 사용자 회원가입 폼

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')
        label = {
            'email': '이메일',
            'password1' : '비밀번호',
            'password2' : '비밀번호 확인',
        }
        widgets = {
            'email' : forms.EmailInput(
                attrs = {
                    'placeholder': 'example@example.com',
                }
            )
        }
