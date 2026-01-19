import  json
import os

class DocumentStore:

    def __init__(self):
        self.store = {}

    def add(self, doc_id: int, title: str):

        self.store[str(doc_id)] = title

    def save(self, output_path: str):
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding="utf-8") as f:
            json.dump(self.store, f)

    @classmethod
    def load(cls, path: str):
        with open(path, "r", encoding="utf-8") as f:
            store = json.load(f)

        obj = cls()
        obj.store = store
        return obj

    def get_title(self, doc_id: int) -> str:
        return self.store.get(str(doc_id), "")        

