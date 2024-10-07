from services.index_service import create_or_update_index
from services.datasource_service import create_or_update_datasource
from services.skillset_service import create_or_update_skillset
from services.indexer_service import create_or_update_indexer

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    create_or_update_index()
    create_or_update_datasource()
    create_or_update_skillset()
    create_or_update_indexer()


if __name__ == "__main__":
    main()
