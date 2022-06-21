from django.contrib.auth.models import BaseUserManager
import random


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, username=None):
        if not username:
            username = str(random.randint(100000000, 999999999999))
        if not phone_number:
            raise ValueError('user must have phone_number')
        user = self.model(username=username, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, phone_number, password, email, username=None):
        if not email:
            raise ValueError('admin must have email address.')
        user = self.create_user(phone_number, password, username)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, email, username=None):
        if not email:
            raise ValueError('superuser must have email address.')
        user = self.create_user(phone_number, password, username)
        user.email = email
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
