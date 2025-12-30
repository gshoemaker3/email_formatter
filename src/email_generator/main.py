import logging
import sys
import os
from argparse import Namespace

import parsers
from gen_html import YamlGen
logger = logging.getLogger(__name__)

def test(html: str):
    with open("email_body.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():

    args: Namespace = parsers.cli_args()
    template = os.path.join(os.getcwd(),'templates', args.template) if args.template else None

    try:
        config_data = parsers.YamlParser(template)
        config_data.load_files()
        generator = YamlGen(config_data)
        msg = generator.gen_email()
        test(msg.get_content())
    except Exception as e:
        logger.exception("The following exception was caught: %s", e)
        input("Please press any button to exit tool...")
        sys.exit()

if __name__ == "__main__":
    main()
