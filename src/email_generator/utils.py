import datetime

def keyword_replace(line: str):
        """ This method looks for keywords and replaces them with their actual values.
        
            A keyword follows the following structure: <KEYWORD>.
        """
        curr_date = datetime.date.today()
        keywords = {"<DATE>": f"({curr_date})"}
        
        # replacement
        for kw, val in keywords.items():
            print(f"line: {line}")
            print(f"replacement: {val}")
            line = line.replace(kw, val)
        print(f"line after replacement: {line}")
        return line