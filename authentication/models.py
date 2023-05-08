from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError('Email is required')
        user = self.model(username=username.lower(), email=email.lower())
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=254, verbose_name='Email')
    username = models.CharField(unique=True, max_length=16, verbose_name='Username')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='Last login')
    is_superuser = models.BooleanField(default=False, verbose_name='is superuser')
    is_staff = models.BooleanField(default=False, verbose_name='is staff')
    is_active = models.BooleanField(default=True, verbose_name='is active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['pk']
        db_table = 'api_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'