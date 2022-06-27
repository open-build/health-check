from __future__ import unicode_literals
from time import sleep, time, strftime
import requests
import datetime
import io
import sys
import os
from .models import MonitorSite, MonitorSiteEntry

from .ssl_check import check_it_out

DELAY = 60  # Delay between site queries
EMAIL_INTERVAL = 1800  # Delay between alert emails

last_email_time = {}  # Monitored sites and timestamp of last alert sent


# Message template for alert
MESSAGE = """From: {sender}
To: {receivers}
Subject: Open Build Health Check Alert

You are being notified that {site} is experiencing a {status} status!
"""


def error_log(site, status):
    # Log status message to log file
    with open('monitor.log', 'a') as log:
        log.write("({}) {} STATUS: {}\n".format(strftime("%a %b %d %Y %H:%M:%S"),
                                                site,
                                                status,
                                                )
                  )


def send_alert(site, status):
    """If more than EMAIL_INTERVAL seconds since last email, resend email"""
    sendmail(sender,
                     receivers,
                     MESSAGE.format(sender=sender,
                                    receivers=", ".join(receivers),
                                    site=site,
                                    status=status
                                    )
                     )
    last_email_time[site] = time()  # Update time of last email
    # using SendGrid's Python Library
    # https://github.com/sendgrid/sendgrid-python
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    message = Mail(
    from_email=sender,
    to_emails=", ".join(receivers),
    subject='Open Build Health Check alert for ' + site,
    html_content=site + status)

    sg = SendGridAPIClient(os.environ.get('SENDGRID'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)




def ping(site):
    # Send GET request to input site and return status code
    resp = requests.get(site)
    return resp.status_code

def check_all_sites():
    sites = MonitorSite.objects.all()

    for site in sites:
        check_now(site)
        sleep(DELAY)


def ssl_check(url):
    import OpenSSL
    import ssl, socket

    # get domain
    domain = url

    # return object
    check = {'error': None,'cert': None, 'exp_date': None,'error_level': None,'message': "Success"}

    hostname = domain.replace("https://","")
    port = 443

    status = check_it_out(hostname,port)

    return status


def check_now(site_to_check):
    site = MonitorSite.objects.get(id=site_to_check)
    url2check = "https://" + site.url
    new_status = ping(url2check)
    ssl_state = ssl_check(url2check)
    if new_status == 200:
        message = "200"
    else:
        error_log(site, new_status)
        send_alert(site, new_status)
        message = "ALERT: " + new_status

    # update model
    CurrentDate = datetime.datetime.now().date()

    print(ssl_state.cert)

    if ssl_state.cert.not_valid_after:
        ssl_expiry_date_datetime_object = ssl_state.cert.not_valid_after.date()

        if CurrentDate > ssl_expiry_date_datetime_object:
            new_ssl_status="expired"
        else:
            new_ssl_status="current"
    else:
        new_ssl_status = "Error:" + str(ssl_state.get('error'))
        ssl_expiry_date_datetime_object = None

    MonitorSite.objects.filter(id=site_to_check).update(status=new_status,last_polled_date_time=CurrentDate,ssl_status=new_ssl_status,ssl_expirtaion=ssl_expiry_date_datetime_object)
    MonitorSiteEntry.objects.create(site=site,status=new_status,ssl_status=new_ssl_status,
    ssl_expirtaion=ssl_expiry_date_datetime_object,url_message=new_status,
    ssl_message=ssl_state.cert.issuer)
    return str(new_status) + " :: " + str(("SSL Certificate for domain", site_to_check, " will expire on (YYYY-MM-DD)", ssl_expiry_date_datetime_object, " issuer: " ,ssl_state.cert.issuer))


if __name__ == '__main__':
    main()
