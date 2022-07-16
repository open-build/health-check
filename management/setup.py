# management/commands/setup.py
from crontab import CronTab
from django.core.management import BaseCommand

class Command(BaseCommand):
    cron = CronTab(tabfile='/etc/crontabs/root', user=True)
    cron.remove_all()

    for command, schedule in settings.CRON_JOBS.items():
        job = cron.new(command='cd /usr/src/app && python3 manage.py {}'.format(command), comment=command)
        job.setall(schedule)
        job.enable()

    cron.write()
