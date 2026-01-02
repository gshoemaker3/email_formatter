import logging
import sys
import os
from argparse import Namespace

import parsers
from gen_html import YamlGen
from email_generator import email_gen

logger = logging.getLogger(__name__)

def test(html: str):
    with open("email_body.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():

    args: Namespace = parsers.cli_args()
    template = os.path.join(os.getcwd(),'templates', args.template) if args.template else None
    client: str = args.client

    try:
        config_data = parsers.YamlParser(template)
        config_data.load_files()
        generator = YamlGen(config_data)
        msg = generator.gen_email()
        test(msg.get_content())

        if sys.platform == "win32" and client == "outlook":
        
            print("\n------------------------------------------------------------")
            print("Please ensure that your Outlook app is open before continuing.")
            input("Once Outlook is open, press any key to continue...")
            email_gen.outlook(msg)
    except Exception as e:
        logger.exception("The following exception was caught: %s", e)
        input("Please press any button to exit tool...")
        sys.exit()

if __name__ == "__main__":
    main()
