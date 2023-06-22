from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'note'

urlpatterns = [
    path('group/<int:pk>/delete/', views.group_delete, name='group_delete'),
    path('', views.note_list, name='note_list'),
    path('group/new/', views.group_new, name='group_new'),
    path('search/', views.search_notes, name='search_notes'),
    path('group/<int:pk>/note/add/', views.group_note_add, name='group_note_add'),
    path('note/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/photo/', views.photo_upload, name='photo_upload'),
    path('profile/status/update/', views.employment_status_update, name='status_update'),
    path('profile/change_password/', views.change_password, name='change_password'),
    path('profile/delete/<int:pk>/  ', views.profile_delete, name='profile_delete'),
    path('photo/delete/<int:pk>/', views.photo_delete, name='photo_delete'),
]

urlpatterns += staticfiles_urlpatterns()