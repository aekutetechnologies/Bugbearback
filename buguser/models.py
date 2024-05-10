from django.db import models

# Create your models here.


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserCreationMethod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, tc, user_type, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            tc=tc,
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, tc, password=None):
        """
        Creates and saves a superuser with the given email, name, tc and password.
        """
        user_type = UserType.objects.get(id=4)
        user = self.create_user(
            email,
            password=password,
            tc=tc,
            user_type=user_type,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#  Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    tc = models.BooleanField()
    user_type = models.ForeignKey(UserType, on_delete=models.DO_NOTHING, default=2)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_via = models.ForeignKey(
        UserCreationMethod, on_delete=models.DO_NOTHING, default=1
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["tc"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class BugUserDetail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/")
    gender = models.CharField(
        max_length=10,
        choices=(("Male", "Male"), ("Female", "Female")),
        default="Male",
        blank=False,
    )

    def __str__(self):
        return self.user.name


class BugBearSkill(models.Model):
    id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=50)
    skill_description = models.TextField()
    skill_logo = models.ImageField(upload_to="skill_logos/")

    def __str__(self):
        return self.skill_name


class BugUserSkill(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(BugBearSkill, on_delete=models.CASCADE)
    skill_level = models.CharField(
        max_length=20,
        choices=(
            ("Beginner", "Beginner"),
            ("Intermediate", "Intermediate"),
            ("Expert", "Expert"),
        ),
        default="Beginner",
        blank=False,
    )

    def __str__(self):
        return self.user.email


class CommunicationLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    language_name = models.CharField(max_length=50)

    def __str__(self):
        return self.language_name


class UsersCommunicationLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(CommunicationLanguage, on_delete=models.CASCADE)
    language_level = models.CharField(
        max_length=20,
        choices=(
            ("Beginner", "Beginner"),
            ("Intermediate", "Intermediate"),
            ("Expert", "Expert"),
        ),
        default="Beginner",
        blank=False,
    )


class BugUserSession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def CreateBugUserSessionToken(self):

        email = self.user.email

        return self.token


class BugOrganization(models.Model):
    id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=100)
    org_email = models.EmailField()
    org_password = models.CharField(max_length=50)

    def __str__(self):
        return self.org_name


class BugOrganizationDetail(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.OneToOneField(BugOrganization, on_delete=models.CASCADE)
    org_country = models.CharField(max_length=50)
    org_city = models.CharField(max_length=50)
    org_address = models.TextField()
    org_phone = models.CharField(max_length=15)
    org_profile_pic = models.ImageField(upload_to="org_profile_pics/")
    org_website = models.CharField(max_length=100)
    org_description = models.TextField()

    def __str__(self):
        return self.organization.org_name
