from django.urls import  path
from .views import register_view,logout_view,login_view,change_password,base

urlpatterns=[
    # path('',base,name='base'),
    path('register/',register_view,name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password, name='password_change'),

]