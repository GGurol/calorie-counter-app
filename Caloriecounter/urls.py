from django.urls import path
from . import views
from .views import delete_meal_grocery

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("diary/", views.diary, name="diary"),
    path('recipes/', views.recipes, name='recipes'),
    path('fasting/', views.fasting, name='fasting'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('grocery_search/', views.grocery_search, name='grocery_search'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_meal', views.add_meal, name='add_meal'),
    path('show_meal/', views.show_meal, name='show_meal'),
    path('grocery_detail/<int:grocery_id>/', views.grocery_detail, name='grocery_detail'),
    path('delete_meal_grocery/<int:meal_grocery_id>/', delete_meal_grocery, name='delete_meal_grocery'),
    path('steps', views.steps, name='steps')
]