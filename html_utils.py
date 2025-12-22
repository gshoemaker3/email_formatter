open_para = '<p>'
close_para = '</p>'
line_break = '<br>'
open_heading = '<h{}>'
close_heading = '</h{}>'
horz_rule = '<hr>'
pre_open = '<pre>'
pre_close = '</pre>'
bold_o = '<b>'
bold_c = '</b>'
hl_open = '<mark>'
hl_close = '</mark>'
strk_open = '<del>'
strk_close = '</del>'
ss_open = '<sub>'
subs_close = '</sub>'
sups_open = '<sup>'
sups_close = '</sup>'

# description list tags
dsc_lst_o = '<dl>'
dsc_lst_c = '</dl>'
# description term tags
def_trm_o = '<dt>'
def_trm_c = '</dt>'
# describe term tags
des_trm_o = '<dd>'
des_trm_c = '</dd>'
# unordered list tags
ul_o = '<ul>'
ul_c = '</ul>'
# order list tags
ol_o = '<ol>'
ol_c = '</ol>'
# list items tags
li_o = '<li>'
li_c = '</li>'

tab_size = 0

def html_indent():
    tabs = " " * tab_size
    return tabs

def html_heading(lvl, data):
    indent = html_indent()
    snippet = f"""{indent}<h{lvl}>{bold_o}{data}{bold_c}</h{lvl}>\n"""
    return snippet

def html_hr(data):
    indent = html_indent()
    return f"{data}{indent}<hr>\n"

def html_paragraph(section):
    indent = html_indent()
    return f"{indent}<p>{section}</p>\n"


def html_list(section, list_type="ul"):
    h_list = None
    indent = html_indent()
    if list_type == "ul":  
        h_list = f"<ul>\n{section}</ul>\n"
    elif list_type == "ol":
        h_list = f"<ol>\n{section}</ol>\n"
    elif list_type == "dl":
        h_list = f"<dl>\n{section}<dl>\n"
    else:
        raise AttributeError("The list_type provided is invalid")
    return h_list


def html_list_item(data: str):
    indent = html_indent()
    li = f"{indent}<li>{data}</li>\n"
    return li


def html_tbl(data: str):
    indent = html_indent()
    settings = 'width="100%" border="0" cellpadding="10" cellspacing="0"'
    tbl= f"{indent}<table {settings}>\n{data}{indent}</table>\n"
    return tbl


def html_tbl_row(data: str):
    indent = html_indent()
    tr = f"{indent}<tr>\n{data}{indent}</tr>\n"
    return tr


def html_tbl_data(data: str):
    indent = html_indent()
    td = f'{indent}<td valign="top">\n{data}{indent}</td>\n'
    return td

def html_open_tag(tag_type: str):
    # get tag
    # add it to return value
    # increment tab size
    # return return value
    pass

def html_close_tag(tag_type: str):
    # get tag
    # decrement tab size
    # return close tag
    pass
def html_incr_indent():
    tab_size += 4

def html_decr_indent():
    tab_size -= 4
