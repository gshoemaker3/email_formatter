from typing import List
import logging

from config_parser.yaml_parser import YamlParser
from html_utils import Html


class YamlGen:
    def __init__(self, data: YamlParser):
        self.data = data
        self.logger = logging.getLogger(__name__)
        self.generator = Html()

    def check_data(self):
        self._check_headings()

    def _check_keys(self, data: dict, required_keys: List[str]):
        for key in required_keys:
            if key not in data:
                raise AttributeError(f"This following required key is missing: {key}")

    def _check_headings(self):

        # Check for required headings
        try:
            for key, value in self.data.headings.items():
                self._check_keys(value, ["title", "type", "sub_bullets"])
        except AttributeError as e:
            raise AttributeError(f"The {key} heading in the headings.yaml is "
                                "missing a required field %s", e)
        except Exception as e:
            self.logger.exception(e)

    def test(self):
        """ This method will validate yaml files before 
            performing operations on them.
        """
        print("----------Types-----------")
        self.print_dict(self.data.type_format)
        print("----------HEADINGS-----------")
        self.print_dict(self.data.headings)
        print("----------HEADING CONTENT-----------")
        self.print_dict(self.data.heading_content)

    def gen_email(self):
        """ This method generates an email"""
        email_body = self._gen_body()
        return email_body
        # print(email_body)

    def _gen_body(self) -> str:
        """ This generates the body of an email in html.
            Return:
                - The body of the email in html.
        """
        indent = self.generator.html_indent()
        ret_val = (f"""{indent}<div style="font-family: 'Aptos', Aptos_EmbeddedFont, """
                  """Aptos_MSFontService, Calibri, Helvetica, sans-serif;">\n""")
        self.generator.html_incr_indent()

        ret_val += self._gen_sections()

        self.generator.html_decr_indent()
        indent = self.generator.html_indent()
        ret_val += f"{indent}</div>\n"
        return ret_val

    def _gen_sections(self) -> str:
        """ This generates all of html for the sections defined in the headings.yaml
        
            Return:
                - All of the sections in the headings.yaml and heading_content.yaml converted
                  to html.
        """
        ret_val = ""
        for key, value in self.data.headings.items():
            h_type = value['type']
            sect_break = value['section_break']
            # generate sub sections
            if h_type == "side_by_side_headings":
                ret_val += self._gen_sub_sections(h_type, key)
                continue
            ret_val += self._gen_section(value, h_type, key)
            ret_val += "<hr>" if sect_break else ""
        return ret_val

    def _gen_section(self, value: dict, s_type: str, key: str) -> str:
        """ This generates html based on a section in the headings.yaml
        
            Args:
                - value: The section that will be converted html
                - s_type: The section type that is defined in body_format.yaml
                - key: The key to the section being converted to html

            Return:
                - The html generated from a single section listed in headings.yaml
        """
        lvl = self.data.type_format[s_type]['level']
        title = value['title']
        ret_val = self.generator.html_heading(lvl, title)
        ret_val += self.proc_section(self.data.heading_content[key], key)
        return ret_val

    def _gen_sub_sections(self,s_type: str, s_key: str) -> str:
        """ This generates a section of sub sections/headings. These
            Are typically groupings of headings that are one the same
            row and in a smaller font size.
        
            Args:
                - s_type: The section type that is defined in body_format.yaml
                - s_key: The key to the section that contains all of the 
                  sub sections/headings.
    
            Return:
                - The html that was generated from section. Sections of sub
                  sections/headings are currently in the form of tables.
        """
        tbl_opts = ['width="100%"', 'cellpadding="5"', 'cellspacing="0"', 'border="0"']
        ri_opts = ['valign="top"']
        ret_val = self.generator.html_open_tag("table", tbl_opts)
        ret_val += self.generator.html_open_tag("row")

        sect_break = self.data.headings[s_key]
        for key, value in self.data.headings[s_key]['headings'].items():
            ret_val += self.generator.html_open_tag("ri", ri_opts)
            ret_val += self._gen_section(value, s_type, key)
            ret_val += self.generator.html_close_tag("ri")

        ret_val += self.generator.html_close_tag("row")
        ret_val += self.generator.html_close_tag("table")

        if sect_break:
            ret_val = self.generator.html_hr(ret_val)

        return ret_val

    def proc_section(self, data, sect_name):
        """ This processes the section that is being converted to html.

            Args:
                - data: This is either a list or dict
        """
        ret_val = ""
        if isinstance(data, list):
            ret_val += self.proc_list(data, sect_name)
        elif isinstance(data, dict):
            ret_val += self.proc_dict(data, sect_name)
        else:
            raise TypeError(f"Unknown data type provided: {type(data)}")
        return ret_val

    def proc_list(self, data: list, sect_key: str) -> str:
        """ This processes lists found while processing a section
            to be converted to html. This method utilizes recursion 
            to process the data found in the data member variable.

            Args:
                - data: a list from the section that is being processed that
                  can contain more lists, dictionaries, or strings.

            Return:
                - a group of items in the section that has been processed into html.
        """
        # indent = self.generator.html_indent()
        sect_type = self.data.headings[sect_key]["content_structure"]
        ret_val = self.generator.html_open_tag(sect_type)
        # ret_val = f"{indent}<ul>\n"
        # self.generator.html_incr_indent()
        for val in data:
            if isinstance(val, str):
                ret_val += self.generator.html_list_item(val)
            elif isinstance(val, dict):
                ret_val += self.proc_dict(val, sect_key)
            elif isinstance(val, list):
                ret_val += self.proc_list(val, sect_key)

        ret_val += self.generator.html_close_tag(sect_type)
        return ret_val
        # self.generator.html_decr_indent()
        # indent = self.generator.html_indent()
        # return ret_val + f"{indent}</ul>\n"

    def proc_dict(self, data: dict, sect_key: str):
        """ This processes dictionaries found while processing a section
            to be converted to html. This method utilizes recursion 
            to process the data found in the data member variable.

            Args:
                - data: a dictionary from the section that is being processed that
                  can contain more lists, dictionaries, or strings.

            Return:
                - a group of items in the section that has been processed into html.
        """
        ret_val = ""
        for key, value in data.items():
            if isinstance(value, str):
                ret_val += self.generator.html_get_item(key, value)
                # ret_val += self.generator.html_list_item(value)
            elif isinstance(value, list):
                ret_val += self.proc_list(value, sect_key)
            elif isinstance(value, dict):
                ret_val += self.proc_dict(value, sect_key)
        return ret_val

    def print_dict(self, data):
        if isinstance(data, list):
            for item in data:
                print(item)
        elif isinstance(data, str):
            print(data)
        else:
            for key, value in data.items():
                print(f"{key} == {value}")
