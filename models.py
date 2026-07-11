from dataclasses import dataclass

@dataclass
class Block:
    year: int
    kind: str
    title: str

    start_para: int
    end_para: int

    start_char: int
    end_char: int

    @property
    def sort_key(self):

        order = {
    "felvételi": 0,
    "pótfelvételi": 1,
    "pótfelvételiúj": 2,
    "pótfelvételi2": 3,
}

        return (
            -self.year,
            order.get(self.kind, 99),
        )