from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),
    path('edit/<int:editing_id>/', views.edit, name='edit'),
#    path('delete/<int:editing_id>/', views.delete, name='delete'),
    path('calc/', views.calc, name='calc'),
    path('calc2/', views.calc2, name='calc2'),
]