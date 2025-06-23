class InMemoryDB:
    po_records = []

    @classmethod
    def load_data(cls, filepath):
        from utils.load_data import get_all_po_records
        cls.po_records = get_all_po_records(filepath) or []

    @classmethod
    def get_all(cls):
        return cls.po_records

    @classmethod
    def get_by_po_number(cls, po_number):
        for record in cls.po_records:
            if record.get("po_number") == po_number:
                return record
        return None 