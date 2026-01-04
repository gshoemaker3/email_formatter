from typing import List
import logging
from email.message import EmailMessage

from parsers import YamlParser
from email_gen import Html


class YamlGen:
    def __init__(self, data: YamlParser):
        self.data = data
        self.logger = logging.getLogger(__name__)
        self.generator = Html()

    def test(self):
        """ This method will validate yaml files before 
            performing operations on them.
        """
        print("----------Types-----------")
        self.print_dict(self.data.type_format)
        print("----------HEADINGS-----------")
        self.print_dict(self.data.section_defs)
        print("----------HEADING CONTENT-----------")
        self.print_dict(self.data.content)

    def gen_email(self) -> EmailMessage:
        """ This method generates an email"""
        email_body = self._gen_body()

        msg = EmailMessage()
        msg['Subject'] = self.data.subject['title']
        msg['To'] = ", ".join(self.data.recipients['to'])
        msg.set_content(email_body, subtype="html")

        return msg

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
        for key, value in self.data.section_defs.items():
            h_type = value['type']
            sect_break = value['section_break']

            if h_type == "side_by_side_headings":
                ret_val += self._gen_sub_sections(h_type, key)
            else:
                ret_val += self._gen_section(value, h_type, key)

            ret_val += self.generator.html_hr() if sect_break else ""
        return ret_val

    def _gen_section(self, value: dict, s_type: str, key: str) -> str:
        """ This generates html based on a section in the headings.yaml
        
            Args:
                - value: The section of section_defs.yaml that will be converted html
                - s_type: The section type that is defined in body_format.yaml
                - key: The key to the section being converted to html

            Return:
                - The html generated from a single section listed in headings.yaml
        """
        formatting = self.data.type_format[s_type]
        options = formatting['options']
        title = value['title']
        ret_val = self.generator.heading(formatting, title)
        ret_val += self.proc_section(self.data.content[key], value, options)

        return ret_val
    
    def _gen_table(self, s_type: str, s_key: str) -> str:
        tbl_options = self.data.type_format[s_type]["options"]
        row_num = self.data.section_defs[s_key]['num_rows']
        ret_val = self.generator.html_open_tag("table", tbl_options)
        ret_val += self._gen_table_headings(self.data.section_defs[s_key], self.data.type_format[s_type])

        # generate rows.
        content_tag = self.data.type_format[s_type]['content_format']['tag']
        content_options = self.data.type_format[s_type]['content_format']['options']
        headings = self.data.section_defs[s_key]['headings']
        for idx in range(row_num):
            ret_val += self.generator.html_open_tag("row")
            for key, val in headings.items():
                ret_val += self.proc_section(self.data.content[key][f'row_{idx+1}'], headings, content_options)
            ret_val += self.generator.html_close_tag("row")


    def _gen_table_headings(self, sub_section: dict, type_format: dict):
        ret_val = self.generator.html_open_tag("row")
        headings = sub_section['headings']
        tag = type_format["heading_format"]["tag"]
        options = type_format["heading_format"]["options"]
        for key, val in headings.items():
            ret_val += self.generator.html_get_item(tag, key, options)
        
        ret_val += self.generator.html_close_tag("row")
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
        ret_val = self.generator.open_tag("table", tbl_opts)
        ret_val += self.generator.open_tag("row")

        for key, value in self.data.section_defs[s_key]['headings'].items():
            ret_val += self.generator.open_tag("ri", ri_opts)
            ret_val += self._gen_section(value, s_type, key)
            ret_val += self.generator.close_tag("ri")

        ret_val += self.generator.close_tag("row")
        ret_val += self.generator.close_tag("table")

        return ret_val

    def proc_section(self, data, content: dict, options: List[str]):
        """ This processes the section that is being converted to html.

            Args:
                - data: This is either a list or dict
        """
        ret_val = ""
        if isinstance(data, list):
            ret_val += self.proc_list(data, content, options)
        elif isinstance(data, dict):
            ret_val += self.proc_dict(data, content, options)
        else:
            raise TypeError(f"Unknown data type provided: {type(data)}")
        return ret_val

    def proc_list(self, data: list, headings: dict, options: List[str]) -> str:
        """ This processes lists found while processing a section
            to be converted to html. This method utilizes recursion 
            to process the data found in the data member variable.

            Args:
                - data: a list from the section that is being processed that
                  can contain more lists, dictionaries, or strings.

            Return:
                - a group of items in the section that has been processed into html.
        """
        sect_type = headings["content_structure"]
        ret_val = self.generator.html_open_tag(sect_type)
        for val in data:
            if isinstance(val, str):
                ret_val += self.generator.html_list_item(val)
            elif isinstance(val, dict):
                ret_val += self.proc_dict(val, headings, options)
            elif isinstance(val, list):
                ret_val += self.proc_list(val, headings, options)

        ret_val += self.generator.html_close_tag(sect_type)
        return ret_val

    def proc_dict(self, data: dict, headings: dict, options: List[str]):
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
                ret_val += self.generator.html_get_item(key, value, options)
            elif isinstance(value, list):
                ret_val += self.proc_list(value, headings, options)
            elif isinstance(value, dict):
                ret_val += self.proc_dict(value, headings, options)
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
