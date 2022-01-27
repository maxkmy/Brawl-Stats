from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('display/<str:playerTag>/', views.playerDetail),
    path('display/<str:playerTag>/<str:brawler>', views.brawlerDetail)
]