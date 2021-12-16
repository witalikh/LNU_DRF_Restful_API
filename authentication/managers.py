from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise TypeError('The email must be set')

        if not password:
            raise TypeError('The password must be given')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(email, password, **extra_fields)
        user.role = 0
        user.is_superuser = True

        user.save()
        return user
