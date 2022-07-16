from monitorsites.health_check import check_all_sites

def my_scheduled_job():
    check_all_sites()
