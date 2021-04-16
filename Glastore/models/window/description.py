

class WindowDescriptionExtractor:

    def __init__(self, description):
        self.full_description = description

    def get_window_descriptions(self):
        self.window_descriptions = {}
        for i, description_start in enumerate(self.start_of_descriptions):
            self.current_description_start = description_start
            self.current_description_index = i
            self.add_window_description()
        window_descriptions = turn_dict_to_list(self.window_descriptions)

        return window_descriptions

    def add_window_description(self):
        window_description = self.get_current_window_description()
        self.save_window_description(window_description)

    def get_current_window_description(self):
        self.current_description = self.get_basic_window_description()
        self.handle_extended_window_descriptions()

        return self.current_description

    def get_basic_window_description(self):
        if self.is_last_description():
            window_description = self.full_description[self.current_description_start:]
        else:
            window_description = self.make_not_last_window()

        return window_description

    def save_window_description(self, window_description):
        prev_description = self.get_previous_window_description()
        if is_extended_description(prev_description) is False:
            self.window_descriptions[self.current_description_index] = window_description

    def get_previous_window_description(self):
        prev_description_index = self.current_description_index - 1
        try:
            prev_description = self.window_descriptions[prev_description_index]
        except KeyError:
            prev_description = ""

        return prev_description

    def is_last_description(self):
        return self.current_description_index == len(self.start_of_descriptions) - 1

    def make_not_last_window(self):
        next_description_start_index = self.current_description_index + 1
        next_description_start = self.start_of_descriptions[next_description_start_index]
        window_description = self.full_description[
            self.current_description_start:next_description_start]
        
        return window_description

    def handle_extended_window_descriptions(self):
        if is_extended_description(self.current_description):
            self.extend_window_description()

    def extend_window_description(self):
        try:
            extended_window_index = self.current_description_index + 2
            next_description_start = self.start_of_descriptions[extended_window_index]
            self.current_description = self.full_description[
                self.current_description_start:next_description_start]
        except IndexError:
            self.current_description = self.full_description[self.current_description_start:]

    @property
    def start_of_descriptions(self):
        return WindowIdentifierIndexExtractor(self.full_description).get_window_identifier_indexes()


class WindowIdentifierIndexExtractor:

    def __init__(self, description):
        self.full_description = description
        self.window_identifiers = [
            "dos",
            "tres",
            "antepecho",
            "fija",
            "fijo",
            "corrediza",
            "abatible",
            "guillotina"
        ]

    def get_window_identifier_indexes(self):
        identifier_indexes = self.get_all_identifier_indexes()
        if len(identifier_indexes) == 0:
            identifier_indexes.append(0)

        return sorted(identifier_indexes)

    def get_all_identifier_indexes(self):
        self.all_identifier_indexes = []
        for identifier in self.window_identifiers:
            identifier_indexes = self.get_identifier_indexes(identifier)
            self.add_identifier_indexes(identifier_indexes)

        return self.all_identifier_indexes

    def add_identifier_indexes(self, identifier_indexes):
        for identifier_index in identifier_indexes:
            self.all_identifier_indexes.append(identifier_index)

    def get_identifier_indexes(self, identifier):
        win_type_count = self.full_description.count(identifier)
        self.start_of_search = 0
        self.identifier_indexes = []
        for _ in range(win_type_count):
            identifier_index = self.get_identifier_index(identifier)
            self.add_identifier_index(identifier_index)

        return self.identifier_indexes

    def get_identifier_index(self, identifier):
        identifier_index = self.full_description.find(
            identifier, self.start_of_search
        )
        return identifier_index

    def add_identifier_index(self, identifier_index):
        if identifier_index != -1:
            self.identifier_indexes.append(identifier_index)
            self.start_of_search = identifier_index + 1


def is_extended_description(description):
    extended_descriptors = [
        "dos",
        "antepecho",
        "tres"
    ]
    for descriptor in extended_descriptors:
        if descriptor in description:
            return True
    return False


def turn_dict_to_list(some_dict):
    return [some_dict[key] for key in some_dict]
