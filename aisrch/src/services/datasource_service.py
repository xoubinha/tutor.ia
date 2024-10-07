import logging
from azure.core.exceptions import ResourceExistsError

from clients.indexer_client import get_indexer_client
from models.datasource_definition import get_datasource


def create_or_update_datasource():
    client = get_indexer_client()
    datasource = get_datasource()
    try:
        client.create_data_source_connection(datasource)
        logging.info(f"Datasource '{datasource.name}' created.")
    except ResourceExistsError:
        client.create_or_update_index(datasource)
        logging.info(f"Datasource '{datasource.name}' updated.")
    except Exception as e:
        logging.error(f"Failed to create or update datasource '{datasource.name}': {e}")
