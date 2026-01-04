import logging

import email_gen
from parsers import YamlParser
from blocks import Blocks

class ContentGen:
    def __init__(self, data: YamlParser):
        self.all_data: YamlParser = data
        self.logger = logging.getLogger(__name__)
        self.generator = email_gen.Html()
        self.blocks: list = self._create_blocks()

    def _create_blocks(self) -> dict[str, Blocks]:
        """ This returns a list of Block objects"""
        blocks = {}

        for key, value in self.all_data.content.items():
            blocks[key] = Blocks(value, self.all_data.type_format)

        return blocks
