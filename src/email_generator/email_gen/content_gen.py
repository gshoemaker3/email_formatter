import logging
from logging import Logger
from email.message import EmailMessage

import email_gen
from parsers import YamlParser
from email_gen import Html
from blocks import Block

class ContentGen:
    """ 
        This class is used for the bulk of the email generation. 
    """
    def __init__(self, data: YamlParser):
        self.all_data: YamlParser = data
        self.logger: Logger = logging.getLogger(__name__)
        self.html_gen: Html  = email_gen.Html()
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
        indent: str = self.html_gen.html_indent()
        ret_val: str = (f"""{indent}<div style="font-family: 'Aptos', Aptos_EmbeddedFont, """
                  """Aptos_MSFontService, Calibri, Helvetica, sans-serif;">\n""")
        self.html_gen.html_incr_indent()

        # build html page.
        for _, value in self.all_data.structure.items():
            if value["section_org"] == "single":
                # retrieve single heading
                blk_name: str = value["blocks"][0]
                ret_val += self.blocks[blk_name].html_content
            elif value["section_org"] == "side-by-side":
                # # create 1 row table
                cols: int = len(value["blocks"])
                table_items: list = [self.blocks[block].html_content for block in value["blocks"]]
                ret_val += self.html_gen.table(1, cols, table_items)

            if value["section_break"]:
                ret_val += self.html_gen.html_hr()

        self.html_gen.html_decr_indent()
        indent = self.html_gen.html_indent()
        ret_val += f"{indent}</div>\n"

        return ret_val

    def gen_email(self) -> EmailMessage:
        """ This method generates an email
        
            Return:
                - The message that is used to create the html file and the eml file.
        """
        email_body = self.structure_blocks()

        msg = EmailMessage()
        msg['Subject'] = self.all_data.subject
        msg['To'] = ", ".join(self.all_data.recipients['to'])
        msg.set_content(email_body, subtype="html")

        return msg
