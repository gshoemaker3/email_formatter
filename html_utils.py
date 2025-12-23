from typing import List


class Html:
    def __init__(self):
        self.tab_size = 0
        self.h_opts = 'style="margin-bottom: 2px;"'
        self.open_tags = {"unordered list": "<ul {}>\n",
                          "ordered list": "<ol {}>\n",
                          "li": "<li {}>",
                          "table": "<table {}>\n",
                          "txt": "<p {}>",
                          "heading": "<h {}>",
                          "bold": "<b>",
                          "row": "<tr {}>\n",
                          "ri": "<td {}>\n",
                          "underline": "<u>"
                          }
        self.close_tags = {"unordered list": "</ul>\n",
                          "ordered list": "</ol>\n",
                          "li": "</li>\n",
                          "table": "</table>\n",
                          "txt": "</p>\n",
                          "heading": "</h>\n",
                          "bold": "</b>",
                          "row": "</tr>\n",
                          "ri": "</td>\n",
                          "underline": "</u>"
                          }
        self.default_opts = {"unordered list": 'style="margin: 4px 0;"',
                             "ordered list": 'style="margin: 4px 0;"',
                             "li": 'style="margin: 0;"',
                             "table": 'width="100%" cellpadding="5" cellspacing="0" border="0"',
                             "txt": 'style="margin: 4px 0;"',
                             "heading": 'style="margin-bottom: 2px;"',
                             "bold": "",
                             "row": "",
                             "ri": 'valign="top"',
                             "underline": ""
                            }

    def html_get_item(self, item_type, data, options: list = None):
        indent = self.html_indent()
        opts = " ".join(options) if options else self.default_opts[item_type]
        o_tag = self.open_tags[item_type].format(opts)
        c_tag = self.close_tags[item_type]
        return indent + o_tag + data + c_tag

    def html_indent(self):
        tabs = " " * self.tab_size
        return tabs

    def html_heading(self, formatting: dict, data):
        indent = self.html_indent()
        settings = ['bold', 'underline']
        lvl = formatting['level']
        ret_val = self.html_open_tag("heading", False).replace('<h',f'<h{lvl}')

        for option in settings:
            ret_val += self.open_tags[option] if formatting[option] else ""

        ret_val += data

        for option in reversed(settings):
            ret_val += self.close_tags[option] if formatting[option] else ""
        ret_val += self.close_tags["heading"].replace('</h',f'</h{lvl}')
        return ret_val

    def html_hr(self):
        indent = self.html_indent()
        return f"{indent}<hr>\n"

    def html_list_item(self, data: str):
        indent = self.html_indent()
        li = f"{indent}<li>{data}</li>\n"
        return li

    def html_open_tag(self, tag_key: str, indent: bool = True, options: List[str] = None):
        ind = self.html_indent()

        if tag_key.upper() == "NONE":
            return ""

        opts = " ".join(options) if options else self.default_opts[tag_key]
        tag = self.open_tags[tag_key].format(opts)
        ret_val = ind + tag
        if indent:
            self.html_incr_indent()
        return ret_val

    def html_close_tag(self, tag_type: str):
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
