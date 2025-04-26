from django.urls import path
from . import views
app_name='blog'

urlpatterns=[
    path('',views.material_list, name='material_list'),
    path('<int:id>/', views.material_detail, name='material_detail'),
    path('new/', views.post_new, name='post_new'),
    path('<int:id>/download', views.download_file, name='download_file'),
    path('alt/<int:id>/', views.material_detail2, name='material_detail2')
]
