import json
import os

class InMemoryDB:
    po_records = []

    @classmethod
    def load_data(cls, filepath):
        # Load PO data from a JSON file
        try:
            with open(filepath, 'r') as f:
                cls.po_records = json.load(f)
        except Exception as e:
            print(f"Error loading PO data from {filepath}: {e}")
            cls.po_records = []

    @classmethod
    def get_all(cls):
        return cls.po_records

    @classmethod
    def get_by_po_number(cls, po_number):
        for record in cls.po_records:
            if record.get("po_number") == po_number:
                return record
        return None