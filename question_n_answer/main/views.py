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