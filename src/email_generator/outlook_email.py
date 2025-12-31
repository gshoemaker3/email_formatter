import os

import win32com.client
from email.message import EmailMessage

def gen_outlook_email(msg: EmailMessage):
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
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