"""
URL configuration for the tracker app.
"""
from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # AJAX APIs
    path('api/task/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
    path('api/task/<int:task_id>/note/', views.save_task_note, name='save_task_note'),
    path('api/task/add/', views.add_task, name='add_task'),

    # Coding Practice
    path('api/coding/<int:cp_id>/update/', views.update_coding_practice, name='update_coding_practice'),
    path('api/coding/add/', views.add_coding_practice, name='add_coding_practice'),

    # Mistake Log
    path('api/mistake/add/', views.add_mistake, name='add_mistake'),
    path('api/mistake/<int:mistake_id>/toggle/', views.toggle_mistake, name='toggle_mistake'),
    path('api/mistake/<int:mistake_id>/delete/', views.delete_mistake, name='delete_mistake'),

    # Progress API (for AJAX partial re-renders)
    path('api/progress/', views.get_progress_data, name='get_progress_data'),
]
