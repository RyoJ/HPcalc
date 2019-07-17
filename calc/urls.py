from django.urls import path
from . import views

app_name = 'apcalc'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('detail/<int:pk>/', views.detail, name='detail'),
#    path('delete/<int:editing_id>/', views.delete, name='delete'),
    path('calc/', views.calc, name='calc'),
    path('apc/', views.apcalc, name='apc'),
    path('graph/', views.graph, name='graph'),
    path('graph_hp/', views.graph_hp, name='graph_hp'),
    path('graph_mp/', views.graph_mp, name='graph_mp'),
    path('graph_all/', views.graph_all, name='graph_all'),
    path('analysis/plot/', views.img_plot, name="img_plot"),
]