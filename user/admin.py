from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from user.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords dont match')
        return password2

    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email',)
    search_fields = ('username', 'email',)
    readonly_fields = ('last_login', 'date_joined')
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username',)}),
        (
            'Personal Info',
            {'fields': ('email',)}
        ),
        (
            'Permission',
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (
            'Important dates',
            {'fields': ('last_login', 'date_joined')}
        )
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'email',),
            },
        ),
    )


admin.site.unregister(Group)
