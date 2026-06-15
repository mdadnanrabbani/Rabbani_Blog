from django.urls import path
from account import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    path('login_user', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout'),
    #Categories
    path('categories', views.categories_acc, name='categories_acc' ),
    path('categories/add_cat', views.add_cat, name='add_cat' ),
    path('categories/delete_cat/<int:id>', views.delete_cat, name='delete_cat'),
    path('categories/edit_cat/<int:id>', views.edit_cat, name='edit_cat'),
    #Posts
    path('post', views.post, name='post'),
    path('post/write_post', views.write_post, name='write_post'),
    path('post/delete/<int:id>', views.delete_post, name='delete_post'),
    path('post/draft_post', views.draft_post, name='draft_post'),
    path('post/edit_post/<int:id>', views.edit_post, name='edit_post'),
    #Users
    path('manage_users', views.manage_users, name='manage_users'),
    path('manage_users/add_new_user', views.add_new_user, name='add_new_user'),
    path('manage_user/delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('manage_user/edit_user/<int:id>', views.edit_user, name='edit_user'),
    #User Profile
    path('profile/<int:id>', views.profile, name='profile'),
    path('profile/edit_profile/<int:id>', views.edit_profile, name='edit_profile'),
]