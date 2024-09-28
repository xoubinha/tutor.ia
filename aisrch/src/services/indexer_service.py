import logging
from azure.core.exceptions import ResourceExistsError

from clients.indexer_client import get_indexer_client
from models.indexer_definition import get_indexer_schema


def create_or_update_indexer():
    client = get_indexer_client()
    indexer = get_indexer_schema()
    try:
        client.create_indexer(indexer)
        print(f"Indexer '{indexer.name}' created.")
    except ResourceExistsError:
        client.create_or_update_index(indexer)
        logging.info(f"Indexer '{indexer.name}' updated.")
    except Exception as e:
        logging.error(f"Failed to create or update indexer '{indexer.name}': {e}")
