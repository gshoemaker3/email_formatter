import os
import logging
import yaml
from typing import Dict, List
from pathlib import Path

from . import utils



class Parser:

    def __init__(self):
        pass

    def select_template(self) -> Path:
        """ This allows the user to select a template stored in the templates
            directory by displaying all of the templates and capturing the
            user's input

            Return:
                - The fully qualified path to the select template to generate the email with.
        """
        try:
            template_dir = Path(os.path.join(os.getcwd(), 'templates'))
            templates: List[str] = self.get_templates(template_dir)
            template: str = self.select_from_list(templates)
            return template_dir / template
        except Exception as e:
            print(e)

    def get_templates(self, template_dir: Path) -> List[str]:
        """ This gathers all templates in the 'templates' directory 
            Templates should always be directories since they are a 
            collection of files. All files are ignored.
        """
        #template_dir = Path(os.path.join(os.getcwd(), "templates"))
        templates = template_dir.glob("*")
        templates = [os.path.basename(i) for i in templates if not os.path.isfile(i)]

        if len(templates) == 0:
            raise FileNotFoundError("No templates were found"
                                    f" in the template directory ({template_dir})")
        return templates

    def select_from_list(self, options: List[str]) -> str:
        """ This method is displays the strings stored in 'options'
            with a corresponding number so a user can select any of the
            displayed items by inputting a number.

            Args:
                - options: A list that contains all of the available options that
                will be displayed to the user.
            Return:
                - The string that the user has selected.
            
        """
        if not isinstance(options, list):
            raise TypeError(f"The provided input arguement is type: {type(options)} "
                             "instead of type List")
        while True:
            print("\nPlease select from the following options:")
            print("--------------------------------------------")
            for idx, item in enumerate(options):
                print(f"{idx+1}) {item}")
            selection = input("\nEnter number here: ")
            is_valid = self.selection_handler(selection, len(options))
            if is_valid:
                return options[int(selection)-1]


    def selection_handler(self, selection: str, num_selection: int) -> bool:
        """ This runs checks on the 'selection' input argument. the 
            checks are defined by the if statements.

            Args:
                - selection: This is an input that is provided by the user.
                It contains the value that needs to be validated.
                - num_selection: This is the number of selections that were
                available for the user to choose from.
            Return:
                - True if 'selection' is a number and is between 0 and the 
                int stored in num_selection, otherwise false.
        """
        if not selection.isdigit():
            print(f"The provided response: {selection} is invalid; it isn't a number."
                " Please try again and input a number.\n")
            return False
        if 1 > int(selection) > len(num_selection):
            print(f"The provided response: {selection} is invalid; number provided is out of range"
                "Please provide a number that is displayed in the selections above.\n")
            return False
        return True

class YamlParser(Parser):

    def __init__(self, config_dir=None):
        self.config_dir = config_dir if config_dir else self.select_template()
        self.font = None
        self.type_format = None
        self.recipients = None
        self.section_defs = None
        self.subject = None
        self.content = None
        self.logger = logging.getLogger("YamlParser")

        self._load_files()

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

    def _load_files(self):
        """ This loads all yaml files and stores them in 
            member variables.
        """
        yaml_files = utils.get_files(self.config_dir, [".yaml", ".yml"])

        for file in yaml_files:
            content = self._load_file(file)

            if file.name == "section_format.yaml":
                self.type_format = content["type"]
                self.font = content["font"]
            elif file.name == "content.yaml":
                self.content = content
            elif file.name == "recipients.yaml":
                self.recipients = content
            else:
                raise ValueError(f"Unknown yaml file found: {file}")
