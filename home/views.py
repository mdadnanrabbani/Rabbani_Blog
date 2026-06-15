from django.contrib import messages
from django.db.models import Q, Model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from blog import settings
from home.forms import ContactForm, CommentForm
from home.models import BlogPost, Contact, Comments
from django.core.mail import send_mail



# Create your views here.


def home(request):
    posts = BlogPost.objects.filter(is_featured = True, status = 'published')
    recent_posts = BlogPost.objects.filter(status = 'published', is_featured = False).order_by('-created_at')[:6]
    context = {
        'posts': posts,
        'recent_posts': recent_posts
    }

    return render(request, 'Pages/index.html', context)


def view_blog(request, post_slug):
    post = BlogPost.objects.get(slug = post_slug)
    recent_posts = BlogPost.objects.filter(status = 'published', is_featured = False).order_by('-created_at') [:6]
    comment = Comments.objects.filter(blog_post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comments.objects.create(
                author = request.user,
                blog_post = post,
                content = form.cleaned_data['content'],
            )
            return redirect('view_blog', post_slug)

    else:
        form = CommentForm()

    context = {
        'post': post,
        'recent_posts': recent_posts,
        'comment': comment,
        'form': form
    }
    return render(request, 'Pages/view_blog.html', context)


def category_wise_view(request, category_slug):
    posts = BlogPost.objects.filter(status = 'published' , category__slug = category_slug)

    return render(request, 'Pages/category_wise_view.html', {'posts': posts})


def all_blogs(request):
    blogs = BlogPost.objects.filter(status = 'published')
    return render(request, 'Pages/all_blogs.html', {'blogs': blogs})


def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        posts = BlogPost.objects.filter( Q(status = 'published'),Q(title__icontains = query) | Q(content__icontains = query) | Q(author__username__icontains = query))

    return render(request, 'Pages/search.html', {'posts': posts})


def about(request):
    return render(request, 'Pages/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email = form.cleaned_data['email'],
                subject = form.cleaned_data['subject'],
                message = form.cleaned_data['message'],
            )
            messages.success(request, 'Thank You for contacting us, We will revert shortly')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'Pages/contact.html', {'form': form})
