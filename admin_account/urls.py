from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    path('login/', views.ObtainTokenPairApiView.as_view(), name = 'token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',views.UserLoggoutApiView.as_view(), name='logout' ),
    path('create_account/', views.CreateAdminUserApiView.as_view(), name = 'create_account'),
    path('forgot_password/', views.ForgotPasswordApiView.as_view(),name='forgot_password'),
    path('verify_verification_code/', views.VerifyVerificationCode.as_view(), name='verify_verification_code'),
    path('reset_password/', views.SetPasswordApiView.as_view(), name='set_password'),
]