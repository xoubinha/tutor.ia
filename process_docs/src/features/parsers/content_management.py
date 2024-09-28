import base64
import io
import os
import re
from typing import Optional
from pydantic.dataclasses import dataclass


@dataclass(config=dict(arbitrary_types_allowed=True))
class File:
    """
    Represents a file stored in a data lake storage account
    This file might contain access control information about which users or groups can access it
    """

    content: io.BufferedReader
    url: Optional[str] = None

    def filename(self):
        return os.path.basename(self.content.name)

    def file_extension(self):
        return os.path.splitext(self.content.name)[1]

    def filename_to_id(self):
        FILENAME_SANITIZATION_PATTERN = "[^0-9a-zA-Z_-]"
        filename_ascii = re.sub(FILENAME_SANITIZATION_PATTERN, "_", self.filename())
        filename_hash = base64.b16encode(self.filename().encode("utf-8")).decode(
            "ascii"
        )
        return f"file-{filename_ascii}-{filename_hash}"

    def close(self):
        if self.content:
            self.content.close()


@dataclass
class Page:
    """
    A single page from a document

    Attributes:
        page_num (int): Page number
        offset (int): If the text of the entire Document was concatenated into a single string, the index of the first character on the page. For example, if page 1 had the text "hello" and page 2 had the text "world", the offset of page 2 is 5 ("hellow")
        text (str): The text of the page
    """

    page_num: int
    offset: int
    text: str


@dataclass
class SplitPage:
    """
    A section of a page that has been split into a smaller chunk.
    """

    page_num: int
    text: str


@dataclass
class Section:
    """
    A section of a page that is stored in a search service. These sections are used as context by Azure OpenAI service
    """

    split_page: SplitPage
    content: File
