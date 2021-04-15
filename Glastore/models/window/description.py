

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

    def save_window_description(self, window_description):
        prev_description = self.get_previous_window_description()
        if is_extended_description(prev_description) is False:
            self.window_descriptions[self.current_description_index] = window_description

    def get_current_window_description(self):
        self.current_description = self.make_basic_window_description()
        self.handle_window_repetitions()

        return self.current_description

    def make_basic_window_description(self):
        if self.is_last_window():
            window_description = self.full_description[self.current_description_start:]
        else:
            next_description_start_index = self.current_description_index + 1
            next_description_start = self.start_of_descriptions[next_description_start_index]
            window_description = self.full_description[
                self.current_description_start:next_description_start]

        return window_description

    def is_last_window(self):
        return self.current_description_index == len(self.start_of_descriptions) - 1

    def handle_window_repetitions(self):
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

    def get_previous_window_description(self):
        prev_description_index = self.current_description_index - 1
        try:
            prev_description = self.window_descriptions[prev_description_index]
        except KeyError:
            prev_description = ""

        return prev_description

    @property
    def start_of_descriptions(self):
        description_start_indexes = self.get_description_start_indexes()
        if len(description_start_indexes) == 0:
            description_start_indexes.append(0)

        return sorted(description_start_indexes)

    def get_description_start_indexes(self):
        self.description_start_indexes = []
        window_identifiers = [
            "dos",
            "tres",
            "antepecho",
            "fija",
            "fijo",
            "corrediza",
            "abatible",
            "guillotina"
        ]
        for win_identifier in window_identifiers:
            description_starts = self.get_description_starts(win_identifier)
            self.add_description_starts(description_starts)

        return self.description_start_indexes

    def get_description_starts(self, win_identifier):
        win_type_count = self.full_description.count(win_identifier)
        self.start_of_search = 0
        self.description_starts = []
        for _ in range(win_type_count):
            description_start = self.get_description_start(win_identifier)
            self.add_description_start(description_start)

        return self.description_starts

    def add_description_starts(self, description_starts):
        for description_start in description_starts:
            self.description_start_indexes.append(description_start)

    def get_description_start(self, win_identifier):
        description_start = self.full_description.find(
            win_identifier, self.start_of_search
        )
        return description_start

    def add_description_start(self, description_start):
        if description_start != -1:
            self.description_starts.append(description_start)
            self.start_of_search = description_start + 1


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
