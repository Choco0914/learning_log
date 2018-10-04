from django import forms

from .models import Topic, Entry

<<<<<<< HEAD
class TopicForm(forms. ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        lavels = {'text' : ''}
=======
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
>>>>>>> 9d27cb3f7b1815aaf61ef9792ea2d650f6cad432

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
<<<<<<< HEAD
        labels = {'text' : ''}
        widgets = {'text' : forms.Textarea(attrs={'cols':80})}
=======
        labels = {'text':''}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}
>>>>>>> 9d27cb3f7b1815aaf61ef9792ea2d650f6cad432
