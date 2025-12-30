import logging
import sys
from argparse import Namespace

from parsers.template_parser import YamlParser
from gen_html import YamlGen
from parsers.cl_parser import cli_args
logger = logging.getLogger(__name__)

def test(html: str):
    with open("email_body.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():

    args: Namespace = cli_args()

    try:
        config_data = YamlParser()
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
