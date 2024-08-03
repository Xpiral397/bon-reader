from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, gender, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, gender= gender, first_name=first_name, last_name=last_name, password= password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, gender, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password=password, username=username,email=email,  gender= gender, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    gender = models.CharField(max_length=7, choices=(('Male',"male"),('Female',"female")))
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    activation_code = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name', 'password','gender']

    def __str__(self):
        return self.email