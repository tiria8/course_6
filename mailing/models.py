from django.db import models

from config import settings


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):

    client_email = models.EmailField(unique=True, verbose_name='почта')
    client_first_name = models.CharField(max_length=150, verbose_name='имя')
    client_last_name = models.CharField(max_length=150, verbose_name='фамилия')
    client_comment = models.CharField(max_length=150, verbose_name='комментарий')
    client_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     verbose_name='владелец', **NULLABLE)

    def __str__(self):

        return f'{self.client_email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('client_email',)


class Message(models.Model):

    message_title = models.CharField(max_length=150, verbose_name='тема')
    message_text = models.TextField(verbose_name='содержание')
    message_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      verbose_name='владелец', **NULLABLE)

    def __str__(self):

        return f'{self.message_title}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('id',)


class Mailing(models.Model):

    PERIOD_DAILY = 'ежедневно'
    PERIOD_WEEKLY = 'еженедельно'
    PERIOD_MONTHLY = 'ежемесячно'

    PERIOD_CHOICES = (
        (PERIOD_DAILY, 'ежедневно'),
        (PERIOD_WEEKLY, 'еженедельно'),
        (PERIOD_MONTHLY, 'ежемесячно')
    )

    STATUS_CREATED = 'создано'
    STATUS_SENT = 'рассылается'
    STATUS_STOPPED = 'остановлено'

    STATUS_CHOICES = (
        (STATUS_CREATED, 'создано'),
        (STATUS_SENT, 'рассылается'),
        (STATUS_STOPPED, 'остановлено')
    )

    mailing_title = models.CharField(max_length=150, verbose_name='заголовок')
    mailing_time_start = models.DateTimeField(verbose_name='начало рассылки')
    mailing_time_finish = models.DateTimeField(verbose_name='окончание рассылки')
    mailing_period = models.CharField(max_length=20, choices=PERIOD_CHOICES, verbose_name='периодичность')
    mailing_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name='статус')
    mailing_message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    mailing_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      verbose_name='владелец', **NULLABLE)
    mailing_clients = models.ManyToManyField(Client, verbose_name='клиенты')

    def __str__(self):

        return f'{self.mailing_title}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('id',)


class Log(models.Model):

    STATUS_TRUE = 'отправлено'
    STATUS_FALSE = 'не отправлено'

    STATUS_CHOICES = (
        (STATUS_TRUE, 'отправлено'),
        (STATUS_FALSE, 'не отправлено')
    )

    log_date_time = models.DateTimeField(verbose_name='дата-время')
    log_status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус')
    log_server_answer = models.TextField(verbose_name='ответ сервера')
    log_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    log_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент', **NULLABLE)

    def __str__(self):
        return f'{self.log_date_time} - {self.log_status}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ('log_date_time',)
