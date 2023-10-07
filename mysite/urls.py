
from django.contrib import admin
from django.urls import path
from  main.views import(post_detail,post_list, category_detail,category_list,post_create,post_edit,post_delete,home)
from  account.views import(register,login,logout,activate,activate1,activate_account)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('post/', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('categories/', category_list, name='category_list'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    path('post/create/', post_create, name='post_create'),  
    path('post/edit/<int:pk>/', post_edit, name='post_edit'),  
    path('post/delete/<int:pk>/', post_delete, name='post_delete'),
    path('activate/', activate, name='activate'),
    path('activate1/', activate1, name='activate1'),
    path('activate/<str:mpesa_code>/', activate_account, name='activate_account'),

    path('register/', register, name='register'),
    path('accounts/login/', login, name='login'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),




]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
