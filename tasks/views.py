from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib import messages
import datetime
# Create your views here.

@login_required
def Tasklist(request):

    search = request.GET.get('search')
    filter = request.GET.get('filter')
    taskDoneRecently = Task.objects.filter(done='done', updated_at__gt=datetime.datetime.now()-datetime.timedelta(days=30), user=request.user).count()
    taskDone = Task.objects.filter(done='done', user=request.user).count()
    taskDoing = Task.objects.filter(done='doing', user=request.user).count()

    if search:
        tasks = Task.objects.filter(title__icontains=search, user=request.user)
    elif filter:
        tasks = Task.objects.filter(done=filter, user=request.user)
    else:
        # created_at, description, done, id, title, updated_at
        tasks_list = Task.objects.all().order_by('-id').filter(user=request.user)
        #PAGINAÇÃO
        paginator = Paginator(tasks_list, 10)
        
        page = request.GET.get('page')

        tasks = paginator.get_page(page)
        #PAGINAÇÃO
    return render(request, 'task/lista.html', {'tasks': tasks, 'taskrecently': taskDoneRecently, 'taskdoing': taskDoing ,'taskdone':taskDone})

@login_required
def NewTask(request):  # CRUD = C
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.user = request.user
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'task/newtask.html', {'form': form})

    form = TaskForm()
    return render(request, 'task/newtask.html', {'form': form})

@login_required
def TaskView(request, id):  # CRUD = R
    tasks = get_object_or_404(Task, pk=id)
    return render(request, 'task/task.html', {'task': tasks})

@login_required
def EditTask(request, id):  # CRUD = U
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)

    if (request.method == 'POST'):   
        form = TaskForm(request.POST, instance=task)

        if(form.is_valid()):
            task.save()
            return redirect('/')
        else:
            return
        return render(request, 'task/edittask.html', {'form':form, 'task':task})
    else:
        return render(request, 'task/edittask.html', {'form':form, 'task':task})

@login_required
def ChangeStatus(request, id):
    task = get_object_or_404(Task, pk=id)

    if(task.done == 'doing'):
        task.done = 'done'
    else:
        task.done = 'doing'

    task.save()

    return redirect('/')

@login_required
def DeleteTask(request, id): #CRUD = D
    task = get_object_or_404(Task, pk=id)
    task.delete()
    messages.info(request, 'Tarefa Deletada!')
    return redirect('/')