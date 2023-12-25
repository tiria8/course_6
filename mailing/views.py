import datetime
from random import sample

import pytz
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from blog.models import Blog
from mailing.forms import MailingForm, ClientForm, MessageForm
from mailing.models import Mailing, Client, Message, Log
from mailing.services import sending_email


class MailingListView(ListView):

    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self, *args, **kwargs):

        queryset = super().get_queryset(*args, **kwargs)

        try:
            user = self.request.user

            if user.is_superuser or user.groups.filter(name='manager'):
                return queryset

            else:
                queryset = queryset.filter(mailing_owner=user)
                return queryset

        except TypeError:
            pass

    def get_context_data(self, **kwargs):

        context = super(MailingListView, self).get_context_data(**kwargs)

        context['title'] = 'Рассылки'
        context['title_2'] = 'мои рассылки'
        context['title_3'] = ('(Перед созданием рассылки необходимо занести клиента и создать сообщение. '
                              'Кнопка отправить рассылки сейчас позволяет запустить рассылки вне расписания)')

        return context


class MailingCreateView(LoginRequiredMixin, CreateView):

    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):

        user = self.request.user
        self.object = form.save()
        self.object.mailing_owner = user
        self.object.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDetailView(DetailView):

    model = Mailing

    def get_context_data(self, **kwargs):

        context = super(MailingDetailView, self).get_context_data(**kwargs)

        context['title'] = 'Рассылки'
        context['title_2'] = 'информация о рассылке'

        return context


class MailingUpdateView(UpdateView):

    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):

        self.object = form.save()
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(MailingUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Рассылки'
        context['title_2'] = 'Редактирование рассылки'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDeleteView(DeleteView):

    model = Mailing

    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):

        context = super(MailingDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Рассылки'
        context['title_2'] = 'Удаление рассылки'
        return context


class ClientListView(ListView):

    model = Client
    template_name = 'mailing/client_list.html'

    def get_queryset(self, *args, **kwargs):

        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(client_owner=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):

        context = super(ClientListView, self).get_context_data(**kwargs)

        context['title'] = 'Клиенты'
        context['title_2'] = 'мои клиенты для рассылок'

        return context


class ClientCreateView(LoginRequiredMixin, CreateView):

    model = Client
    form_class = ClientForm

    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):

        self.object = form.save()
        self.object.client_owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(ClientCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Клиенты'
        context['title_2'] = 'Создание клиента'
        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):

    model = Client
    form_class = ClientForm

    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):

        self.object = form.save()
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Клиенты'
        context['title_2'] = 'Редактирование клиента'
        return context


class ClientDeleteView(DeleteView):

    model = Client

    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, **kwargs):

        context = super(ClientDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Клиенты'
        context['title_2'] = 'Удаление клиента'
        return context


class MessageListView(LoginRequiredMixin, ListView):

    model = Message
    template_name = 'mailing/message_list.html'

    def get_queryset(self, *args, **kwargs):

        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(message_owner=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):

        context = super(MessageListView, self).get_context_data(**kwargs)

        context['title'] = 'Сообщения'
        context['title_2'] = 'мои сообщения для рассылок'

        return context


class MessageCreateView(LoginRequiredMixin, CreateView):

    model = Message
    form_class = MessageForm

    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):

        self.object = form.save()
        self.object.message_owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(MessageCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        context['title_2'] = 'Создание сообщения'
        return context


class MessageUpdateView(LoginRequiredMixin, UpdateView):

    model = Message
    form_class = MessageForm

    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):

        self.object = form.save()
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(MessageUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        context['title_2'] = 'Редактирование сообщения'
        return context


class MessageDeleteView(LoginRequiredMixin, DeleteView):

    model = Message

    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, **kwargs):

        context = super(MessageDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        context['title_2'] = 'Удаление сообщения'
        return context


def send_mailing_to_clients(request):

    date_time_now = datetime.datetime.now()
    user = request.user
    mailings = Mailing.objects.filter(mailing_owner=user)

    desired_timezone = pytz.timezone('Europe/Moscow')

    for mailing in mailings:
        time_start = mailing.mailing_time_start.astimezone(desired_timezone)
        time_now = date_time_now.astimezone(desired_timezone)
        time_finish = mailing.mailing_time_finish.astimezone(desired_timezone)

        if mailing.mailing_status == 'рассылается':

            if time_start < time_now < time_finish:

                for client in mailing.mailing_clients.all():

                    sending_email(mailing, client)
            elif time_now > time_finish:
                mailing.mailing_status = mailing.STATUS_STOPPED
                mailing.save()

    return redirect(reverse('mailing:mailing_list'))


def mailing_logs(request, pk):

    mailing = get_object_or_404(Mailing, pk=pk)

    if settings.CACHE_ENABLED:
        key = 'logs_list'
        logs = cache.get(key)

        if logs is None:
            logs = Log.objects.filter(log_mailing=mailing).order_by('-log_date_time')[:10]

            cache.set(key, logs)

    else:
        logs = Log.objects.filter(log_mailing=mailing).order_by('-log_date_time')[:10]

    if (mailing.mailing_owner == request.user or request.user.is_superuser
            or request.user.groups.filter(name='manager').exists()):
        context = {
            'title': 'Логи',
            'title_2': 'логи ваших рассылок',
            'title_3': '(выводится список из 10 последних логов рассылки)',
            'logs': logs,
        }
        return render(request, 'mailing/log_list.html', context)
    else:
        return redirect("mailing:mailing_list")


def main_page_view(request):

    blogs = Blog.objects.filter(blog_is_active=True)
    if len(blogs) >= 3:
        blog_list = sample(list(blogs), 3)
    else:
        blog_list = blogs

    mailings_count = Mailing.objects.count()

    mailings_is_sending = Mailing.objects.filter(mailing_status='рассылается').count()

    clients_count = Client.objects.count()

    context = {
        'title': 'Главная',
        'title_2': 'сервис создания рассылок',
        'blog_list': blog_list,
        'mailings_count': mailings_count,
        'mailings_is_sending': mailings_is_sending,
        'clients_count': clients_count
    }
    return render(request, 'mailing/base.html', context)