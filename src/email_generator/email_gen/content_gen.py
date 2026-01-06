import logging
from email.message import EmailMessage

import email_gen
from parsers import YamlParser
from blocks import Block

class ContentGen:
    def __init__(self, data: YamlParser):
        self.all_data: YamlParser = data
        self.logger = logging.getLogger(__name__)
        self.html_gen = email_gen.Html()
        self.blocks: list = self._create_blocks()

    def _create_blocks(self) -> dict[str, Block]:
        """ This returns a list of Block objects
        
            Return:
                - The key is the name of the section in the content.yaml
                and the value is a Blocks objects
        """
        blocks = {}

        for key, value in self.all_data.content.items():
            blocks[key] = Block(value, self.all_data.block_format)

        return blocks
    
    def structure_blocks(self) -> str:
        """ This takes the html content in each block stored
            in self.blocks and organizes all of it into a single
            html page. This will utilize the structure.yaml to 
            organize the blocks.
        """
        indent = self.html_gen.html_indent()
        ret_val = (f"""{indent}<div style="font-family: 'Aptos', Aptos_EmbeddedFont, """
                  """Aptos_MSFontService, Calibri, Helvetica, sans-serif;">\n""")
        self.html_gen.html_incr_indent()

        # build html page.
        for _, value in self.all_data.structure.items():
            if value["section_org"] == "single":
                # retrieve single heading
                blk_name = value["blocks"][0]
                ret_val += self.blocks[blk_name].html_content
            elif value["section_org"] == "side-by-side":
                # create 1 row table
                ret_val += self.html_gen.open_tag("table")
                ret_val += self.html_gen.open_tag("row")

                for blk_name in value["blocks"]:
                    html = self.blocks[blk_name].html_content
                    ret_val += self.html_gen.get_item("ri", html)
                ret_val += self.html_gen.close_tag("row")
                ret_val += self.html_gen.close_tag("table")

            if value["section_break"]:
                ret_val += self.html_gen.html_hr()

        self.html_gen.html_decr_indent()
        indent = self.html_gen.html_indent()
        ret_val += f"{indent}</div>\n"

        return ret_val

    def gen_email(self) -> EmailMessage:
        """ This method generates an email"""
        email_body = self.structure_blocks()

        msg = EmailMessage()
        msg['Subject'] = self.all_data.subject
        msg['To'] = ", ".join(self.all_data.recipients['to'])
        msg.set_content(email_body, subtype="html")

        return msg
