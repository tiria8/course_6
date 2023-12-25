from django import forms

from mailing.models import Mailing, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_current_version":
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mailing_clients'].queryset = Client.objects.filter(client_owner=user)

        self.fields['mailing_message'].queryset = Message.objects.filter(message_owner=user)

    class Meta:
        model = Mailing

        exclude = ('mailing_log', 'mailing_owner')
        widgets = {
            'mailing_time_start': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'mailing_time_finish': forms.DateTimeInput(
                attrs={'type': 'datetime-local'})
        }


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client

        exclude = ('client_owner',)


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message

        exclude = ('message_owner',)
