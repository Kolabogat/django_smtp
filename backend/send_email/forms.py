from django.forms import Form, CharField, TextInput, Textarea, EmailField


class SendEmailForm(Form):
    title = CharField(
        label='Title', min_length=4, max_length=80, widget=TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Title', 'id': 'form-title'}
        )
    )
    message = CharField(
        label='Message', widget=Textarea(attrs={'class': 'form-control', 'rows': '5'})
    )


class SendReviewForm(Form):
    title = CharField(
        label='Title', min_length=4, max_length=80, widget=TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Title', 'id': 'form-title'}
        )
    )
    email = EmailField(
        max_length=100, widget=TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'E-mail', 'id': 'form-email'}
        )
    )
    message = CharField(
        label='Message', widget=Textarea(attrs={'class': 'form-control', 'rows': '5'})
    )
