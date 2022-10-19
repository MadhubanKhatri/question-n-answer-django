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



