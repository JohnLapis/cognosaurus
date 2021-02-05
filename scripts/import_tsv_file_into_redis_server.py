import argparse
import json

import redis


def get_db(host, port):
    return redis.Redis(host=host, port=port, db=0)


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


def main(file, db_host="localhost", db_port=6379):
    rows = read_file(file)
    assert validate_columns(next(rows))

    fields = [
        "lang_1",
        "word_1",
        "lang_2",
        "word_2",
    ]

    db = get_db(db_host, db_port)
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
    parser.add_argument(
        "--host", type=str, help="Host to use to connect to database."
    )
    parser.add_argument(
        "--port", type=int, help="Port to use to connect to database."
    )
    args = parser.parse_args()
    main(args.file, args.host, args.port)
