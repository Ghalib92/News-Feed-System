from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
import os
 
from django.urls import reverse_lazy





urlpatterns = [

 path('', views.home, name = 'home'),
 path('login',views.login,name='login'),
 path('signup',views.signup,name='signup'),
 path('change-password/', views.change_password, name='change_password'), 
 path('logout', views.logout, name='logout'),
 path('dashboard/',views.dashboard, name = 'dashboard'),
 path('profile/', views.profile_view, name='profile'),
 path('category/<str:category_name>/', views.category_posts, name='category_posts'),
 path('read-more/<slug:slug>/',views.read_more, name = 'read_more'),
 path('posts',views.posts,name ='posts'),
 path('post/<slug:slug>/', views.read_more, name='read_more'),
 path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
 path('post/<int:post_id>/save/', views.toggle_save, name='toggle_save'),
 path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
 path('liked/', views.liked_posts, name='liked_posts'),
 path('saved/', views.saved_posts, name='saved_posts'),
 path('analytics/', views.analytics_view, name='analytics'),
 path('get-analytics-data/', views.get_analytics_data, name='get_analytics_data'),
 


]



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(BASE_DIR, 'static'))

