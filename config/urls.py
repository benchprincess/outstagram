from django.contrib import admin
from django.urls import path
from members import views as member_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # auth
    path('signup/', member_views.SignupView.as_view(), name='signup'),
    # as_view()는 CBV를 FBV처럼 사용할 수 있게 변환하는 메서드
]
