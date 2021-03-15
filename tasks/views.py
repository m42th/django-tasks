from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm
from django.contrib import messages
# Create your views here.

def Tasklist(request):

    search = request.GET.get('search')
    if search:
        tasks = Task.objects.filter(title__icontains=search)
    else:
        # created_at, description, done, id, title, updated_at
        tasks_list = Task.objects.all().order_by('-id')
        #PAGINAÇÃO
        paginator = Paginator(tasks_list, 3)
        
        page = request.GET.get('page')

        tasks = paginator.get_page(page)
        #PAGINAÇÃO
    return render(request, 'task/lista.html', {'tasks': tasks})

def NewTask(request):  # CRUD = C
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'Doing'
            task.save()
            return redirect('/task/')
    else:
        form = TaskForm()
        return render(request, 'task/newtask.html', {'form': form})

    form = TaskForm()
    return render(request, 'task/newtask.html', {'form': form})

def TaskView(request, id):  # CRUD = R
    tasks = get_object_or_404(Task, pk=id)
    return render(request, 'task/task.html', {'task': tasks})

def EditTask(request, id):  # CRUD = U
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)

    if (request.method == 'POST'):   
        form = TaskForm(request.POST, instance=task)

        if(form.is_valid()):
            task.save()
            return redirect('/task/')
        else:
            return
        return render(request, 'task/edittask.html', {'form':form, 'task':task})
    else:
        return render(request, 'task/edittask.html', {'form':form, 'task':task})

def DeleteTask(request, id): #CRUD = D
    task = get_object_or_404(Task, pk=id)
    task.delete()
    messages.info(request, 'Tarefa Deletada!')
    return redirect('/task/')