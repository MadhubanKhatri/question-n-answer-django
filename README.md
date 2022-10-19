Welcome Friends,
This is our new blog. In this blog, I am creating a **Question-n-Answer** website like, [Stackoverflow](https://stackoverflow.com), [Quora](https://quora.com). 

## About the Website ?
This website is able to _Signup & Login_. After login user can access its _Home page_ where users' questions are displayed. User can click on question and see its answers. User's name and upload date are also displayed below the answer. Other users can write the answer for particular question. User can ask the question and can see them in their _profile page_. A search tool also included in this website which can search the user's related query.

Here my source code:-
### models.py
```python
from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class User(models.Model):
	user_name = models.CharField(max_length=50)
	email = models.EmailField()
	pass_word = models.CharField(max_length=50)
	gender = models.CharField(max_length=10)

	def __str__(self):
		return self.user_name


class AnswerSection(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	answer = models.TextField()
	upload_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.answer

class QuestionSection(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	question = models.CharField(max_length=200)
	upload_date = models.DateField(auto_now_add=True)
	answer = models.ManyToManyField(AnswerSection)

	def __str__(self):
		return self.question

```

### admin.py
```python
from django.contrib import admin
from .models import User, QuestionSection, AnswerSection
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'gender')

@admin.register(QuestionSection)
class QuestionSectionAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'upload_date')

@admin.register(AnswerSection)
class AnswerSectionAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user', 'upload_date')
```

### views.py
```python
from django.shortcuts import render, redirect
from .models import User, QuestionSection, AnswerSection
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.

def home(request):
	if 'user_name' in request.session:
		all_questions = QuestionSection.objects.all()
		data = {'questions': all_questions}
		return render(request, 'html_files/home.html', data)
	else:
		messages.warning(request, 'You have to login first.')
		return redirect('login')


def login(request):
	if 'user_name' not in request.session:
		if request.method == 'POST':
			mail = request.POST['email']
			pwd = request.POST['pwd']
			check_user = User.objects.filter(email=mail, pass_word=pwd)
			if check_user.exists():
				request.session['user_name'] = check_user[0].user_name
				return redirect('home')
			else:
				messages.warning(request, 'Wrong credentials.')
		return render(request, 'html_files/login.html')
	else:
		return redirect('home')


def signup(request):
	if request.method == 'POST':
		uname = request.POST['uname']
		mail = request.POST['mail']
		pwd = request.POST['pwd']
		gender = request.POST['gen']
		if (uname and mail and pwd and gender):
			create_user = User.objects.create(user_name=uname, email=mail, pass_word=pwd, gender=gender)
			create_user.save()
			messages.success(request, 'New user created successfully.')
		else:
			messages.warning(request, 'All the fields are compulsory.')
	return render(request, 'html_files/signup.html')


def log_out(request):
	del request.session['user_name']
	return redirect('login')



def create_post(request, question):
	if 'user_name' in request.session:
		question_of_answer = QuestionSection.objects.get(question=question)
		data = {"question": question_of_answer}
		return render(request, 'html_files/create_post.html', data)
	else:
		return redirect('login')


def save_answer(request, question):
	if request.method=='POST':
		get_answer = request.POST['answer']
		session_user = User.objects.get(user_name=request.session['user_name'])
		print(session_user)
		current_que = QuestionSection.objects.get(question=question)
		print(current_que)

		create_new_ans = AnswerSection.objects.create(user=session_user, answer=get_answer)
		create_new_ans.save()
		current_que.answer.add(create_new_ans)
		messages.success(request,'Your answer is successfully saved.')
		return redirect('home')

def ask_question(request):
	if 'user_name' in request.session:
		return render(request, 'html_files/ask_question.html')
	else:
		return redirect('login')

def save_question(request):
	if request.method=='POST':
		session_user = User.objects.get(user_name=request.session['user_name'])
		get_question = request.POST['askQuestion']
		print(get_question)
		new_question = QuestionSection.objects.create(user=session_user, question=get_question)
		new_question.save()
		return redirect('home')

def show_answers(request, question):
	if 'user_name' in request.session:
		question_to_answer = QuestionSection.objects.get(question=question)
		data = {'question_to_answer':question_to_answer}
		return render(request,'html_files/show_answers.html', data)
	else:
		return redirect('home')


def profile(request):
	if 'user_name' in request.session:
		get_session_user = User.objects.get(user_name=request.session['user_name'])
		user_questions = QuestionSection.objects.filter(user=get_session_user)
		user_answers = AnswerSection.objects.filter(user=get_session_user)
		data = {'user_questions': user_questions, 'user_answers': user_answers}
		return render(request, 'html_files/profile.html', data)
	else:
		return redirect('home')



def search_tool(request):
	search_item = request.GET['search_value']
	search_in_question = QuestionSection.objects.filter(question__contains = search_item)
	data = {'query': search_in_question}
	return render(request, 'html_files/search_tool.html', data)
```

### app's urls.py
```python
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
```

### project's urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
]
```

### base.html
```html
{% load static %}


<!doctype html>
<html lang="en">
<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
  <link rel="stylesheet" type="text/css" href="{% static 'css/my_css.css' %}">
  <script src="https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js" referrerpolicy="origin"></script>

  <title>{% block title %}{% endblock %}</title>
</head>
<body style="background-color: #222; color:white;">
	<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="{% url 'home' %}"><b>QnA</b></a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" aria-current="page" href="{% url 'home' %}">Home</a>
          </li>

          {% if not request.session.user_name%}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'login' %}">Login</a>
          </li>

          <li class="nav-item">
            <a class="nav-link" href="{% url 'signup' %}">Signup</a>
          </li>
          {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{% url 'ask_question' %}" >Ask a Question</a>
          </li>

          {% endif %}
          

          <li class="nav-item">
            <form class="d-flex" action="{% url 'search_tool' %}" method="get">
              <input class="form-control me-2" name="search_value" type="search" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
          </li>
          
        </ul>
        
        {% if request.session.user_name %}
        <!-- Example single danger button -->
        <div class="btn-group">
          <button type="button" class="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            {{request.session.user_name}}
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item" href="#">@{{request.session.user_name}}</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="{% url 'profile' %}">Profile</a></li>
            <li><a class="dropdown-item" href="{% url 'ask_question' %}">Ask a Question</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="{% url 'logout' %}">Logout</a></li>
          </ul>
        </div>
        {% endif %}

      </div>
    </div>
  </nav>
 
  {% if messages %}
    {% for message in messages %}
      <div class="alert alert-dismissible fade show alert-{{message.tags}}" role="alert">
      {{message}}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    {% endfor %}
  {% endif %}

  {% block body %}
  {% endblock %}

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

  <script type="text/javascript" src="{% static 'js/my_js.js' %}"></script>

  <script>
  tinymce.init({
    selector: '#tiny_textarea',
    height: "500",
  });

  </script>
</body>
</html>

```


### home.html
```html
{% extends 'html_files/base.html' %}

{% block title%}Home{% endblock %}

{% block body%}
<div class="container-fluid w-75 my-3">
	

	{% if questions %}
	{% for question in questions reversed %}
	<div class="alert alert-success" role="alert">

		<h4 class="alert-heading"><a href="{% url 'show_answers' question.question %}">{{question.question}}</a></h4>
		<small>by {{question.user.user_name}}, {{question.upload_date}} </small>
		<hr>
		<p>Total Answers - {{question.answer.count}}</p>
		{% if question.user.user_name != request.session.user_name %}
			<a href="{% url 'create_post' question.question %}">Write the answer</a>
		{% endif %}
		<hr>
	</div>
	{% endfor %}
	{% endif %}

	
</div>
{% endblock %}
```

### signup.html
```html
{% extends 'html_files/base.html' %}

{% block title %}Signup{% endblock %}

{% block body %}
<div class="container-fluid w-50 my-4 py-5" style="color: white;">
	<h3 style="text-align:center;">Signup</h3>
	<form action="{% url 'signup' %}" method="post">
		{% csrf_token %}
	<div class="mb-3">
		<label for="exampleFormControlInput1" class="form-label">Username</label>
		<input type="text" class="form-control" name="uname" id="exampleFormControlInput1" placeholder="eg. User name">
	</div>
	<div class="mb-3">
		<label for="exampleFormControlInput1" class="form-label">Email address</label>
		<input type="email" class="form-control" name="mail" id="exampleFormControlInput1" placeholder="eg. name@example.com">
	</div>
	<div class="mb-3">
		<label for="exampleFormControlTextarea1" class="form-label">Password</label>
		<input type="password" class="form-control" name="pwd" id="exampleFormControlInput1" placeholder="eg. Password">
	</div>
	<div class="mb-3">
		<label for="exampleFormControlInput1" class="form-label">Gender</label>
		<select class="form-control" name="gen">
			<option>Male</option>
			<option>Female</option>
			<option>Other</option>
		</select>
	</div>
	<div class="mb-3">
		<input type="submit" class="form-control btn btn-outline-success" id="exampleFormControlInput1" value="Signup">
	</div>
	</form>
</div>
{% endblock %}
```

### login.html
```html
{% extends 'html_files/base.html' %}

{% block title %}Login{% endblock %}

{% block body %}
<div class="container-fluid w-50 my-4 py-5" style="color: white;">
	<form action="{% url 'login' %}" method="post">
		{% csrf_token %}
	<h3 style="text-align:center;">Login</h3>
	<div class="mb-3">
		<label for="exampleFormControlInput1" class="form-label">Email address</label>
		<input type="email" class="form-control" name="email" id="exampleFormControlInput1" placeholder="eg. name@example.com">
	</div>
	<div class="mb-3">
		<label for="exampleFormControlTextarea1" class="form-label">Password</label>
		<input type="password" class="form-control" name="pwd" id="exampleFormControlInput1" placeholder="eg. Password">
	</div>

	<div class="mb-3">
		<input type="submit" class="form-control btn btn-outline-success" id="exampleFormControlInput1" value="Login">
	</div>
	</form>
</div>
{% endblock %}
```


### ask_question.html
```html
{% extends 'html_files/base.html' %}

{% block title %}{% endblock %}


{% block body %}
	<div class="container-fluid my-4 mx-5 w-50 justify-content-center">
		<h1>Ask your question:</h1>
		<form method="post" action="{% url 'save_question' %}">
			{% csrf_token %}
			<textarea class="form-control" name="askQuestion" placeholder="Write your Question..." cols="100" rows="10"></textarea>
			<br>
			<input type="submit" value="Submit" class="btn btn-primary">
		</form>
	</div>
	
	
{% endblock %}
```

### create_post.html
```html
{% extends 'html_files/base.html' %}

{% block title %}{{request.session.user_name}}|Posts|{% endblock %}



{% block body %}
	{# answer the question #}
	
	<div class="container-fluid w-75 my-4">
		<h3>{{question.question}}</h3>
		<hr>
		<form action="{% url 'save_answer' question.question %}" method="post">	
			{% csrf_token %}
			<textarea id="tiny_textarea" name="answer" placeholder="Write your answer here..."></textarea>
			<br>
			<input type="submit" value="Submit the answer" class="btn btn-primary">
		</form>
	</div>
	
{% endblock %}
```


### profile.html
```html
{% extends 'html_files/base.html' %}

{% block title %}{{request.session.user_name}} | Profile{% endblock %}



{% block body %}
	<h1 class="my-4">Hello {{request.session.user_name}} !</h1>
	
	{# all the Quetions of user are displayed here. #}
	<div class="alert alert-success w-50 mx-1 my-3" role="alert">
		<h2>Your Questions</h2>
		<hr>
		{% for question in user_questions %}
			<h4 class="alert-heading"><a href="{% url 'show_answers' question.question %}">{{question.question}}</a></h4>
			<small>{{question.upload_date}}</small>
			<hr>
		{% endfor %}
	</div>


	{# all the Answers of user are displayed here. #}
	<div class="alert alert-success mx-4 w-50 my-3" role="alert" style="position: absolute; top: 135px; right: -30px;">
		<h2>Your Answers</h2>
		<hr>
		{% for answer in user_answers %}
			<h6 class="alert-heading">{{answer.answer|safe}}</h6>
			<small>{{answer.upload_date}}</small>
			<hr>
		{% endfor %}
	</div>
	
{% endblock %}
```

### search_tool.html
```html
{% extends 'html_files/base.html' %}

{% block title %}{% endblock %}


{% block body %}
	
		{% if query %}
			{% for q in query reversed%}
			<div class="alert alert-success w-75 mx-5 my-3" role="alert">
				<h4 class="alert-heading text-danger"><a href="{% url 'show_answers' q.question %}">{{q.question}}</a></h4>
				<small>by {{q.user}} | {{q.upload_date}}</small>
			</div>
			{% endfor %}
		{% else %}
			<h3 class="text-center my-5">No search results found.</h3>
		{% endif %}
	

{% endblock %}
```

### show_answers.html
```html
{% extends 'html_files/base.html' %}

{% block title %}All answers{% endblock %}

{% block body %}

	<div class="alert alert-success w-75 mx-5 my-3" role="alert">
		<h4 class="alert-heading text-danger">{{question_to_answer}}</h4>
		<small>by {{question_to_answer.user.user_name}}</small>
		<hr>
		{% for answer in question_to_answer.answer.all reversed %}
			<p><b>{{answer.answer|safe}}</b></p>
			<small style="color: black;">by {{answer.user}}</small><br>
			<hr>
			<br>
		{% empty %}
			<h4>No answers yet...</h4>
			{% if question_to_answer.user.user_name != request.session.user_name %}
				<a href="{% url 'create_post' question_to_answer.question %}">Write a answer</a>
			{% endif %}
		{% endfor %}
	</div>

{% endblock %}
```

