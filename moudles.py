from elasticsearch_dsl import DocType,Text
from config import host
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=[host])

class Search(DocType):
    file = Text()
    data = Text()
    source = Text()

    class Meta:
        index = "sgk"
        doc_type = "163mail"


if __name__ == "__main__":
    Search.init()