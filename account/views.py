from multiprocessing import context

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify

from account.forms import RegisterForm, LoginForm, addCategory, addPost, addUser, EditUser
from home.models import Category, BlogPost


# Create your views here.

@login_required(login_url='login_user')
def dashboard(request):
    user = request.user
    total_blog_count = BlogPost.objects.filter(author=user).count()
    total_category = Category.objects.all().count()

    context = {
        'TotalBlogsCount': total_blog_count,
        'TotalCategories': total_category,
    }
    return render(request,'Pages/dashboard.html', context)



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')

            User.objects.create_user(
                email=email,
                username=username,
                password=password
            )

            messages.success(request, 'User created successfully')
            return redirect('login_user')

    else:
        form = RegisterForm()

    return render(request, 'Pages/register.html', {'form': form})



def login_user (request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request, username=username, password=password
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid Credentials')

    else:
        form = LoginForm()
    return render(request, 'Pages/user_login.html', {'form': form})



@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('home')



@login_required(login_url='login_user')
@permission_required('home.view_category', raise_exception=True)
def categories_acc(request):
    categories = Category.objects.all()
    return render(request,'Pages/categories_acc.html', {'categories': categories})

@permission_required('home.add_category', raise_exception=True)
@login_required(login_url='login_user')
def add_cat(request):
    if request.method == 'POST':
        form = addCategory(request.POST)
        if form.is_valid():
           category = Category.objects.create(
                category_name = form.cleaned_data['category_name'],
            )
           category.slug = slugify(category.category_name + '-'+ str(category.id) )
           category.save()
           return redirect('categories_acc')

    else:
        form = addCategory()
    context = {
        'form': form
    }
    return render(request,'Pages/add_cat.html', context)

@login_required(login_url='login_user')
@permission_required('home.delete_category', raise_exception=True)
def delete_cat(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('categories_acc')

@login_required(login_url='login_user')
@permission_required('home.chnage_category', raise_exception=True)
def edit_cat(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = addCategory(request.POST, initial={'category_name': category.category_name})
        if form.is_valid():
            category.category_name = form.cleaned_data['category_name']
            category.save()
            return redirect('categories_acc')
    else:
        form = addCategory(initial={'category_name': category.category_name})
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'Pages/edit_cat.html', context)


@login_required(login_url='login_user')
@permission_required('home.view_blogpost', raise_exception=True)
def post(request):
    posts = BlogPost.objects.filter(author=request.user, status='published')
    return render(request,'Pages/post.html', {'posts': posts})

@login_required(login_url='login_user')
@permission_required('home.add_blogpost', raise_exception=True)
def write_post(request):
    if request.method == 'POST':
        form = addPost(request.POST, request.FILES)
        if form.is_valid():
            post = BlogPost.objects.create(
                title = form.cleaned_data['title'],
                short_description =form.cleaned_data['short_description'],
                content = form.cleaned_data['content'],
                featured_img = form.cleaned_data['featured_img'],
                status = form.cleaned_data['status'],
                category = form.cleaned_data['category'],
                author=request.user,
                is_featured = form.cleaned_data['is_featured'],
            )
            post.slug = slugify(post.title + '-' + str(post.id))
            post.save()
            return redirect('dashboard')
    else:
        form = addPost()
    context = {
        'form': form,
    }
    return render(request,'Pages/write_post.html', context)


@login_required(login_url='login_user')
@permission_required('home.delete_blogpost', raise_exception=True)
def delete_post(request, id):
    post = BlogPost.objects.get(id=id)
    post.delete()
    return redirect('post')


@login_required(login_url='login_user')
@permission_required('home.view_blogpost', raise_exception=True)
def draft_post(request):
    posts = BlogPost.objects.filter(status='draft', author=request.user)
    return render(request,'Pages/draft_post.html', {'posts': posts})



@login_required(login_url='login_user')
@permission_required('home.change_blogpost', raise_exception=True)
def edit_post(request, id):
    post = BlogPost.objects.get(id=id)
    if request.method == 'POST':
        form = addPost(request.POST, request.FILES)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.short_description = form.cleaned_data['short_description']
            post.content = form.cleaned_data['content']
            post.featured_img = form.cleaned_data['featured_img']
            post.status = form.cleaned_data['status']
            post.category = form.cleaned_data['category']
            post.author = request.user
            post.is_featured = form.cleaned_data['is_featured']
            post.save()
            return redirect('post')

    else:
        form = addPost(initial={
            'title': post.title,
            'short_description': post.short_description,
            'content':post.content ,
            'featured_img': post.featured_img,
            'status': post.status,
            'category': post.category,
            'is_featured': post.is_featured})
    context = {
        'form': form,
        'post': post,
    }
    return render(request,'Pages/edit_post.html', context)


@login_required(login_url='login_user')
@permission_required('auth.view_user', raise_exception=True)
def manage_users(request):
    users = User.objects.all()
    return render(request,'Pages/manage_users.html', {'users': users})

@login_required(login_url='login_user')
@permission_required('auth.add_user', raise_exception=True)
def add_new_user(request):
    if request.method == 'POST':
        form = addUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = addUser()
    return render(request,'Pages/add_new_user.html', {'form': form})



@login_required(login_url='login_user')
@permission_required('auth.delete_user', raise_exception=True)
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('manage_users')

@login_required(login_url='login_user')
@permission_required('auth.change_user', raise_exception=True)
def edit_user(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = addUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = addUser(instance=user)
    context = {
        'form': form,
        'user': user,
    }
    return render(request,'Pages/edit_user.html', context)

@login_required(login_url='login_user')
def profile(request, id):
    user = User.objects.get(id=id)
    posts = BlogPost.objects.filter(author=user)
    context = {
        'posts': posts,
        'user': user,
    }
    return render(request,'Pages/profile.html', context)


def edit_profile(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = EditUser(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
    else:
        form = EditUser(initial={
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
    context = {
        'form': form,
        'user': user,
    }
    return render(request,'Pages/edit_profile.html', context)