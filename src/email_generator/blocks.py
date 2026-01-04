import email_gen
from email_gen import Html

class Blocks:
    def __init__(self, section: dict, format: dict):
        self.type: str = section['type']
        self.title: str = section['title']
        self.sub_bullets: bool = section['sub_bullets']
        self.section_break: bool = section['section_break']
        self.content_structure: str = section['content_structure']
        self.content: list = section['content']
        self.format: dict = format[section['type']]
        self.html_generator: Html = email_gen.Html()
        self.html_content: str = self._convert_data()

    def get_format(self, data: dict):
        self.format = data

    def _convert_data(self) -> str:
        """ This will take in the member variables of the block and 
            convert the content to an html snippet. Once all of the 
            data stored in self.content has been converted to html, 
            the converted data is stored in self.html_content

            Return:
                - The html version of the data stored in self.content
        """
        ret_val = ""
        # create title
        ret_val += self.html_generator.heading(self.format, self.title)

        #Create Open tag for content structure.
        ret_val += self.html_generator.open_tag(self.content_structure)

        # Process content
        for item in self.content:
            ret_val += self.process_content(item)

        # Create close tag for content structure
        ret_val += self.html_generator.close_tag(self.content_structure)

        # Store converted data in member var.
        return ret_val

    def process_content(self, data: dict | list) -> str:
        """ This processes the data in self.content by recursing through it.
        
            Args:
                - data: This is the dictionary or list that will be processed.

            Return:
                - This eventually returns a string 
        """

        if isinstance(data, dict):
            # process dictionary
            for key, value in data.items():
                if isinstance(value, str):
                    # base case
                    return self.html_generator.get_item(key, value)
                elif isinstance(value, list):
                    if key in ["bullets", "numbers"] :
                        return (self.html_generator.open_tag(key)
                                + self.process_content(value)
                                + self.html_generator.close_tag(key))
                    else:
                        return self.process_content(value)
                elif isinstance(value, dict):
                    return self.process_content(value)
                else:
                    raise TypeError(f"unhandled type ({type(value)}) found.")
        elif isinstance(data, list):
            # Process list
            return self.process_content(data[0])
