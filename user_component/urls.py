from django.urls import path
from . import views as user_views


urlpatterns = [
    path('', user_views.login_view, name='login'),
    path('signup/', user_views.signup_view, name='signup'),
    path('home/', user_views.user_home, name='user_home'),
    path('installed_app/<int:app_id>/', user_views.installed_app_detail, name='installed_app_detail'),
    path('profile/', user_views.user_profile, name='user_profile'),
    path('points/', user_views.user_points, name='user_points'),
    path('leaderboard/', user_views.leaderboard, name='leaderboard'),
    path('tasks/', user_views.user_tasks, name='user_tasks'),
    path('tasks/<int:app_id>/', user_views.task_detail, name='task_detail'),
    path('tasks/<int:app_id>/upload/', user_views.upload_screenshot, name='upload_screenshot'),
    path('logout/', user_views.logout_view, name='logout'),
    path('dashboard/', user_views.user_dashboard, name='user_dashboard'),
]