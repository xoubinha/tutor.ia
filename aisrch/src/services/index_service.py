import logging
from azure.core.exceptions import ResourceExistsError

from models.index_definition import get_index_schema
from clients.search_client import get_search_client


def create_or_update_index():
    client = get_search_client()
    index = get_index_schema()
    try:
        client.create_index(index)
        logging.info(f"Index '{index.name}' created.")
    except ResourceExistsError:
        client.create_or_update_index(index)
        logging.info(f"Index '{index.name}' updated.")
    except Exception as e:
        logging.error(f"Failed to create or update index '{index.name}': {e}")
