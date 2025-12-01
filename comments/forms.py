from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form used to create new comments.

    This ModelForm exposes only the `content` field to users,
    while the `user` and `profile` fields are set automatically
    in the view logic.

    Attributes:
        Meta:
            model (Comment): The model this form is based on.
            fields (list): The fields included in the form.
            widgets (dict): Custom widgets for rendering fields.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment…'
            })
        }
