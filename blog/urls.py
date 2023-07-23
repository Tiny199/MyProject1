from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('',views.HomeView.as_view(),name="home"),
    path('article/<int:pk>',views.ArticleView.as_view(), name='article-details'),
    path('add_post/',views.AddPost.as_view(),name='add_post'),
    path('add_category/',views.AddCategory.as_view(),name='add_category'),
    path('article/edit/<int:pk>',views.EditPost.as_view(),name='edit_post'),
    path('article/<int:pk>/delete/',views.DeletePost.as_view(),name='delete_post'),
    path('registery/',views.UserRegisterView.as_view(),name='register'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('category/<str:cats>/',views.Categoryview,name='category'),
    path('like/<int:pk>',views.LikeView ,name='like_post'),
    #path( 'like/<int:pk>',views.LikeViewPost,name='like_post'),
    path('edit_profile/',views.UserEditView.as_view(),name='edit_profile'),
    path('<int:pk>/password/',views.PassChangeVW.as_view(template_name='member/change_pass.html')),
    path('password_changed',views.passs_changed,name='password_changed'),
    path('<int:pk>/profile/',views.ProfilePageView.as_view(), name='profile_page_show'),
    path('<int:pk>/edit_profile/',views.EditProfilePageView.as_view(), name='profile_page_edit'),
    path('create_profile/',views.CreateProfilePageView.as_view(), name='create_profile_page'),
    path('article/<int:pk>/comment/', views.AddCommentview.as_view(), name='add_comment'),
]