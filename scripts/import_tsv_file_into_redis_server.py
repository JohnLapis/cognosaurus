import argparse
import json
import os

import redis


def get_db():
    return redis.Redis(host="0.0.0.0", port=os.environ["REDIS_PORT"], db=0)


def read_file(name):
    """
    Columns of file:
    concept id, lang 1, word 1, lang 2, word 2, translit 1, translit 2
    """
    with open(name, "r") as f:
        for row in f.readlines():
            yield row.strip().split("\t")[1:5]


def validate_columns(columns):
    fields = [
        "lang 1",
        "word 1",
        "lang 2",
        "word 2",
    ]
    return columns == fields


def main(file):
    rows = read_file(file)
    assert validate_columns(next(rows))

    fields = [
        "lang_1",
        "word_1",
        "lang_2",
        "word_2",
    ]

    db = get_db()
    assert db.ping()

    row_hashes = set()
    for row in rows:
        parsed_row = {field: row[i] for i, field in enumerate(fields)}

        row_hash = hash(str(parsed_row))
        if row_hash in row_hashes:
            continue

        row_hashes.add(row_hash)

        key_1 = parsed_row["lang_1"] + ":" + parsed_row["word_1"]
        db.rpush(
            f"cognate:{key_1}",
            json.dumps(
                {
                    "word": parsed_row["word_2"],
                    "lang": parsed_row["lang_2"],
                }
            ),
        )
        key_2 = parsed_row["lang_2"] + ":" + parsed_row["word_2"]
        db.rpush(
            f"cognate:{key_2}",
            json.dumps(
                {
                    "word": parsed_row["word_1"],
                    "lang": parsed_row["lang_1"],
                }
            ),
        )

    db.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates database with data from tsv file."
    )
    parser.add_argument("file", type=str, help="tsv file.")
    args = parser.parse_args()
    main(args.file)
