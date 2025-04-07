from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login_api'),
    path('user-login/', views.login_page, name='login_page'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    # In App API's
    path('dashboard/', views.dashboard, name='dashboard'),
    # All Questions related
    path('post-question/', views.post_question, name='post_question'),
    path('question/<int:question_id>/like/', views.toggle_question_like, name='toggle_question_like'),
    path('question/<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    # All Answers related
    path('answer/<int:answer_id>/like/', views.toggle_like, name='toggle_like'),
    path('answer/<int:answer_id>/edit/', views.edit_answer, name='edit_answer'),
    path('answer/<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),
]