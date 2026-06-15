from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home import views
urlpatterns = [
    path('', views.home, name='home'),
    path("view_blog/<slug:post_slug>", views.view_blog, name='view_blog'),
    path('category/<slug:category_slug>', views.category_wise_view, name='category_wise_view'),
    path('all_blogs', views.all_blogs, name='all_blogs'),
    path('search', views.search, name='search'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

