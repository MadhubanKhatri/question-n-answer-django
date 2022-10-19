from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('login/', views.login, name='login'),
	path('signup/', views.signup, name='signup'),
	path('logout/', views.log_out, name='logout'),
	path('<str:question>/create_post/', views.create_post, name='create_post'),
	path('<str:question>/save_answer/', views.save_answer, name='save_answer'),
	path('<str:question>/show_answers/', views.show_answers, name='show_answers'),
	path('profile/', views.profile, name='profile'),
	path('ask_question/', views.ask_question, name='ask_question'),
	path('save_question/', views.save_question, name='save_question'),
	path('search_tool/', views.search_tool, name='search_tool')
]