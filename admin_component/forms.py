# admin_component/forms.py
from django import forms
from .models import App, Category, SubCategory
from django.contrib.auth.models import User

class AddAppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['app_name', 'app_link', 'app_category', 'sub_category', 'points', 'app_image']
        model = App
        fields = ['app_name', 'app_link', 'app_category', 'sub_category', 'points', 'app_image']
        widgets = {
            'app_name': forms.TextInput(attrs={'placeholder': 'App Name'}),
            'app_link': forms.TextInput(attrs={'placeholder': 'App Link'}),
            'points': forms.NumberInput(attrs={'placeholder': 'Points'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['app_category'].queryset = Category.objects.all()
        self.fields['sub_category'].queryset = SubCategory.objects.all()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('This field is required.')
        return image

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Category Name'}),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Sub Category Name'}),
        }

class AdminUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True
        user.is_superuser = False  # Custom admin should not be a superuser
        if commit:
            user.save()
        return user