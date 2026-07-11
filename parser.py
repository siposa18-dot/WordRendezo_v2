import re
from models import Block

# Feladatcím felismerése
PATTERN = re.compile(
    r"^(20\d{2})\.(felvételi|pótfelvételi2|pótfelvételiúj|pótfelvételi ?)"
)


def read_blocks(doc):
    """
    Kiolvassa a dokumentumból a feladatblokkokat.

    Visszatér:
        list[Block]
    """

    blocks = []

    para_count = doc.Paragraphs.Count

    # 1. blokkkezdetek keresése
    for i in range(1, para_count + 1):

        p = doc.Paragraphs(i)

        txt = p.Range.Text.strip().replace("\r", "")

        m = PATTERN.match(txt)

        if not m:
            continue

        blocks.append(
            Block(
                year=int(m.group(1)),
                kind=m.group(2).replace(" ", ""),
                title=txt,

                start_para=i,
                end_para=0,

                start_char=p.Range.Start,
                end_char=0,
            )
        )

    # 2. blokkvégek meghatározása
    for i in range(len(blocks)):

        if i == len(blocks) - 1:

            blocks[i].end_para = para_count
            blocks[i].end_char = doc.Content.End

        else:

            next_para = doc.Paragraphs(blocks[i + 1].start_para)

            blocks[i].end_para = blocks[i + 1].start_para - 1
            blocks[i].end_char = next_para.Range.Start

    return blocks


def print_blocks(blocks):

    print()

    print("=" * 80)

    for b in blocks:

        print(
            f"{b.year} "
            f"{b.kind:15} "
            f"P:{b.start_para:3}-{b.end_para:3}   "
            f"C:{b.start_char:6}-{b.end_char:6}"
        )

    print("=" * 80)