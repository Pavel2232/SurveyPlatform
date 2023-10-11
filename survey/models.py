from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.conf import settings


class Survey(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='surveys',
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=500,
        db_index=True,
        verbose_name='Название опроса'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание опроса'
    )

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.title


class Question(models.Model):
    surveys = models.ManyToManyField(
        Survey,
        related_name='questions',
        verbose_name='Опросы'
    )
    text_question = models.TextField(verbose_name='Текст вопроса')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text_question


class Answer(models.Model):
    questions = models.ManyToManyField(
        Question,
        related_name='answers',
        verbose_name='Вопросы'
    )
    answer = models.TextField(verbose_name='Ответ')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.answer


class LikeDislike(models.Model):
    LIKE = 'Like'
    DISLIKE = 'Dislike'
    NOTHING = 'Nothing'

    MARKS = [
        (LIKE, 'Нравится'),
        (DISLIKE, 'Не нравится'),
        (NOTHING, 'Нет отметки'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='marks',
        verbose_name='Пользователь'
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='marks',
        verbose_name='Опросы'
    )
    mark = models.CharField(
        max_length=7,
        choices=MARKS,
        db_index=True,
        verbose_name='Отметка',
        default=NOTHING
    )

    class Meta:
        verbose_name = 'Отметка'
        verbose_name_plural = 'Отметки'
        constraints = (UniqueConstraint(fields=['user', 'survey'], name='unique_mark'),)

    def __str__(self):
        return self.mark


class ViewingSurvey(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name='Опросы'
    )
    view = models.BooleanField(default=False, verbose_name='Просмотрено')

    class Meta:
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'
        constraints = (UniqueConstraint(fields=['user', 'survey'], name='unique_view'),)

    def __str__(self):
        return self.survey.title


class Alert(models.Model):
    LIKE = 'Like'
    DISLIKE = 'Dislike'
    VIEW = 'View'

    ALERT = [
        (LIKE, 'Нравится'),
        (DISLIKE, 'Не нравится'),
        (VIEW, 'Просмотрено',)
    ]

    text_alert = models.CharField(
        max_length=11,
        choices=ALERT,
        db_index=True,
        verbose_name='Уведомление'
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='alerts',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Уведломление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return self.text_alert
