from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('Users require an email field')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('user_type', 1)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

	groups = models.ManyToManyField(
		Group,
		related_name='custom_user_set',  # Change this to a unique name
		blank=True,
		help_text=_(
			'The groups this user belongs to. A user will get all permissions '
			'granted to each of their groups.'
		),
		related_query_name='custom_user'
	)
	user_permissions = models.ManyToManyField(
		Permission,
		related_name='custom_user_permissions',  # Change this to a unique name
		blank=True,
		help_text='Specific permissions for this user.',
		related_query_name='custom_user'
	)

	USER_TYPE_CHOICES = (
		(1, 'Administrador'),
		# (2, 'Sólo lectura'),
	)

	username = None
	email = models.EmailField(_('Email'), unique=True)
	phone = models.CharField('Teléfono', max_length=20, null=True, blank=True)
	position = models.CharField('Cargo', max_length=100, null=True, blank=True)
	user_type = models.PositiveSmallIntegerField('Tipo de usuario', choices=USER_TYPE_CHOICES)
	active = models.BooleanField(default=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
