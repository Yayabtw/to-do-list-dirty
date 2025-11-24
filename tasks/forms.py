from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    """Form for creating and updating tasks."""

    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add new task'})
    )

    class Meta:
        model = Task
        fields = '__all__'
