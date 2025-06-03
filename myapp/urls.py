from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'), 
    path('logout/', views.custom_logout, name='logout'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photos/<str:tag>/', views.photos_by_tag, name='photos_by_tag'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    path('photos/<int:pk>/edit/', views.edit_photo, name='edit_photo'),
    path('photos/<int:pk>/delete/', views.delete_photo, name='delete_photo'),
]