from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserForm, MyUserCreationForm, TaskForm
from .models import User, Task, Category, Subcategory, Offer, Message

# Create your views here.
def home(request):
    tasks_count = Task.objects.filter(is_done=True).all().count()
    context = {'tasks_count': tasks_count}
    return render(request, 'home.html', context)
    
@login_required(login_url='login')
def create(request):
    user = request.user
    form = TaskForm()
    if request.method == 'POST':
        category = Category.objects.get(id=request.POST.get('category'))
        subcategory = Subcategory.objects.get(id=request.POST.get('subcategory'))
        Task.objects.create(
            client=user,
            category=category,
            subcategory=subcategory,
            address=request.POST.get('address'),
            price=request.POST.get('price'),
            time=request.POST.get('time'),
            description=request.POST.get('description'),
        )
        return redirect('tasks')
    context = {'form': form}
    return render(request, 'create.html', context)

def offer(request, pk):
    offer = Offer.objects.get(id=pk)
    messages = offer.message_set.all()
    context = {'offer': offer, 'messages': messages}
    if request.method == 'POST':
        task = Task.objects.get(id=offer.task.id)
        task.executor = offer.master
        task.is_taken = True
        task.save()
        return redirect('tasks')
    return render(request, 'offer.html', context)

def makeoffer(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    error = None
    if Offer.objects.filter(master=request.user, task=task).all().count() > 0:
        error = 'error'
    print(Offer.objects.filter(master=request.user, task=task))
    context = {'task': task, 'form': form, 'error': error}
    if request.method == 'POST':
        offer = Offer.objects.create(master=request.user, task=task)
        message = Message.objects.create(user=request.user, offer=offer, text=request.POST.get('message'))
        return redirect('tasks')
    return render(request, 'makeoffer.html', context)

def main(request):
    return render(request, 'main.html')

def profile(request, pk):
    user = User.objects.get(id=pk)
    ended_tasks = Task.objects.filter(executor=user, is_done=True)
    active_tasks = Task.objects.filter(executor=user, is_done=False)
    my_tasks = Task.objects.filter(client=user, is_done=True)
    context = {'user': user, 'ended_tasks': ended_tasks, 'active_tasks': active_tasks, 'my_tasks': my_tasks}
    return render(request, 'profile.html', context)

def stuff(request):
    stuff = User.objects.all()
    context = {'stuff': stuff}
    return render(request, 'stuff.html', context)

def tasks(request):
    tasks = Task.objects.filter(is_taken=False, is_done=False).all().order_by('-created')
    context = {'tasks': tasks}
    return render(request, 'tasks.html', context)

def task(request, pk):
    task = Task.objects.get(id=pk)
    offers = task.offer_set.all()
    context = {'task': task, 'offers': offers}
    return render(request, 'task.html', context)

def become(request):
    return render(request, 'become_executor.html')

def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration!')
    return render(request, 'login_register.html', {'form': form})

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Пользователя с таким номером не существует')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            messages.error(request, "Номер телефона или пароль неверны!!!")
    context = {'page': page}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def loadList(request):
    template_name = 'category_list.html'
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id)
    return render(request,template_name,{'subcategories':subcategories, 'category_id': category_id})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    return render(request, 'update-user.html', {'form': form})