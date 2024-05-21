from django.urls import path
from . import views as admin_views


urlpatterns = [
    path('', admin_views.admin_login_view, name='admin_login'),
    path('home/', admin_views.home_view, name='admin_home'),
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('settings/', admin_views.settings_view, name='settings'),
    path('create_admin_user/', admin_views.create_admin_user_view, name='create_admin_user'),
    path('logout/', admin_views.logout_view, name='logout'),
    path('settings/delete_category/<int:category_id>/', admin_views.delete_category, name='delete_category'),
    path('settings/delete_subcategory/<int:subcategory_id>/', admin_views.delete_subcategory, name='delete_subcategory'),
    path('settings/edit_category/<int:category_id>/', admin_views.edit_category, name='edit_category'),
    path('settings/edit_subcategory/<int:subcategory_id>/', admin_views.edit_subcategory, name='edit_subcategory'),
]