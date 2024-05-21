from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from django.db import transaction
from .forms import CustomUserCreationForm, ScreenshotUploadForm, ProfileUpdateForm
from admin_component.models import App, AppUsers
from user_component.models import Screenshot
import json



def format_data(apps):
    app_data = []
    for app in apps:
        name= app.app_name
        link= app.app_link
        category =app.app_category
        sub_category =app.sub_category
        image= app.app_image
        points = app.points
        id=app.id
        app_data.append({
            'id':id,
            'app': app,
            'name':name,
            'link': link,
            'category' :category,
            'subcategory' : sub_category,
            'points' : points,
            'image' : image, 
            'id' :id
        })
    return app_data
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        print(f"form: {form.is_valid()}")
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            password =  form.cleaned_data.get('password1')
            user = authenticate(username =username, password= password)
            print(f"Authenticated user:{user}")
            if user is not None:
                login(request,user)
                return redirect('user_home')
        else:
            print(form.errors)
            return render(request, 'signup.html', {'form': form})
    else:
        form =UserCreationForm()
    return render(request, 'signup.html', {'form':form})   

def login_view(request):
    if request.method == "POST":
        form= AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if user.is_staff:
                return redirect('admin_home')
            else:
                return redirect('user_home')
        else:
            print(form.errors,"user_login")
            return render(request, 'login.html', {'form': form})
    else:
        form =AuthenticationForm()
    return render(request, 'login.html', {'form':form})   


@login_required
def user_home(request):
    installed_apps = App.objects.filter(appusers__user=request.user)
    return render(request, 'user_home.html', {'apps': installed_apps})

@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile')
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'user_profile.html', {'form': form})

@login_required
def user_points(request):
    user = request.user
    total_points = AppUsers.objects.filter(user=user).aggregate(Sum('app__points'))['app__points__sum'] or 0

    category_points = (
        AppUsers.objects.filter(user=user)
        .values('app__app_category__name')
        .annotate(total=Sum('app__points'))
        .order_by('app__app_category__name')
    )

    sub_category_points = (
        AppUsers.objects.filter(user=user)
        .values('app__sub_category__name')
        .annotate(total=Sum('app__points'))
        .order_by('app__sub_category__name')
    )

    context = {
        'total_points': total_points,
        'category_points': json.dumps(list(category_points), cls=DjangoJSONEncoder),
        'sub_category_points': json.dumps(list(sub_category_points), cls=DjangoJSONEncoder),
    }
    return render(request, 'user_points.html', context)

@login_required
def leaderboard(request):
    leaderboard_data = (
        AppUsers.objects.values('user__username')
        .annotate(total_points=Sum('app__points'))
        .order_by('-total_points')
    )

    context = {
        'leaderboard_data': leaderboard_data,
    }
    return render(request, 'leaderboard.html', context)

@login_required
def user_tasks(request):
    # Apps that the user has not installed yet
    installed_apps_ids = AppUsers.objects.filter(user=request.user).values_list('app_id', flat=True)
    tasks_apps = App.objects.exclude(id__in=installed_apps_ids)
    print(tasks_apps)
    data=format_data(tasks_apps)
    return render(request, 'user_tasks.html', {'apps':data })

@login_required
def task_detail(request, app_id):
    app = get_object_or_404(App, id=app_id)
    return render(request, 'task_detail.html', {'app': app})

@login_required
def upload_screenshot(request, app_id):
    app = get_object_or_404(App, id=app_id)
    if request.method == 'POST':
        form = ScreenshotUploadForm(request.POST, request.FILES)

        if form.is_valid():
            with transaction.atomic():
                screenshot = form.save(commit=False)
                screenshot.user = request.user
                screenshot.app = app
                screenshot.save()
                AppUsers.objects.create(user=request.user, app=app)
            messages.success(request, 'Screenshot uploaded successfully.')
            return redirect('user_tasks')
        else:
            messages.error(request, 'Failed to upload screenshot.')
    return redirect('task_detail', app_id=app_id)

@login_required
def installed_app_detail(request, app_id):
    app = get_object_or_404(App, id=app_id)
    screenshot = get_object_or_404(Screenshot, app=app, user=request.user)
    return render(request, 'installed_app_detail.html', {'app': app, 'screenshot': screenshot})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_dashboard(request):
    # Get the current logged-in user
    user = request.user

    # Assuming you have a field named 'username' in your User model
    username = user.username

    # Get total points for the user (assuming a 'user' foreign key in the Point model)
    # total_points = Point.objects.filter(user=user).aggregate(total_points=Sum('points'))['total_points'] or 0

    # Get points breakdown by platform (assuming a 'platform' field in the Point model)
    # points_breakdown = Point.objects.filter(user=user).values('platform').annotate(total_points=Sum('points'))

    context = {
        'username': username,
        'total_points': 10,
        # 'points_breakdown': points_breakdown,
    }
    return render(request, 'user_dashboard.html', context)
