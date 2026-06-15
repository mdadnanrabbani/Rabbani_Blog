from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from home.models import Category


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField( label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField( label = 'Conform password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))


class LoginForm(forms.Form):
    username = forms.CharField(label='User Name' , widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label = 'Password' , widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class addCategory(forms.Form):
    category_name = forms.CharField(label='Category Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sports, Music, etc'}))


class addPost(forms.Form):
    STATUS_CHOICES = {
        'published': 'Published',
        'draft': 'Draft',
    }
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your post title...'}))
    short_description = forms.CharField(label = 'Short Description', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your post short description...'}))
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your post content...'}))
    featured_img = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select Category', widget=forms.Select(attrs={'class': 'form-control'}))
    is_featured = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox-label'}))

class addUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')


class EditUser(forms.Form):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
