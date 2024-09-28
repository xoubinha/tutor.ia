import html
import logging
import io

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentTable, ContentFormat
from azure.core.credentials import AzureKeyCredential
from pydantic.dataclasses import dataclass
from typing import List

from .content_management import Page

logger = logging.getLogger("ingester")


@dataclass(config=dict(arbitrary_types_allowed=True))
class DocumentAnalysisParser:
    """
    Concrete parser backed by Azure AI Document Intelligence that can parse many document formats into pages
    """

    endpoint: str
    credential: AzureKeyCredential
    model_id: str = "prebuilt-layout"

    def parse(self, content: io.BufferedReader) -> List[Page]:
        logger.info(
            "Extracting text from '%s' using Azure Document Intelligence", content.name
        )

        document_intelligence_client = DocumentIntelligenceClient(
            endpoint=self.endpoint, credential=self.credential
        )
        poller = document_intelligence_client.begin_analyze_document(
            model_id=self.model_id,
            analyze_request=content,
            content_type="application/octet-stream",
        )
        doc_intelligence_results = poller.result()

        offset = 0
        pages = []
        for page_num, page in enumerate(doc_intelligence_results.pages):
            tables_on_page = DocumentAnalysisParser.find_tables_on_page(
                doc_intelligence_results, page_num
            )
            table_chars, page_offset = DocumentAnalysisParser.generate_table_chars(
                tables_on_page, page
            )
            page_text = DocumentAnalysisParser.generate_page_text(
                doc_intelligence_results, page_offset, table_chars, tables_on_page
            )
            pages.append(Page(page_num=page_num, offset=offset, text=page_text))
            offset += len(page_text)
        return pages

    @classmethod
    def table_to_html(cls, table: DocumentTable):
        table_html = "<table>"
        rows = [
            sorted(
                [cell for cell in table.cells if cell.row_index == i],
                key=lambda cell: cell.column_index,
            )
            for i in range(table.row_count)
        ]
        for row_cells in rows:
            table_html += "<tr>"
            for cell in row_cells:
                tag = (
                    "th"
                    if (cell.kind == "columnHeader" or cell.kind == "rowHeader")
                    else "td"
                )
                cell_spans = ""
                if cell.column_span is not None and cell.column_span > 1:
                    cell_spans += f" colSpan={cell.column_span}"
                if cell.row_span is not None and cell.row_span > 1:
                    cell_spans += f" rowSpan={cell.row_span}"
                table_html += f"<{tag}{cell_spans}>{html.escape(cell.content)}</{tag}>"
            table_html += "</tr>"
        table_html += "</table>"
        return table_html

    @classmethod
    def find_tables_on_page(cls, doc_intelligence_results, page_num):
        tables_on_page = [
            table
            for table in (doc_intelligence_results.tables or [])
            if table.bounding_regions
            and table.bounding_regions[0].page_number == page_num + 1
        ]
        return tables_on_page

    @classmethod
    def generate_table_chars(cls, tables_on_page, page):
        page_offset = page.spans[0].offset
        page_length = page.spans[0].length
        table_chars = [-1] * page_length
        for table_id, table in enumerate(tables_on_page):
            for span in table.spans:
                for i in range(span.length):
                    idx = span.offset - page_offset + i
                    if idx >= 0 and idx < page_length:
                        table_chars[idx] = table_id
        return table_chars, page_offset

    @classmethod
    def generate_page_text(
        cls, doc_intelligence_results, page_offset, table_chars, tables_on_page
    ):
        page_text = ""
        added_tables = set()
        for idx, table_id in enumerate(table_chars):
            if table_id == -1:
                page_text += doc_intelligence_results.content[page_offset + idx]
            elif table_id not in added_tables:
                page_text += DocumentAnalysisParser.table_to_html(
                    tables_on_page[table_id]
                )
                added_tables.add(table_id)
        return page_text
