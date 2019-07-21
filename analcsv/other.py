import csv
from collections import Counter, defaultdict


class BaseStats(object):
    pass


class SourceStats(BaseStats):
    def __init__(self, file, delimiter="|"):
        # TODO: Throw if file is not file-like object. Validate.
        self._file = file
        self._csv = csv.DictReader(self._file, delimiter=delimiter)
        self.counter = Counter()
        self.column_counters = defaultdict(Counter)

    # TODO: Create decorator to reset file position?
    def __reset_file_cursor(self):
        pass

    """ TODO: Allow for many instances of this class to be run in threads.
    Would be cool if we allow for many instances of this class can be created
    (i.e. many files), and then be able to actually do the processing of the files
    (i.e. call the func) all at the same time, via threads.
    """

    def read(self):
        for line in self._csv:
            self.counter["total_rows"] += 1
            for k, v in line.items():
                if v:
                    self.column_counters[k]["populated"] += 1

    @property
    def header(self):
        return self._csv.fieldnames

    def count_column(self, search_term, target_column=""):
        counter = Counter()
        column_counters = defaultdict(Counter)
        for line in self._csv:
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
