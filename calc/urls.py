from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('detail/<int:pk>/', views.detail, name='detail'),
#    path('delete/<int:editing_id>/', views.delete, name='delete'),
    path('calc/', views.calc, name='calc'),
    path('ap/', views.apcalc, name='ap'),
]