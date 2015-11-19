import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, password=None, **kwargs):
        if not kwargs.get('email') and not kwargs.get('username'):
            raise ValueError('User must have a valid email.')
        elif not kwargs.get('email'):
            kwargs["email"] = kwargs.get('username') + "@" + "localhost.com"
        account = self.model(email=kwargs.get('email'))
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, password, **kwargs):
        account = self.create_user(password, **kwargs)
        account.is_active = True
        account.is_staff = True
        account.is_superuser = True
        account.save()
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, blank=True, default="key")
    key_expires = models.DateTimeField(default=datetime.date.today)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = AccountManager()

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
