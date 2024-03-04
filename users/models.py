from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Email', blank=False,
                              null=False)
    groups = models.ManyToManyField('auth.Group', related_name='myuser_set',
                                    blank=True)
    user_permissions = models.ManyToManyField('auth.Permission',related_name='myuser_set',
                                              blank=True)
    username = models.CharField(max_length=150, unique=True,
                                verbose_name='Login', blank=False,
                                null=False)
    first_name = models.CharField(max_length=150, blank=False,
                                  verbose_name='First name', null=False,)
    last_name = models.CharField(max_length=150,blank=False,
                                 verbose_name='Last name', null=False)

    REQUIRED_FIELDS = (
        'email', 'first_name', 'last_name', 'password',
    )

