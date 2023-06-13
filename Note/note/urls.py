from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'note'

urlpatterns = [
    path('group/<int:pk>/delete/', views.group_delete, name='group_delete'),
    path('', views.note_list, name='note_list'),
    path('group/new/', views.group_new, name='group_new'),
    path('group/<int:pk>/note/add/', views.group_note_add, name='group_note_add'),
    path('note/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('note/new/', views.note_add, name='note_new'),
]

urlpatterns += staticfiles_urlpatterns()