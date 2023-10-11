from django.urls import path

from survey.views import CreateSurveyView, ListSurveySerializerView, RetrieveSurveyView, CreateQuestionView, \
    ListQuestionView, RetrieveQuestionView, ListNotViewedSurvey, LikeDislikeView, ListAlertView

urlpatterns = [
    path('create/', CreateSurveyView.as_view(), name='survey-create'),
    path('list/', ListSurveySerializerView.as_view(), name='survey-list'),
    path('<int:pk>', RetrieveSurveyView.as_view(), name='survey-detail'),

    path('question/create/', CreateQuestionView.as_view(), name='question-create'),
    path('question/list/', ListQuestionView.as_view(), name='question-list'),
    path('question/<int:pk>/', RetrieveQuestionView.as_view(), name='question-detail'),



    path('user/not_viewed/', ListNotViewedSurvey.as_view(), name='user-new-survey'),
    path('like/', LikeDislikeView.as_view(), name='like'),
    path('alerts/', ListAlertView.as_view(), name='alert'),
]
