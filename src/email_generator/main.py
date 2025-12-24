import logging
import sys
import os

from template_parser import YamlParser
from gen_html import YamlGen

logger = logging.getLogger(__name__)

def test(html: str):
    with open("email_body.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    try:
        config_dir = os.path.join(os.getcwd(), "templates", "example")
        config_data = YamlParser(config_dir)
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
