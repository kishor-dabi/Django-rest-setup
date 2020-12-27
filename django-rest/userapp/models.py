from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# from django_rest.userrole.models import UserRole

# ----------------------------------------------- send email code

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

# -----------------------------------------------send email end code


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            email=self.normalize_email(email),

        )
        # user.first_name = first_name
        # user.last_name = last_name
        # user.age = age
        # user.phone_number = phone_number
        # user.gender = gender
        user.set_password(password)
        print(user, "------------------")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class UserRole(models.Model):
    role_name = models.CharField(max_length=100)
    permission = models.TextField()
    # = models.ForeignKey(PermissionGroup, on_delete=models.CASCADE, related_name='permission_set')
    class Meta:
        """
        to set table name in database
        """
        db_table = "user_role"


class User(AbstractBaseUser, PermissionsMixin):

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    is_active = models.BooleanField(default=True)
    user_type = models.OneToOneField('UserType', null=True, on_delete=models.CASCADE, related_name='profile')

    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, null=True, unique=False)
    last_name = models.CharField(max_length=50, null=True, unique=False)
    phone_number = models.CharField(max_length=10, unique=True, null=True, blank=False)
    age = models.PositiveIntegerField(null=True, blank=False)
    role = models.OneToOneField(UserRole, on_delete=models.CASCADE, null=True, related_name='role')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)


    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.email

    # class Meta:
    #     """
    #     to set table name in database
    #     """
    #     # db_table = "login"


# class UserProfile(models.Model):
#
#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     first_name = models.CharField(max_length=50, unique=False)
#     last_name = models.CharField(max_length=50, unique=False)
#     phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
#     age = models.PositiveIntegerField(null=False, blank=False)
#     role = models.OneToOneField(UserRole, on_delete=models.CASCADE, null=True, related_name='role')
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#
#     class Meta:
#         """
#         to set table name in database
#         """
#         db_table = "profile"


class Car(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    publisher = models.CharField(max_length=400)
    release_date = models.DateField()
    parts = models.ManyToManyField('Part', related_name='parts', blank=True)


class Part(models.Model):
    name = models.CharField(max_length=225)
    description = models.CharField(max_length=400)
    # date_of_birth = models.DateField()
    cars = models.ManyToManyField('Car', related_name='cars', blank=True)


class DoctorType(models.Model):

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225)


class UserType(models.Model):

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225)

class Doctor(models.Model):

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225)
    contact_number = models.CharField(max_length=10)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    is_active = models.BooleanField(default=True)
    doctor_type = models.OneToOneField(DoctorType, on_delete=models.CASCADE, related_name='doctor_type')
