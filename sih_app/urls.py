from django.urls import path
from .views import InitialView, Signup, Signin, Home, Profile, Logout, Search, send_data, C_DLS, UpdateProfile, events, news
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('Ajax/getdata/', send_data, name='ajax_view'),
    path('', InitialView.as_view(), name='land'),
    path('Signup/<str:email>/', Signup.as_view(), name='signup'),
    path('Signin/', Signin.as_view(), name='signin'),
    path('Search/', Search.as_view(), name='search'),
    path('Home/', Home.as_view(), name='home'),
    path('Profile/', Profile.as_view(), name='profile'),
    path('Logout/', Logout.as_view(), name='logout'),
    path('C-DLS/', C_DLS.as_view(), name='C-DLS'),
    path('Update/', UpdateProfile.as_view(), name='update'),
    path('Events/', events, name='events'),
    path('Notice/', news, name='news')
]

