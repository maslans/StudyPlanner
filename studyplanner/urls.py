"""
URL configuration for studyplanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileEditView.as_view(), name='profile'),
    path('tasks/', views.TasksListView.as_view(), name='tasks'),
    path('tasks/add/', views.add_or_edit_task, name='add_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/edit/', views.add_or_edit_task, name='add_task'),
    path('tasks/<int:task_id>/done/', views.mark_done, name='mark_done'),

    path('tests/', views.TestListView.as_view(), name='tests'),
    path('tests/add/', views.add_or_edit_test, name='add_test'),
    path('tests/<int:test_id>/delete/', views.delete_task, name='delete_test'),
    path('tests/<int:test_id>/edit/', views.add_or_edit_test, name='add_test'),

    path('exams/', views.ExamListView.as_view(), name='exams'),
    path('exams/add/', views.add_or_edit_exam, name='add_exam'),
    path('exams/<int:exam_id>/delete/', views.delete_task, name='delete_exam'),
    path('exams/<int:exam_id>/edit/', views.add_or_edit_exam, name='add_exam'),

    path('subjects/', views.SubjectListView.as_view(), name='subjects'),
    path('subjects/add', views.add_subject, name='add_subject'),

    path('messages/get/', views.get_messages, name='get_messages'),
    path('messages/send/', views.post_message, name='send_message'),
    path('export/xml/', views.export_tasks_xml, name='export_tasks_xml'),
    path('import/', views.import_tasks, name='import_tasks'),
]
