from django.contrib import admin
from django.urls import path
from referral.views import SignUpView, LogInView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
]
