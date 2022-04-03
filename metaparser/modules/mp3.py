from typing import Any, List

import eyed3  # type: ignore
import eyed3.mp3  # type: ignore

from .base import BaseParser
from .constants import (FIELD_ALBUM, FIELD_ALBUM_ARTIST, FIELD_ALBUM_TYPE,
                        FIELD_ARTIST, FIELD_ARTIST_ORIGIN, FIELD_ARTIST_URL,
                        FIELD_AUDIO_FILE_URL, FIELD_AUDIO_SOURCE_URL,
                        FIELD_BEST_RELEASE_DATE, FIELD_BPM, FIELD_CD_ID,
                        FIELD_COMMERCIAL_URL, FIELD_COMPOSER, FIELD_COPYRIGHT,
                        FIELD_COPYRIGHT_URL, FIELD_ENCODED_BY,
                        FIELD_ENCODING_DATE, FIELD_GENRE,
                        FIELD_INTERNET_RADIO_URL, FIELD_ORIGINAL_ARTIST,
                        FIELD_ORIGINAL_RELEASE_DATE, FIELD_PAYMENT_URL,
                        FIELD_PLAY_COUNT, FIELD_PUBLISHER, FIELD_PUBLISHER_URL,
                        FIELD_READ_ONLY, FIELD_RECORDING_DATE,
                        FIELD_RELEASE_DATE, FIELD_TAGGING_DATE,
                        FIELD_TERMS_OF_USE, FIELD_TITLE, FIELD_TRACK_NUM)


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
                FIELD_GENRE, FIELD_COMPOSER, FIELD_ALBUM_TYPE, FIELD_ARTIST_ORIGIN, FIELD_ARTIST_URL,
                FIELD_AUDIO_FILE_URL, FIELD_AUDIO_SOURCE_URL,
                FIELD_BEST_RELEASE_DATE, FIELD_BPM, FIELD_CD_ID, FIELD_COMMERCIAL_URL, FIELD_COPYRIGHT,
                FIELD_COPYRIGHT_URL, FIELD_ENCODED_BY,
                FIELD_ENCODING_DATE, FIELD_INTERNET_RADIO_URL, FIELD_ORIGINAL_ARTIST, FIELD_ORIGINAL_RELEASE_DATE,
                FIELD_PAYMENT_URL, FIELD_PLAY_COUNT,
                FIELD_PUBLISHER_URL, FIELD_READ_ONLY, FIELD_RECORDING_DATE, FIELD_RELEASE_DATE, FIELD_TAGGING_DATE,
                FIELD_TERMS_OF_USE]

    def edit_field(self, field: str, value: Any) -> None:
        if self.tag is None:
            raise TypeError("Tag is null, parse the file first")
        if field not in self.get_fields():
            raise KeyError("Field not present in parser")
        setattr(self.tag, field, value)
        self.tag.save()

    def scrape(self):
        self.tag.clear()
        self.tag.save()

    def print(self):
        print("Showing ID3 version" + ": " + ".".join([str(num) for num in getattr(self.tag, "version", None)]))
        print("Showing only not None fields")
        print("-------------------------------------")
        for field in self.get_fields():
            value = getattr(self.tag, field, None)
            if value is not None:
                print(field + ": " + str(value))
        print("-------------------------------------")
