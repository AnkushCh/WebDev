from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordChangeDoneView,PasswordChangeView
from hack_app import views

urlpatterns = [
    path('', views.home, name='home'),
    
    
    path('register/', views.signup, name='signup'),
    
    # path('profile/', views.profile, name='profile'),
    # path('editprofile/',views.update_profile,name='editprofile'),
    url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    
    path('login/',  views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    path('password-reset/', PasswordResetView.as_view(),{'post_change_redirect': 'password_reset_done'}, name='password_reset',),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change-done/',PasswordChangeDoneView.as_view(),name='password_change_done' ),
    path('password-change/',PasswordChangeView.as_view(),{'post_change_redirect': 'password_change_done'}, name='password_change'),
]