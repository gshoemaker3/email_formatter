import os

from email.message import EmailMessage


def outlook(msg: EmailMessage):
    # Save as .eml
    with open('report.eml', 'wb') as f:
        f.write(msg.as_bytes())

    # Launch in Outlook
    os.startfile('report.eml')