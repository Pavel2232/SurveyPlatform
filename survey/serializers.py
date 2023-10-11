from django.db import transaction
from rest_framework import serializers
from survey.models import Survey, Question, Answer, LikeDislike, Alert


class CreateSurveySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Survey
        fields = '__all__'

    def is_valid(self, raise_exception=True):
        self._questions = self.initial_data.pop('questions')
        self._answers = self.initial_data.pop('answers')
        return super().is_valid(raise_exception=raise_exception)

    @transaction.atomic
    def create(self, validated_data):
        survey = Survey.objects.create(**validated_data)
        for question in self._questions:
            question_obj, _ = Question.objects.get_or_create(text_question=question)
            survey.questions.add(question_obj)

        for answer in self._answers:
            answer_obj, _ = Answer.objects.get_or_create(answer=answer)
            survey.questions.get(surveys__questions__surveys=survey).answers.add(answer_obj)

        return survey


class SurveySerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    questions = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    dislike = serializers.SerializerMethodField()
    view = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ['title', 'user', 'questions', 'answer', 'like', 'dislike', 'view']



    def get_questions(self, survey: Survey):
        return survey.questions.values('text_question')

    def get_answer(self, survey: Survey):
        return survey.questions.values_list('answers__answer')

    def get_like(self, survey: Survey):
        return survey.marks.filter(mark__exact='Like').values('mark').count()

    def get_dislike(self, survey: Survey):
        return survey.marks.filter(mark__exact='Dislike').values('mark').count()

    def get_view(self, survey: Survey):
        return survey.views.filter(view=True).count()

    def is_valid(self, raise_exception=False):
        if self.initial_data.get('questions'):
            self._questions = self.initial_data.pop('questions')
        return super().is_valid(raise_exception=raise_exception)

    def update(self, survey: Survey, validated_data):
        questions = []
        if self._questions:
            for question in self._questions:
                question_obj, _ = Question.objects.get_or_create(text_question=question.get('text_question'))
                questions.append(question_obj)
        survey.questions.set(questions)

        survey.save()
        return super().update(survey, validated_data)


class CreateQuestionSerializer(serializers.ModelSerializer):
    surveys = serializers.SlugRelatedField(queryset=Survey.objects.all(), many=True, slug_field='id')
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def is_valid(self, raise_exception=True):
        self._answers = self.initial_data.pop('answers')
        return super().is_valid(raise_exception=raise_exception)

    @transaction.atomic
    def create(self, validated_data):
        survey = validated_data.pop('surveys')
        question_obj, _ = Question.objects.get_or_create(text_question=validated_data.get('text_question'))

        question_obj.surveys.set(survey)
        for answer in self._answers:
            answer_obj, _ = Answer.objects.get_or_create(answer=answer)
            question_obj.answers.add(answer_obj)

        return question_obj

    def get_answer(self, question: Question):
        return question.answers.values_list('answer')


class QuestionSerializers(serializers.ModelSerializer):
    surveys = serializers.SlugRelatedField(queryset=Survey.objects.all(), slug_field='title', many=True)
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['surveys', 'text_question', 'answer', 'id']

    def get_answer(self, question: Question):
        return question.answers.values_list('answer')

    def is_valid(self, raise_exception=False):
        if self.initial_data.get('answers'):
            self._answres = self.initial_data.pop('answers')
        return super().is_valid(raise_exception=raise_exception)

    def update(self, question: Question, validated_data):
        answers = []
        if self._answres:
            for answer in self._answres:
                answer_obj, _ = Answer.objects.get_or_create(answer=answer)
                answers.append(answer_obj)
        question.answers.set(answers)

        question.save()
        return super().update(question, validated_data)


class MakeMarkSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    survey = serializers.SlugRelatedField(queryset=Survey.objects.all(), slug_field='title')

    class Meta:
        model = LikeDislike
        fields = '__all__'

    def create(self, validated_data):
        if not validated_data.get('mark'):
            validated_data['mark'] = 'Nothing'
        mark_obj, create = LikeDislike.objects.get_or_create(user=validated_data.get('user'),
                                                             survey=validated_data.get('survey'))
        if not create:
            mark_obj.mark = validated_data.get('mark')
            return mark_obj

        mark_obj.mark = validated_data.get('mark')

        if mark_obj.mark == mark_obj.LIKE:
            Alert.objects.create(text_alert='Like', user_to=mark_obj.survey.user)

        if mark_obj.mark == mark_obj.DISLIKE:
            Alert.objects.create(text_alert='Dislike', user_to=mark_obj.survey.user)
        return mark_obj


class AlertSerializer(serializers.ModelSerializer):
    user_to = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Alert
        fields = '__all__'
