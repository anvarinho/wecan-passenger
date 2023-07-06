from django.contrib import admin
from .models import User, Task, Category, Subcategory, Offer, Message
# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Offer)
admin.site.register(Message)