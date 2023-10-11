from django.contrib.auth.models import (
    BaseUserManager
)


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.is_active = True

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email=None, password=None):

        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
