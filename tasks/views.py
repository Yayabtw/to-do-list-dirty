from django.conf import settings
from django.shortcuts import redirect, render

from .forms import TaskForm
from .models import Task


def index(request):
    """View for listing all tasks."""
    tasks = Task.objects.all().order_by('-priority', 'created')
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # adds to the database if valid
            form.save()
        return redirect('/')

    context = {'tasks': tasks, 'form': form, 'version': settings.VERSION}
    return render(request, 'tasks/list.html', context)


def update_task(request, pk):
    """View for updating a task."""
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'tasks/update_task.html', context)


def delete_task(request, pk):
    """View for deleting a task."""
    item = Task.objects.get(id=pk)

    if request.method == "POST":
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'tasks/delete.html', context)
