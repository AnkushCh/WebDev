from django.urls import path,include
from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView
from django.conf.urls.static import static
from django.conf import settings
from hack_app import views
from .forms import *

urlpatterns = [
    path('', views.home, name='home'),
    
    
    path('register/', views.signup, name='signup'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('accounts/profile/', views.view_profile, name='profile'),
    path('accounts/editprofile/',views.edit_profile,name='editprofile'),
    # path('accounts/password/change',views.change_password ,name='account_change_password'),
    path('accounts/password/',PasswordResetView.as_view(),{'post_change_redirect': 'password_reset_done'} ,name='account_set_password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    path('contact_us',views.contact_us,name='contact_us'),
    path('login/',  views.login_view, name='login'),
    
    url('^', include('django.contrib.auth.urls')),

    path("reimburse",views.TReimburseCreateView.as_view(),name='reimburse'),
    path('regwizard/',views.RegViewWizard.as_view([RegForm1,RegForm2]),name='regwizard'),
    path('org_dashboard/',views.org_dashboard,name='org_dashboard'),
    # new-------------------
    path('reglists',views.RegsListView.as_view(),name="reglists"),
    path('reglists',views.RegsListView.as_view(),name="reglists"),
    path('travellists',views.TravelListView.as_view(),name="travellists"),
    path('traveldetail/<int:pk>',views.TravelDetailView.as_view(),name="traveldetail"),
    path("accept_travel/<int:pk>",views.AcceptTravel.as_view(),name="accept_travel"),
    path('regdetail/<int:pk>',views.RegDetailView.as_view(),name="regdetail"),
    path("upvote/<int:pk>",views.Upvote.as_view(),name="upvote"),
    path("downvote/<int:pk>",views.Downvote.as_view(),name="downvote"),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)