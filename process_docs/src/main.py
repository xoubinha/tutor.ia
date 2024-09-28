import os
import re
from typing import List

from features.parsers import DocumentAnalysisParser, Section, File
from features.splitters import SentenceTextSplitter
from features.configuration import get_app_settings
from features.storage import AzureStorageAccount
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


def parse_file(
    file: File, parser: DocumentAnalysisParser, splitter: SentenceTextSplitter
) -> List[Section]:
    pages = [
        page
        for page in parser.parse(
            content=file.content,
        )
    ]
    sections = [
        Section(split_page, content=file) for split_page in splitter.split_pages(pages)
    ]
    return sections


def main():
    settings = get_app_settings()
    docintelligence_endpoint = settings.docintelligence_api_endpoint
    docintelligence_api_key = settings.docintelligence_api_key

    storage_account_name = settings.storage_account_name
    storage_account_container = settings.storage_account_container
    storage_account_connection_string = settings.storage_account_connection_string

    parser = DocumentAnalysisParser(
        docintelligence_endpoint, AzureKeyCredential(docintelligence_api_key)
    )
    splitter = SentenceTextSplitter()

    storage_account = AzureStorageAccount(
        storage_account_name,
        storage_account_container,
        storage_account_connection_string,
    )

    files = storage_account.download_files()
    files = [files[0], files[1]]

    for file in files:
        sections = parse_file(file, parser, splitter)
        print(file.filename())
        if sections:
            MAX_BATCH_SIZE = 1000
            section_batches = [
                sections[i : i + MAX_BATCH_SIZE]
                for i in range(0, len(sections), MAX_BATCH_SIZE)
            ]

            print(len(section_batches))
            for batch_index, batch in enumerate(section_batches):
                for section_index, section in enumerate(batch):
                    document = {
                        "id": f"{section.content.filename_to_id()}-page-{section_index + batch_index * MAX_BATCH_SIZE}",
                        "subject": file.url.split("/")[6],
                        "type": file.url.split("/")[7],
                        "storage_url": file.url,
                        "title": section.content.filename(),
                        "chapter": "",
                        "section": "",
                        "page": str(section.split_page.page_num),
                        "content": re.sub(
                            r"<[^>]*>|<!--.*?-->|\\n+",
                            " ",
                            section.split_page.text,
                            flags=re.DOTALL,
                        )
                        .strip()
                        .replace("\n", " "),
                    }
                    storage_account.upload_blob(
                        data=document,
                        blob_name=f"{ "/".join(file.url.split("/")[4:7])}/processed/{section.content.filename()}-{section_index}-parsed.json",
                    )
            #     documents = [
            #         {
            #             "id": f"{section.content.filename_to_id()}-page-{section_index + batch_index * MAX_BATCH_SIZE}",
            #             "subject": file.url.split("/")[6],
            #             "type": file.url.split("/")[7],
            #             "storage_url": file.url,
            #             "title": section.content.filename(),
            #             "chapter": "",
            #             "section": "",
            #             "page": str(section.split_page.page_num),
            #             "content": re.sub(
            #                 r"<[^>]*>|<!--.*?-->|\\n+",
            #                 " ",
            #                 section.split_page.text,
            #                 flags=re.DOTALL,
            #             )
            #             .strip()
            #             .replace("\n", " "),
            #         }
            #         for section_index, section in enumerate(batch)
            #     ]
            # storage_account.upload_blob(
            #     data=documents,
            #     blob_name=f"{ "/".join(file.url.split("/")[4:7])}/processed/{file.filename()}-parsed.json",
            # )


if __name__ == "__main__":
    main()
