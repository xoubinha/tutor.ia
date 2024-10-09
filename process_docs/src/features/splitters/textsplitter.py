import logging
from abc import ABC
from typing import Generator, List

import tiktoken

from features.parsers import Page, SplitPage

logger = logging.getLogger("ingester")

ENCODING_MODEL = "text-embedding-3-large"

STANDARD_WORD_BREAKS = [",", ";", ":", " ", "(", ")", "[", "]", "{", "}", "\t", "\n"]

CJK_WORD_BREAKS = [
    "、",
    "，",
    "；",
    "：",
    "（",
    "）",
    "【",
    "】",
    "「",
    "」",
    "『",
    "』",
    "〔",
    "〕",
    "〈",
    "〉",
    "《",
    "》",
    "〖",
    "〗",
    "〘",
    "〙",
    "〚",
    "〛",
    "〝",
    "〞",
    "〟",
    "〰",
    "–",
    "—",
    "‘",
    "’",
    "‚",
    "‛",
    "“",
    "”",
    "„",
    "‟",
    "‹",
    "›",
]

STANDARD_SENTENCE_ENDINGS = [".", "!", "?"]

CJK_SENTENCE_ENDINGS = ["。", "！", "？", "‼", "⁇", "⁈", "⁉"]

bpe = tiktoken.encoding_for_model(ENCODING_MODEL)

DEFAULT_OVERLAP_PERCENT = 10
DEFAULT_SECTION_LENGTH = 1000


class TextSplitter(ABC):
    """
    Splits a list of pages into smaller chunks
    :param pages: The pages to split
    :return: A generator of SplitPage
    """

    def split_pages(self, pages: List[Page]) -> Generator[SplitPage, None, None]:
        if False:
            yield


class SentenceTextSplitter(TextSplitter):
    """
    Class that splits pages into smaller chunks. This is required because embedding models may not be able to analyze an entire page at once
    """

    def __init__(self, max_tokens_per_section: int = 500):
        self.sentence_endings = STANDARD_SENTENCE_ENDINGS + CJK_SENTENCE_ENDINGS
        self.word_breaks = STANDARD_WORD_BREAKS + CJK_WORD_BREAKS
        self.max_section_length = DEFAULT_SECTION_LENGTH
        self.sentence_search_limit = 100
        self.max_tokens_per_section = max_tokens_per_section
        self.section_overlap = int(
            self.max_section_length * DEFAULT_OVERLAP_PERCENT / 100
        )

    def split_page_by_max_tokens(
        self, page_num: int, text: str
    ) -> Generator[SplitPage, None, None]:
        """
        Recursively splits page by maximum number of tokens to better handle languages with higher token/word ratios.
        """
        tokens = bpe.encode(text)
        if len(tokens) <= self.max_tokens_per_section:
            yield SplitPage(page_num=page_num, text=text)
        else:
            start = int(len(text) // 2)
            pos = 0
            boundary = int(len(text) // 3)
            split_position = -1
            while start - pos > boundary:
                if text[start - pos] in self.sentence_endings:
                    split_position = start - pos
                    break
                elif text[start + pos] in self.sentence_endings:
                    split_position = start + pos
                    break
                else:
                    pos += 1

            if split_position > 0:
                first_half = text[: split_position + 1]
                second_half = text[split_position + 1 :]
            else:
                middle = int(len(text) // 2)
                overlap = int(len(text) * (DEFAULT_OVERLAP_PERCENT / 100))
                first_half = text[: middle + overlap]
                second_half = text[middle - overlap :]
            yield from self.split_page_by_max_tokens(page_num, first_half)
            yield from self.split_page_by_max_tokens(page_num, second_half)

    def find_page(self, pages, offset):
        num_pages = len(pages)
        for i in range(num_pages - 1):
            if offset >= pages[i].offset and offset < pages[i + 1].offset:
                return pages[i].page_num
        return pages[num_pages - 1].page_num

    def split_pages(self, pages: List[Page]) -> Generator[SplitPage, None, None]:
        all_text = "".join(page.text for page in pages)
        if len(all_text.strip()) == 0:
            return

        length = len(all_text)
        if length <= self.max_section_length:
            yield from self.split_page_by_max_tokens(
                page_num=self.find_page(pages, 0), text=all_text
            )
            return

        start = 0
        end = length
        while start + self.section_overlap < length:
            end = self.find_section_end(all_text, start, length)
            start = self.adjust_start_for_next_section(all_text, start, end)
            section_text = all_text[start:end]
            yield from self.split_page_by_max_tokens(
                page_num=self.find_page(pages, start), text=section_text
            )

            start = self.handle_unclosed_tables(pages, section_text, start, end)

        if start + self.section_overlap < end:
            yield from self.split_page_by_max_tokens(
                page_num=self.find_page(pages, start), text=all_text[start:end]
            )

    def find_section_end(self, all_text, start, length):
        last_word = -1
        end = start + self.max_section_length

        if end > length:
            end = length
        else:
            while (
                end < length
                and (end - start - self.max_section_length) < self.sentence_search_limit
                and all_text[end] not in self.sentence_endings
            ):
                if all_text[end] in self.word_breaks:
                    last_word = end
                end += 1
            if (
                end < length
                and all_text[end] not in self.sentence_endings
                and last_word > 0
            ):
                end = last_word
        if end < length:
            end += 1
        return end

    def adjust_start_for_next_section(self, all_text, start, end):
        last_word = -1
        while (
            start > 0
            and start > end - self.max_section_length - 2 * self.sentence_search_limit
            and all_text[start] not in self.sentence_endings
        ):
            if all_text[start] in self.word_breaks:
                last_word = start
            start -= 1
        if all_text[start] not in self.sentence_endings and last_word > 0:
            start = last_word
        if start > 0:
            start += 1
        return start

    def handle_unclosed_tables(self, pages, section_text, start, end):
        last_table_start = section_text.rfind("<table")
        if (
            last_table_start > 2 * self.sentence_search_limit
            and last_table_start > section_text.rfind("</table")
        ):
            logger.info(
                f"Section ends with unclosed table, starting next section with the table at page {self.find_page(pages, start)} offset {start} table start {last_table_start}"
            )
            start = min(end - self.section_overlap, start + last_table_start)
        else:
            start = end - self.section_overlap
        return start
