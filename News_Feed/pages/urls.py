from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('', views.home, name = 'home'),
 path('login',views.login,name='login'),
 path('signup',views.signup,name='signup'),
 path('logout', views.logout, name='logout'),
 path('dashboard/',views.dashboard, name = 'dashboard'),
 path('category/<str:category_name>/', views.category_posts, name='category_posts'),
 path('read-more/<slug:slug>/',views.read_more, name = 'read_more'),
 path('posts',views.posts,name ='posts'),
 path('post/<slug:slug>/', views.read_more, name='read_more'),
 path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
 path('post/<int:post_id>/save/', views.toggle_save, name='toggle_save'),
 path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
 path('liked/', views.liked_posts, name='liked_posts'),
 path('saved/', views.saved_posts, name='saved_posts'),

]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
