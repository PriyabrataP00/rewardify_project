from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from .forms import AddAppForm, CategoryForm, SubCategoryForm,AdminUserCreationForm
from .models import Category, SubCategory, AppUsers, App

def admin_login_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url = '/admin/login')(view_func)
    return decorated_view_func


@admin_login_required
def admin_dashboard(request):
    status_message=""
    overwrite_warning = False
    existing_app_id = None

    if request.method == 'POST':
        
        if 'confirm_overwrite' in request.POST:
            existing_app_id = request.POST.get('existing_app_id')
            app = App.objects.get(id=existing_app_id)
            form = AddAppForm(request.POST, request.FILES, instance=app)
            if form.is_valid():
                form.save()
                status_message = "App overwritten successfully!"
                
            else:
                status_message = "Failed to overwrite app!"
        else:
            form = AddAppForm(request.POST, request.FILES)
            if form.is_valid():
                app_name = form.cleaned_data.get('name')
                existing_app = App.objects.filter(app_name=app_name).first()
                if existing_app:
                    overwrite_warning = True
                    existing_app_id = existing_app.id
                else:
                    form.save()
                    status_message = "App added Successfully!"
            else:
                print(form.errors)
                status_message = "Failed to add app!"
    else:
        form = AddAppForm()
    return render(request, 'admin_dashboard.html', {'form': form, 
                                                    'category_form': CategoryForm(),
                                                    'subcategory_form': SubCategoryForm(),
                                                    'status_message' : status_message,
                                                     'overwrite_warning': overwrite_warning,
                                                     'existing_app_id': existing_app_id })

@admin_login_required
def home_view(request):

    apps = App.objects.all()
    app_data = []
    for app in apps:
        name= app.app_name
        link= app.app_link
        category =app.app_category
        sub_category =app.sub_category
        image= app.app_image
        downloads = AppUsers.objects.filter(app=app).count()
        points=app.points
        total_points = downloads * points
        
        app_data.append({
            'app': app,
            'name':name,
            'link': link,
            'category' :category,
            'subcategory' : sub_category,
            'downloads': downloads,
            'points':points,
            'total_points': total_points,
            'image' : image
        })
    return render(request, 'admin_home.html', {'app_data': app_data})


@admin_login_required
def settings_view(request):
    # Initialize forms
    category_form = CategoryForm()
    subcategory_form = SubCategoryForm()
    app_form = AddAppForm()

    if request.method == 'POST':
        if 'category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('settings')
        elif 'subcategory' in request.POST:
            subcategory_form = SubCategoryForm(request.POST)
            if subcategory_form.is_valid():
                subcategory_form.save()
                return redirect('settings')
        elif 'edit_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id)
            category_form = CategoryForm(request.POST, instance=category)
            if category_form.is_valid():
                category_form.save()
                return redirect('settings')
        elif 'edit_subcategory' in request.POST:
            subcategory_id = request.POST.get('subcategory_id')
            subcategory = get_object_or_404(SubCategory, id=subcategory_id)
            subcategory_form = SubCategoryForm(request.POST, instance=subcategory)
            if subcategory_form.is_valid():
                subcategory_form.save()
                return redirect('settings')

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    context = {
        'categories': categories,
        'subcategories': subcategories,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
    }
    return render(request, 'admin_settings.html', context)

def create_admin_user_view(request):
    admin_user_form = AdminUserCreationForm()

    if request.method == 'POST':
        admin_user_form = AdminUserCreationForm(request.POST)
        if admin_user_form.is_valid():
            admin_user_form.save()
            return redirect('create_admin_user')  # Redirect to refresh the page

    return render(request, 'create_admin_user.html', {
        'admin_user_form': admin_user_form})

@admin_login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('settings')

@admin_login_required
def delete_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    subcategory.delete()
    return redirect('settings')

@admin_login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})

@admin_login_required
def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = SubCategoryForm(instance=subcategory)
    return render(request, 'edit_subcategory.html', {'form': form})



def admin_login_view(request):
    if request.method == 'POST':
        form= AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            # Redirect to admin home
            return redirect('admin_home')
        else:
            print(form.errors,"admin_login")
            # Display error message for invalid credentials
            return render(request, 'admin_login.html', {'error_message': 'Invalid username or password.'})
    else:
        form=AuthenticationForm()
    return render(request, 'admin_login.html')

def logout_view(request):
    logout(request)
    return redirect('login')