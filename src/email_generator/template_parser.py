import os
import logging
from typing import Dict

import yaml

from src.email_generator import utils


class YamlParser:

    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.font = None
        self.type_format = None
        self.recipients = None
        self.headings = None
        self.subject = None
        self.heading_content = None
        self.logger = logging.getLogger("YamlParser")

    def _load_file(self, filepath: str) -> Dict:
        """ loads a yaml file.

            Args:
                - filepath: the filepath to the yaml file that will be parsed.
            Return:
                - A dictionary of the parsed yaml file stored in filepath.
        """

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Could not find the following file: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def load_files(self):
        """ This loads all yaml files and stores them in 
            member variables.
        """
        yaml_files = utils.get_files(self.config_dir, [".yaml", ".yml"])

        for file in yaml_files:
            content = self._load_file(file)

            if file.name == "body_format.yaml":
                self.type_format = content["type"]
                self.font = content["font"]
            elif file.name == "heading_content.yaml":
                self.heading_content = content
            elif file.name == "headings.yaml":
                self.headings = content["sections"]
                self.subject = content["subject"]
            elif file.name == "recipients.yaml":
                self.recipients = content
            else:
                raise ValueError(f"Unknown yaml file found: {file}")
