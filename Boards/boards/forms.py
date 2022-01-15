# django
from django import forms


class NewTopicForm(forms.Form):
    """New Topic Form"""
    subject = forms.CharField(max_length=255)
    message = forms.CharField(
        max_length=4000,
        widget=forms.Textarea(),
        help_text='The max length of the text is 4000'
    )
