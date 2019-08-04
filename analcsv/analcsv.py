import csv
import logging
import pprint
from argparse import ArgumentParser
from collections import Counter, defaultdict


def sniff_dialect(args, line_count=None):
    lines = ""
    with open(args.source, encoding=args.file_encoding, newline="") as f:
        for line_number, line in enumerate(f):
            if line_count and line_number >= line_count:
                break
            else:
                lines += line
    return csv.Sniffer().sniff(lines, args.dialect_delimiter)


def command_count(args):
    counter = Counter()
    columns_store = defaultdict(set)
    if args.column is not None:
        for column in args.column:
            columns_store[column] = set()  # For tracking unique values
    print(columns_store)
    with open(args.source, encoding=args.file_encoding, newline="") as f:
        csv_reader = csv.DictReader(f, dialect=args.dialect)
        for row in csv_reader:
            counter["total/rows"] += 1
            for column_name, column_set in columns_store.items():
                if column_name in row:
                    column_set.add(row[column_name])

    for column_name, column_set in columns_store.items():
        counter[f"total/uniques_{column_name}"] = len(column_set)

    return counter


if __name__ == "__main__":
    # argparse
    available_dialects = ",".join(csv.list_dialects())
    epilog = f"""Available predefined dialects:
    {', '.join(csv.list_dialects())}.
    Available special dialect options:
    sniff (attempts to figure out the dialect from sample of file content;
    dialect-delimiter option is used),
    custom (manually builds dialect using dialect-* options)."""
    parser = ArgumentParser(epilog=epilog)
    subparsers = parser.add_subparsers(dest="command")

    parser.add_argument("source", type=str)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument("--file_encoding", type=str, default="utf-8")
    parser.add_argument("--dialect", type=str, default="sniff")
    parser.add_argument("--dialect_delimiter", type=str)

    parser_count = subparsers.add_parser("count")
    parser_count.add_argument("-c", "--column", action="append", type=str)

    args = parser.parse_args()
    print(f"{args}")

    if args.dialect == "sniff":
        args.dialect = sniff_dialect(args, 50)
    elif args.dialect == "custom":
        raise NotImplementedError("'custom' as a dialect value.")
        # TODO: Manually create dialect object from passed dialect-* parameters

    # Logging
    if args.verbose >= 1:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Work
    if args.command == "count":
        result = command_count(args)
        report = pprint.pformat(result)
        logger.info(f"{report}")
    else:
        logger.error("No matching command.")
