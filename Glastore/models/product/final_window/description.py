
window_identifiers = [
    "dos",
    "tres",
    "antepecho",
    "fija",
    "fijo",
    "corrediz",
    "abatible",
    "oscilobatiente",
    "guillotina"
]


class SubWindowDescriptionGetter:

    def __init__(self, description):
        self.full_description = description.lower()

    def get_window_descriptions(self):
        self.window_descriptions = {}
        for i, description_start in enumerate(self.description_indexes):
            self.current_description_start = description_start
            self.current_description_index = i
            self.add_window_description()
        window_descriptions = turn_dict_to_list(self.window_descriptions)

        return window_descriptions

    def add_window_description(self):
        if self.current_description_is_part_of_antepecho() is False:
            self.save_current_window_description()

    def save_current_window_description(self):
        self.window_descriptions[self.current_description_index] = self.current_window_description

    def current_description_is_part_of_antepecho(self):
        prev_description = self.previous_window_description
        if "antepecho" in prev_description:
            return self.is_composed_antepecho(prev_description)
        return False

    def is_composed_antepecho(self, description):
        for win_identifier in window_identifiers:
            if f"antepecho {win_identifier}" in description:
                return True
        return False

    @property
    def current_window_description(self):
        self.current_description = self.get_basic_window_description()
        self.handle_extended_window_description()

        return self.current_description

    def get_basic_window_description(self):
        if self.is_last_description():
            window_description = self.make_last_description()
        else:
            window_description = self.make_not_last_description()

        return window_description

    def is_last_description(self):
        return self.current_description_index == len(self.description_indexes) - 1

    def make_last_description(self):
        return self.full_description[self.current_description_start:]

    def make_not_last_description(self):
        next_description_start_index = self.current_description_index + 1
        next_description_start = self.description_indexes[next_description_start_index]
        window_description = self.full_description[
            self.current_description_start:next_description_start]

        return window_description

    def handle_extended_window_description(self):
        if self.is_extended_description(self.current_description):
            self.extend_window_description()

    def is_extended_description(self, description):
        extended_descriptors = [
            "dos",
            "tres"
        ]
        for descriptor in extended_descriptors:
            if descriptor in description:
                return True
        if description == "antepecho ":
            return True

        return False

    def extend_window_description(self):
        try:
            extended_description_index = self.current_description_index + 2
            next_description_start = self.description_indexes[extended_description_index]
            current_description_start = self.current_description_start
            self.current_description = self.full_description[
                current_description_start:next_description_start
            ]
        except IndexError:
            self.current_description = self.full_description[self.current_description_start:]

    @property
    def previous_window_description(self):
        prev_description_index = self.current_description_index - 1
        try:
            prev_description = self.window_descriptions[prev_description_index]
        except KeyError:
            prev_description = ""

        return prev_description

    @property
    def description_indexes(self):
        sub_win_description_index = SubWindowDescriptionIndexGetter(self.full_description)

        return sub_win_description_index.get_window_description_indexes()


class SubWindowDescriptionIndexGetter:

    def __init__(self, description):
        self.full_description = description

    def get_window_description_indexes(self):
        identifier_indexes = self.get_all_identifier_indexes()
        if len(identifier_indexes) == 0:
            identifier_indexes.append(0)
        identifier_indexes = sorted(identifier_indexes)
        identifier_indexes[0] = 0

        return identifier_indexes

    def get_all_identifier_indexes(self):
        self.all_identifier_indexes = []
        for identifier in window_identifiers:
            identifier_indexes = self.get_identifier_indexes(identifier)
            self.add_identifier_indexes(identifier_indexes)

        return self.all_identifier_indexes

    def add_identifier_indexes(self, identifier_indexes):
        for identifier_index in identifier_indexes:
            self.all_identifier_indexes.append(identifier_index)

    def get_identifier_indexes(self, identifier):
        win_type_count = self.full_description.count(identifier)
        self.start_of_search = 0
        self.current_identifier_indexes = []
        for _ in range(win_type_count):
            identifier_index = self.get_identifier_index(identifier)
            self.add_identifier_index(identifier_index)

        return self.current_identifier_indexes

    def get_identifier_index(self, identifier):
        identifier_index = self.full_description.find(
            identifier, self.start_of_search
        )
        return identifier_index

    def add_identifier_index(self, identifier_index):
        if identifier_index != -1:
            self.current_identifier_indexes.append(identifier_index)
            self.start_of_search = identifier_index + 1


def turn_dict_to_list(some_dict):
    return [some_dict[key] for key in some_dict]
