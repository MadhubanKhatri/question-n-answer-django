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