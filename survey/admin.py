from django.contrib import admin
from survey.models import Survey, Question, Answer, ViewingSurvey, LikeDislike, Alert

admin.site.register(Alert)
admin.site.register(Answer)
admin.site.register(ViewingSurvey)
admin.site.register(LikeDislike)


class AnswerInline(admin.TabularInline):
    model = Answer.questions.through
    extra = 1


class QuestionsInline(admin.TabularInline):
    model = Question.surveys.through
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline
    ]


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    inlines = [
        QuestionsInline,
    ]

# Register your models here.
