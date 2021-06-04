


from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.signin, name='login'), 
    path('logout/', views.signout, name='logout'), 
    path('signup/', views.signup, name='signup'),
    path('department/', views.department, name='department'),
    path('departments/<str:name>/', views.dep_display, name='dep_display'),
    path('departments/<str:name>/<str:number>/', views.school_year, name='school_year'),
    path('account/<str:name>/', views.account, name="account"),
    path('forms/', views.forms, name="forms"),
    path('forms/stream/', views.stream_form, name="stream_form"),
    path('add_project/<str:name>/', views.add_project, name="add_project"),

   
    path('fira/', views.profile_settings, name='pro'),
    path('render_pdf/<str:name>/', views.render_pdf, name="render_pdf"),

]