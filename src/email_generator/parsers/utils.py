from pathlib import Path
from typing import List


def get_files(dir: str, exts: List[str] = None) -> List[Path]:
    """ This method retrieves all yaml files stored in the
        config directory.
    
        Args:
            - dir: the file path of the directory that contains desired files.
            - exts: A list of desired file extensions form the user.
        Return:
            - A list of file names.
    """
    print(dir)
    config_dir = Path(dir)
    if exts:
        exts = set(exts)
        return [item for item in config_dir.iterdir() if item.is_file() and item.suffix in exts]
    return [item for item in config_dir.iterdir() if item.is_file()]