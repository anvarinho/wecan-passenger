from django.db import models
from django.utils import timesince
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200)
    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length = 200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(verbose_name="номер телефона", unique=True, max_length=17, null=True)
    bio = models.TextField(default='')
    avatar = models.ImageField(null=True, default='avatar.png', upload_to="static/avatars")
    is_master = models.BooleanField(default=False)
    crafts = models.ManyToManyField(Category, blank=True, related_name='crafts', default=None)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']
    @property
    def name(self):
        return str(self.first_name) + " " + str(self.last_name[0])
    @property
    def registered(self):
        return timesince.timesince(self.created).split(',')[0]
    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

def create_superuser(self, email, full_name, profile_picture, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not full_name:
            raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.full_name = full_name
        user.set_password(password)
        user.profile_picture = profile_picture
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user

class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    description = models.TextField()
    address = models.CharField(max_length = 100, default="",blank=True)
    price = models.CharField(max_length = 20, default="Договорная")
    time = models.CharField(max_length = 100, default="В ближайшее время")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client")
    executor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="executor", null=True, blank=True)
    is_taken = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    @property
    def offers(self):
        self.offer_set.all()
    @property
    def timesince(self):
        return timesince.timesince(self.created).split(',')[0]
    def __str__(self):
        return self.subcategory.name + " " + self.timesince + " назад."

class Offer(models.Model):
    master = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    @property
    def timesince(self):
        return timesince.timesince(self.created).split(',')[0]
    def __str__(self):
        return str(self.task.subcategory) + " " + str(self.master.name)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    text = models.CharField(max_length = 200)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text