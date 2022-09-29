from re import search

from .field import Field


class Phone(Field):

    def __init__(self, value: str):
        super().__init__(value)
        self.value: int = value

    @Field.value.setter
    def value(self, value):
        self._value: int = self.check_phone_number(value)

    @staticmethod
    def check_phone_number(phone: str) -> int:
        clean_phone = (
                        phone.strip()
                        .removeprefix("+")
                        .replace("(", "")
                        .replace(")", "")
                        .replace("-", "")
                        .replace(" ", "")
                    )

        phone = search(r"(?:380|0)\d{9}", clean_phone)

        if not phone:
            raise ValueError(f"Phone number {clean_phone} is not valid")

        phone = phone.group()

        phone = '38' + phone if phone.startswith('0') else phone

        return int(phone)
