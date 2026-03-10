from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage,name='home'),
    path('/report',views.report,name='report'),
    path('/manage/<int:issue_id>/',views.manage,name='manage'),
    path('delete_issue/<int:id>/', views.delete_issue, name='delete_issue'),
    path('map_view/',views.map_view,name='map'),
]
