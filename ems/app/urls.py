from django.urls import path
from . import views
urlpatterns = [
    path('',views.login),
    path('register',views.user_reg),
    path('adm_home',views.adm_home),
    path('usr_home',views.user_home),
    path('stf_home',views.staff_home),
    path('stf_reg',views.staff_reg),
    path('logout',views.logout),
    # admin,
    path('adm_catering',views.adm_catering),
    path('adm_dec',views.adm_decr),
]

