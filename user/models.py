from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from phonenumber_field.modelfields import PhoneNumberField

class PhoneManager(BaseUserManager):
    use_in_migrations = True

    def normalize_phone(self, phone):
     
        return phone.strip()

    def _create_user(self, phone, email, password=None, **extra_fields):
        
        if not phone:
            raise ValueError("Telefon raqami kiritilishi shart")
        email = self.normalize_email(email)
        phone = self.normalize_phone(phone)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser bo'lishi uchun is_staff=True bo'lishi kerak.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser bo'lishi uchun is_superuser=True bo'lishi kerak.")

        return self._create_user(phone, email, password, **extra_fields)



class User(AbstractUser):
    class UserAuthStatus(models.TextChoices):
        NEW = 'new', 'Yangi'
        APPROVED = 'approved', 'Tasdiqlangan'

    phone = PhoneNumberField(unique= True)
    username = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = PhoneManager()
    # app_user.username
    status = models.CharField(max_length=50,choices=UserAuthStatus.choices, default='new')

    code = models.CharField(max_length=4,null=True)
    expire_date = models.DateTimeField(null=True)


    def __str__(self) -> str:
        return f"{self.id}-{self.phone}"
