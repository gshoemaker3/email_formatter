from typing import List
from datetime import date

import yaml
import os


class Html:
    def __init__(self):
        self.tab_size = 0
        self.parsed_yaml = self._load_file(os.path.join('email_gen', 'html_mappings.yaml'))
        self.date = date.today().strftime("%m-%d-%Y")
        self.open_tags = self.parsed_yaml["open_tags"]
        self.close_tags = self.parsed_yaml["close_tags"]
        self.default_styling = self.parsed_yaml["default_styling"]


    def get_item(self, item_type, data, options: list = None):
        indent = self.html_indent()
        opts = " ".join(options) if options else self.default_styling[item_type]
        o_tag = self.open_tags[item_type].format(opts)
        c_tag = self.close_tags[item_type]
        return indent + o_tag + data + c_tag

    def html_indent(self):
        tabs = " " * self.tab_size
        return tabs

    def heading(self, formatting: dict, text: str) -> str:
        """ This creates a html heading 
        
            Args:
                - text: This is the text that will be converted to html
    
            Return:
                - The completed html heading.
        """
        settings = ['bold', 'underline']
        lvl = formatting['level']
        indent = self.html_indent()
        tag = self.open_tag("heading", False).replace('<h',f'<h{lvl}')
        ret_val = f"{indent}{tag}"

        for option in settings:
            ret_val += self.open_tags[option] if formatting[option] else ""

        ret_val += text

        for option in reversed(settings):
            ret_val += self.close_tags[option] if formatting[option] else ""
        ret_val += self.close_tags["heading"].replace('</h',f'</h{lvl}')
        return ret_val

    def html_hr(self):
        indent = self.html_indent()
        return f"{indent}<hr>\n"

    def html_list_item(self, text: str):
        """ This creates a html list item

            Args:
                - the text that will be converted to a list item
        """
        indent = self.html_indent()
        li = f"{indent}<li>{text}</li>\n"
        return li

    def open_tag(self, tag_key: str, indent: bool = True, options: List[str] = None) -> str:
        """ This creates and HTML open tag for the tag specified in the tag_key
            input argument.

            Args:
                - tag_key: This is the key that will be used to obtain the open tag. 
                           The key-value pairs can be found in the self.open_tags dict
                - indent: This determines if the self.tab_size needs to be incremented.
                - options: This is a list of options that will be applied to the open tag.
                           Options include font, font size, style, etc.

            Return:
                - the desired open tag
        """
        ind = self.html_indent()

        if tag_key.upper() == "NONE":
            return ""

        opts = " ".join(options) if options else self.default_styling[tag_key]
        tag = self.open_tags[tag_key].format(opts)
        ret_val = ind + tag
        if indent:
            self.html_incr_indent()
        return ret_val

    def close_tag(self, tag_type: str):
        if tag_type.upper() == "NONE":
            return ""

        self.html_decr_indent()
        ind = self.html_indent()
        tag = self.close_tags[tag_type]

        return ind + tag

    def html_incr_indent(self):
        self.tab_size += 4

    def html_decr_indent(self):
        self.tab_size -= 4

    def table(self, rows: int, cols: int, items: list):
        """ this is used to create a html table based off of input arguments.
            If there are more elements requested to be in the table than provided
            elements in the data argument, an empty table element is added.

            Args:
                - rows: the number of rows the table will have
                - cols: the number of columns the table will have
                - items: each element contains html code that the
                        user wants to insert into the table. If
                        there are more table entries than elements
                        in the list, blanks values will be added to
                        the table. NOTE: This data comes in as a 1D array
                        that is then converted to a 2D table based 
                        on the number of rows and columns.
            return:
                - html code representing the table.
        """
        ret_val: str = self.open_tag("table")

        # Row loop
        for row in range(rows):
            # start row
            ret_val += self.open_tag("row")
            # column loop
            for col in range(cols):
                item_idx: int = cols * row + col
                row_item: str = items[item_idx] if item_idx < len(items) else ""
                ret_val += self.get_item('ri', row_item)
            # End row
            ret_val += self.close_tag("row")
        ret_val += self.close_tag("table")

        return ret_val

    def _load_file(self, filepath: str) -> dict:
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

