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
    path('adm_hall',views.adm_halls),
    path('adm_photo',views.adm_photo),

    # user,
    path('user_about',views.user_about),
    path('user_contact',views.user_contact),
    path('user_profile',views.profile, name='profile'),
    path('user_editprofile/<int:cid>/', views.edit_profile, name='edit_profile'),
    path('details/<pid>',views.halldetails),
    path('allhalls',views.allhalls),
    path('alldec',views.alldec),
    path('dec_details/<pid>',views.dec_details),
    path('allfoods',views.allfoods),
    path('bookmark/<pid>',views.bookmark),
    path('dec_mark/<pid>',views.dec_mark),
    path('buy',views.buy),
    
    

]

