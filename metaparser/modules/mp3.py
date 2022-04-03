from typing import Any
from typing import List

import eyed3
import eyed3.mp3

from .base import BaseParser
from .constants import FIELD_PUBLISHER, FIELD_ARTIST, FIELD_ALBUM, FIELD_ALBUM_ARTIST, FIELD_TITLE, FIELD_TRACK_NUM, \
    FIELD_GENRE, FIELD_COMPOSER


class Mp3Parser(BaseParser):
    @staticmethod
    def supported_mimes() -> List[str]:
        return ["audio/mpeg"]

    def __init__(self) -> None:
        super().__init__()
        self.tag = None

    def parse(self, filename: str) -> None:
        audiofile = eyed3.load(filename)
        self.tag = audiofile.tag

    def get_fields(self) -> List[str]:
        return [FIELD_PUBLISHER, FIELD_ARTIST, FIELD_ALBUM, FIELD_ALBUM_ARTIST, FIELD_TITLE, FIELD_TRACK_NUM,
                FIELD_GENRE, FIELD_COMPOSER]

    def edit_field(self, field: str, value: Any) -> None:
        if field not in self.get_fields():
            raise KeyError("Field not present in parser")
        setattr(self.tag, field, value)
        self.tag.save()

    def scrape(self):
        for field in self.get_fields():
            setattr(self.tag, field, None)
            self.tag.save()
