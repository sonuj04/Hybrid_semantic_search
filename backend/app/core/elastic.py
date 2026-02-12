from elasticsearch import Elasticsearch
from app.settings import settings


_es_client = None


def get_es_client():
    global _es_client
    if _es_client is None:
        _es_client = Elasticsearch(
            settings.ES_URL,
            basic_auth=(settings.ES_USERNAME, settings.ES_PASSWORD),
            ca_certs=settings.ES_CA_CERT,
        )
    return _es_client
