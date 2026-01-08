import os
import sys
import subprocess
from email.message import EmailMessage


def outlook(msg: EmailMessage):
    # Save as .eml

    eml_file = os.path.join('files','email_files', 'report.eml')
    with open(eml_file, 'wb') as f:
        f.write(msg.as_bytes())

    if sys.platform == "win32":
        os.startfile(eml_file)  # Only available on Windows
    elif sys.platform == "darwin":
        subprocess.call(["open", eml_file])  # For macOS
    else:
        subprocess.call(["xdg-open", eml_file])  # For Linux