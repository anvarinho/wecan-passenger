from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Task, Subcategory


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Номер телефона',
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','first_name','last_name', 'email', 'bio']
        labels = {
            'avatar': 'Фото',
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'bio': 'О себе'
        }

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['category', 'subcategory', 'address', 'time', 'price', 'description']
        labels = {
            'category': 'Выберите категорию вашей задачи',
            'subcategory': 'Выберите подкатегорию вашей задачи',
            'address': 'Введите ваш адрес',
            'time': 'Введите удобное время (по умолчанию в ближайшее время)',
            'price': 'Введите стоимость (по умолчанию договорная)',
            'description': 'Опишите подробно вашу задачу',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')