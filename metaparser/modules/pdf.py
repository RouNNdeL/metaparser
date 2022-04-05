from typing import List, Dict, Any

from PyPDF2 import PdfFileReader, PdfFileMerger

from .base import BaseParser

FIELD_DISCLAIMER = "You can specify your own fields. Make sure they start with /"
FIELD_TITLE = "/Title"
FIELD_AUTHOR = "/Author"
FIELD_SUBJECT = "/Subject"
FIELD_KEYWORD = "/Keyword"
FIELD_CREATED_DATE = "/Created Date"
FIELD_MODIFIED_DATE = "/Modified Date"
FIELD_CREATOR = "/Creator"
FIELD_PRODUCER = "/Producer"
FIELD_TRAPPED = "/Trapped"



class PDFParser(BaseParser):
    def get_fields(self) -> List[str]:
        return [
            FIELD_DISCLAIMER,
            FIELD_TITLE,
            FIELD_AUTHOR,
            FIELD_SUBJECT,
            FIELD_KEYWORD,
            FIELD_CREATED_DATE,
            FIELD_MODIFIED_DATE,
            FIELD_CREATOR,
            FIELD_PRODUCER,
            FIELD_TRAPPED
        ]

    @staticmethod
    def supported_mimes() -> List[str]:
        return ["application/pdf", "application/pdf-x"]

    def __init__(self) -> None:
        super().__init__()
        metadata = None
        filename = None

    def parse(self, filename: str) -> None:
        self.filename = filename
        metadata = PdfFileReader(filename).getDocumentInfo()
        self.metadata = {}
        for field in metadata:
            self.metadata[field] = metadata[field]

    def set_field(self, field: str, value: Any) -> None:
        if not field.startswith("/"):
            raise ValueError("Bad name for field")
        self.metadata[field] = value
        self.write()

    def write(self) -> None:
        pdf_merger = PdfFileMerger()
        pdf_merger.append(self.filename)
        pdf_merger.addMetadata(self.metadata)
        pdf_merger.write(self.filename)

    def get_all_values(self) -> Dict[str, str]:
        return self.metadata
