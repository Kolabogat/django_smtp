from django.forms import Form, CharField, TextInput, Textarea


class SendEmailForm(Form):
    title = CharField(
        label='Title', min_length=4, max_length=80, widget=TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Title', 'id': 'form-title'}
        )
    )
    message = CharField(
        label='Message', widget=Textarea(attrs={'class': 'form-control', 'rows': '5'})
    )
