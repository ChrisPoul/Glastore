

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
        self.description_start_indexes = []
        for win_identifier in window_identifiers:
            self.get_start_of_description(win_identifier)
        if self.is_first_description_start_index():
            self.description_start_indexes.append(0)

        return sorted(self.description_start_indexes)

    def is_first_description_start_index(self):
        return len(self.description_start_indexes) == 0

    def get_start_of_description(self, win_identifier):
        win_type_count = self.full_description.count(win_identifier)
        start = 0
        for _ in range(win_type_count):
            description_start = self.full_description.find(
                win_identifier, start)
            start = self.add_description_start(description_start)

    def add_description_start(self, description_start):
        start = 0
        if description_start != -1:
            self.description_start_indexes.append(description_start)
            start = description_start + 1

        return start


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