import os
import sys

from email.message import EmailMessage
import win32com.client
from win32com.client import CDispatch

def gen_outlook_email(msg: EmailMessage):

    if not sys.platform == "win32":
        raise OSError(f"Wrong OS. Needed os is win32, but currently using {sys.platform}")

    outlook = win32com.client.Dispatch("Outlook.Application")
    mail: CDispatch = outlook.CreateItem(0)
    mail.To = msg.get("To", "")
    mail.Subject = msg.get("Subject","")
    mail.HTMLBody = msg.get_content()
    mail.Display()

def gen_outlook_email_2(msg: EmailMessage):
    # Save as .eml
    with open('report.eml', 'wb') as f:
        f.write(msg.as_bytes())

    # Launch in Outlook
    os.startfile('report.eml')