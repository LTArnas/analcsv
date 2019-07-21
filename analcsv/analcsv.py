import csv
import locale
import logging
from string import Template
from collections import Counter, defaultdict
from argparse import ArgumentParser, FileType

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def display(source):
    logger.info("{:-^50}".format(" Basic "))
    for k, v in source.counter.items():
        if k == "total_rows":
            logger.info("{}: {:,}".format("Total rows", v))
        else:
            logger.info("{}: {}".format(k, v))
    # logger.info("{:-<50}".format(""))

    logger.info("{:-^50}".format(" Columns "))
    for column, counter in source.column_counters.items():
        logger.info("{:_^50}".format(column))

        logger.info(
            "{:^10} - {:^10} / {:^10} ({:^10})".format(
                "STAT", "COUNT", "TOTAL ROWS", "DIFFERENCE"
            )
        )

        for k, v in counter.items():
            logger.info(
                "{:^10} - {:^10,} / {:^10,} ({:^10,})".format(
                    k, v, source.counter["total_rows"], source.counter["total_rows"] - v
                )
            )


def read(self):
    for line in self._csv:
        self.counter["total_rows"] += 1
        for k, v in line.items():
            if v:
                self.column_counters[k]["populated"] += 1


def count_total_rows(file, delimiter="|"):
    c = Counter()
    with open(file, "r") as f:
        csv_reader = csv.DictReader(f, delimiter=delimiter)
        for line in csv_reader:
            c["ctr"] += 1
    return c


def tester(file, delimiter="|"):
    c = Counter()
    with open(file, "r") as f:
        csv_reader = csv.DictReader(f, delimiter=delimiter)
        for line in csv_reader:
            c["tester"] += 1
    return c


def count_column(csv, search_term, target_column=""):
    counter = Counter()
    column_counters = defaultdict(Counter)
    for line in csv:
        line_matched = False
        for k, v in line.items():
            if search_term in v:
                counter["total_field_matches"] += 1
                column_counters[k]["substring_match"] += 1
                if search_term == v:
                    column_counters[k]["exact_match"] += 1
                if not line_matched:
                    counter["line_matches"] += 1
                    line_matched = True
    return counter, column_counters


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("source", type=str)
    parser.add_argument("-d", "--delimiter", type=str, default="|")
    parser.add_argument("-e", "--encoding", type=str, default="utf-8")
    args = parser.parse_args()

    c = tester(args.source)
    c2 = count_total_rows(args.source)
    print(c)
    print(c2)
    """
    with open(args.source, encoding=args.encoding) as f:
        s = SourceStats(f, delimiter=args.delimiter)
        c, cc = s.count_column("hi")
        s.read()
        print(type(c), type(cc))
        for i in c.items():
            print(i)
        for i in cc.items():
            print(i)
        logger.info("{:=^50}".format(" Result "))
        display(s)
    """
