import logging
import datetime
from datetime import timezone
import pytz

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from adv_app.models import Adv
from django.contrib.auth.models import User

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)

# отправление раз в неделю пользователям писем с ссылками на популярные объявления:
def my_job():
    today = datetime.datetime.now(timezone.utc)
    day_week_ago = today - datetime.timedelta(days=7)
    advs = Adv.objects.filter(date_adv__gte=day_week_ago)
    all_advs = []
    for i in advs:
        if i.adv_popular is True:
            all_advs.append(i)
    mail_list = set(advs.values_list("author__email", flat=True))

    html_content = render_to_string(
        'week_advs.html',
        {
            'link': f'http://127.0.0.1:8000',
            'all_advs':all_advs,
        }
    )
    msg = EmailMultiAlternatives(
        subject="Популярное за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=mail_list,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="wed", hour="00", minute="40"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="10"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")