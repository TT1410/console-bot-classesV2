from typing import Optional, Generator
from collections import UserDict

from .record import Record


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def iterator(self, count: int = 0) -> 'Generator[list[Record]]':
        records = []

        count = count if count else len(self.data)

        for record in self.data.values():

            if len(records) >= count:
                yield records
                records = []

            records.append(record)

        if records:
            yield records

    def __repr__(self):
        return "AddressBook({})".format(', '.join([f"{k}={v}" for k, v in self.__dict__.items()]))
