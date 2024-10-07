import logging
from azure.core.exceptions import ResourceExistsError

from clients.indexer_client import get_indexer_client
from models.skillset_definition import get_skillset


def create_or_update_skillset():
    client = get_indexer_client()
    skillset = get_skillset()
    try:
        client.create_skillset(skillset)
        logging.info(f"Skillset '{skillset.name}' created.")
    except ResourceExistsError:
        client.create_or_update_index(skillset)
        logging.info(f"Skillset '{skillset.name}' updated.")
    except Exception as e:
        logging.error(f"Failed to create or update skillset '{skillset.name}': {e}")
