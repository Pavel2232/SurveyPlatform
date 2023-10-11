from django.db.models import Count
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from survey.models import Survey, ViewingSurvey, Question, LikeDislike, Alert
from survey.serializers import CreateSurveySerializer, SurveySerializers, CreateQuestionSerializer, QuestionSerializers, \
    MakeMarkSerializer, AlertSerializer


class CreateSurveyView(CreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = CreateSurveySerializer
    permission_classes = [IsAuthenticated, ]


class ListSurveySerializerView(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializers
    permission_classes = [IsAuthenticated, ]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['title']
    ordering_fields = ['like']

    def get_queryset(self):
        return self.queryset.annotate(like=Count('marks', mark__exact='Like'))


class RetrieveSurveyView(RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializers
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        obj, create = ViewingSurvey.objects.get_or_create(survey=self.get_object(), user=request.user, view=True)
        if create:
            Alert.objects.create(text_alert='View', user_to=self.get_object().user)
        return self.retrieve(request, *args, **kwargs)


class CreateQuestionView(CreateAPIView):
    queryset = Question
    serializer_class = CreateQuestionSerializer
    permission_classes = [IsAuthenticated, ]


class ListQuestionView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializers
    permission_classes = [IsAuthenticated, ]


class RetrieveQuestionView(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializers
    permission_classes = [IsAuthenticated, ]


class ListNotViewedSurvey(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializers
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset.exclude(views__user=self.request.user, views__view=True)


class LikeDislikeView(CreateAPIView):
    queryset = LikeDislike.objects.all()
    serializer_class = MakeMarkSerializer
    permission_classes = [IsAuthenticated, ]


class ListAlertView(ListAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset.filter(user_to=self.request.user)
