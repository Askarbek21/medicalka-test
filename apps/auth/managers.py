from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(
        self,
        email,
        username,
        full_name,
        password,
        is_verified=False,
        **extra_fields,
    ):
        if not email:
            raise ValueError('Почта должна быть указана.')

        if not username:
            raise ValueError('Имя пользователя должно быть указано.')

        if not password:
            raise ValueError('Пароль должен быть указан.')

        if not full_name:
            raise ValueError('Полное имя должно быть указано.')

        email = self.normalize_email(email)

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(
            email=email,
            username=username,
            full_name=full_name,
            is_verified=is_verified,
            **extra_fields,
        )

        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)

        return user


    def create_superuser(
        self,
        email,
        username,
        full_name,
        password,
        **extra_fields,
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('verification_token', None)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(
            email=email,
            username=username,
            full_name=full_name,
            password=password,
            **extra_fields,
        )
