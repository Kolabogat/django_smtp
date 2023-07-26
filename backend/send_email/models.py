from django.db.models import Model, BooleanField, ForeignKey, PROTECT
from django.contrib.auth import get_user_model

User = get_user_model()


class Contact(Model):
    class Meta:
        verbose_name = 'User Contact'
        verbose_name_plural = 'Users Contacts'
        ordering = ['user']

    user = ForeignKey(to=User, verbose_name='User', on_delete=PROTECT, related_name='user_contact')

    subscribed_mail = BooleanField(max_length=50, help_text='I want to receive mails.', default=False)

    def __str__(self):
        return self.user
