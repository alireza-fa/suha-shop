from django import forms
from django.utils.translation import gettext_lazy as _


class CommentForm(forms.Form):
    star = forms.IntegerField()
    body = forms.CharField(
        widget=forms.Textarea(attrs={"class": 'form-control mb-3', "id": 'body', "name": 'comment', "cols": '30', "rows": '10',
                                     "data-max-length": '200', "placeholder": _('Write your overview...')}),
    )
