import logging
import sys
import os
from argparse import Namespace
from email.message import EmailMessage

import parsers
from gen_html import YamlGen
from email_gen import mail_clients
import email_gen

logger = logging.getLogger(__name__)

def main():

    args: Namespace = parsers.cli_args()
    template = os.path.join(os.getcwd(),'templates', args.template) if args.template else None
    client: str = args.client

    try:
        config_data: parsers.YamlParser = parsers.YamlParser(template)
        content = email_gen.ContentGen(config_data)
        msg: EmailMessage = content.gen_email()

        with open("email_body_3.html", "w", encoding="utf-8") as f:
            f.write(msg.get_content())
        
        if sys.platform == "win32" and client == "outlook":
            print("\n------------------------------------------------------------")
            print("Please ensure that your Outlook app is open before continuing.")
            input("Once Outlook is open, press any key to continue...")
            mail_clients.outlook(msg)
    except Exception as e:
        logger.exception("The following exception was caught: %s", e)
        input("Please press any button to exit tool...")
        sys.exit()

if __name__ == "__main__":
    main()
