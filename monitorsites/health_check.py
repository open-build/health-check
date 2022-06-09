from __future__ import unicode_literals
from time import sleep, time, strftime
import requests
import io
import smtplib
import sys
from smtp_config import sender, password, receivers, host, port


DELAY = 60  # Delay between site queries
EMAIL_INTERVAL = 1800  # Delay between alert emails

last_email_time = {}  # Monitored sites and timestamp of last alert sent


# Message template for alert
MESSAGE = """From: {sender}
To: {receivers}
Subject: Open Build Health Check Alert

You are being notified that {site} is experiencing a {status} status!
"""


def colorize(text, color):
    """Return input text wrapped in ANSI color codes for input color."""
    return COLOR_DICT[color] + str(text) + COLOR_DICT['end']


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
    if (time() - last_email_time[site]) > EMAIL_INTERVAL:
        try:

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
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
                    except smtplib.SMTPException:



def ping(site):
    # Send GET request to input site and return status code
    resp = requests.get(site)
    return resp.status_code


def get_sites():
    # Return list of unique URLs This will be in the model next
    sites = ['https://www.open.build', 'https://www.buildly.io',]

    # Eliminate exact duplicates in sites
    sites = list(set(sites))

    return sites


def main():
    sites = get_sites()

    for site in sites:
        print("Beginning monitoring of {}".format(site))
        last_email_time[site] = 0  # Initialize timestamp as 0

    while sites:
        for site in sites:
            status = ping(site)
            if status == 200:
                sys.stdout.flush()
            else:
                error_log(site, status)
                send_alert(site, status)
        sleep(DELAY)
    else:
        print("No site(s) input to monitor!")


if __name__ == '__main__':
    main()
