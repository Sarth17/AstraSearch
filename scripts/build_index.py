import json
from src.utils.config import SIMPLEWIKI_XML
from src.parser.wiki_parser import parse_wikipedia_dump
from src.preprocessing.cleaner import clean_wiki_text
from src.preprocessing.tokenizer import tokenize
from src.indexer.inverted_index import InvertedIndex
from src.indexer.index_writer import write_index
from src.storage.document_store import DocumentStore
from src.utils.config import (
    RAW_DATA_DIR,
    INVERTED_INDEX_PATH,
    DOCUMENT_STORE_PATH,
    METADATA_PATH
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    index = InvertedIndex()
    doc_store = DocumentStore()
    total_docs = 0

    xml_path = SIMPLEWIKI_XML

    logger.info("Starting indexing process")

    for doc_id, title, raw_text in parse_wikipedia_dump(xml_path):
        clean_text = clean_wiki_text(raw_text)
        tokens = tokenize(clean_text)

        if not tokens:
            continue

        index.add_document(doc_id, tokens)
        doc_store.add(doc_id, title)
        total_docs += 1

        if total_docs % 1000 == 0:
            logger.info(f"Indexed {total_docs} documents")

    # Write index to disk
    write_index(index, INVERTED_INDEX_PATH)
    doc_store.save(DOCUMENT_STORE_PATH)

    # Write metadata
    metadata = {"total_docs": total_docs}
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f)

    logger.info("Indexing completed successfully")
    logger.info(f"Total documents indexed: {total_docs}")
    print("XML path:", xml_path)
    print("Exists:", xml_path.exists())


if __name__ == "__main__":
    main()
