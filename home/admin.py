from django.contrib import admin

from home.models import *


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category__category_name', 'status', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured',)

admin.site.register(Contact)
admin.site.register(Comments)