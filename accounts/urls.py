from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('verify_phone/', views.UserVerifyPhone.as_view(), name='verify_phone'),
    path('send_otp_code/', views.AgainSendOtpCodeView.as_view(), name='send_otp_code'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileEditView.as_view(), name='profile_edit'),
    path('change_password/', views.UserChangePassword.as_view(), name='change_password'),
    path('change_password_success/', views.ChangePasswordSuccessView.as_view(), name='change_success'),
    path('forget_password/', views.UserForgetPasswordView.as_view(), name='forget_password'),
    path('forget_password_success/', views.UserForgetPasswordConfirmView.as_view(), name='forget_password_success'),
    path('favorite_list/', views.UserFavoriteListView.as_view(), name='favorite'),
    path('login/', views.UserLoginRegisterView.as_view(), name='login_register'),
]
