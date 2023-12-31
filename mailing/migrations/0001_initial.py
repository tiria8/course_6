# Generated by Django 4.2.8 on 2023-12-25 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_email', models.EmailField(max_length=254, unique=True, verbose_name='почта')),
                ('client_first_name', models.CharField(max_length=150, verbose_name='имя')),
                ('client_last_name', models.CharField(max_length=150, verbose_name='фамилия')),
                ('client_comment', models.CharField(max_length=150, verbose_name='комментарий')),
                ('client_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ('client_email',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_title', models.CharField(max_length=150, verbose_name='тема')),
                ('message_text', models.TextField(verbose_name='содержание')),
                ('message_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_title', models.CharField(max_length=150, verbose_name='заголовок')),
                ('mailing_time_start', models.DateTimeField(verbose_name='начало рассылки')),
                ('mailing_time_finish', models.DateTimeField(verbose_name='окончание рассылки')),
                ('mailing_period', models.CharField(choices=[('ежедневно', 'ежедневно'), ('еженедельно', 'еженедельно'), ('ежемесячно', 'ежемесячно')], max_length=20, verbose_name='периодичность')),
                ('mailing_status', models.CharField(choices=[('создано', 'создано'), ('рассылается', 'рассылается'), ('остановлено', 'остановлено')], default='создано', max_length=20, verbose_name='статус')),
                ('mailing_clients', models.ManyToManyField(to='mailing.client', verbose_name='клиенты')),
                ('mailing_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='сообщение')),
                ('mailing_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_date_time', models.DateTimeField(verbose_name='дата-время')),
                ('log_status', models.CharField(choices=[('отправлено', 'отправлено'), ('не отправлено', 'не отправлено')], max_length=20, verbose_name='Статус')),
                ('log_server_answer', models.TextField(verbose_name='ответ сервера')),
                ('log_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.client', verbose_name='клиент')),
                ('log_mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
                'ordering': ('log_date_time',),
            },
        ),
    ]
