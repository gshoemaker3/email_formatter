import argparse
import os

def cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Email Generator Parser")

    parser.add_argument('-t', '--template', type=sanitize_template, help="Template to generate email from")
    parser.add_argument('-c', '--client', default="outlook",
                        choices=["outlook", "gmail"], type=str,
                        help="Email client that will be sendint the email")
    parser.add_argument('-v', '--verbose', action="store_true")

    return parser.parse_args()

def sanitize_template(value: str) -> str:
    if not isinstance(value, str):
        raise argparse.ArgumentTypeError("The value for '-t'/'--template' must be a string")

    template = os.path.join(os.getcwd(), 'templates', value)
    if not os.path.exists(template):
        raise argparse.ArgumentError(argument=value, message=f"The provided template doesn't exist")

    return value.strip().lower()
