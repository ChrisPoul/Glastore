

class WindowDescriptionExtractor:

    def __init__(self, description):
        self.full_description = description

    def get_window_descriptions(self):
        self.window_descriptions = {}
        for description_start in self.start_of_descriptions:
            self.current_description_start = description_start
            self.save_description()
        window_descriptions = self.get_window_descriptions_list()

        return window_descriptions

    def get_window_descriptions_list(self):
        return [self.window_descriptions[i] for i in self.window_descriptions]

    def save_description(self):
        self.current_description_index = self.start_of_descriptions.index(
            self.current_description_start)
        window_description = self.get_window_description()
        prev_description = self.get_previous_window_description()
        if not self.is_relative_window(prev_description):
            self.window_descriptions[self.current_description_index] = window_description

    def get_window_description(self):
        self.make_basic_window_description()
        self.handle_window_repetitions()

        return self.window_description

    def make_basic_window_description(self):
        if self.is_last_window():
            self.window_description = self.full_description[self.current_description_start:]
        else:
            next_description_start_index = self.current_description_index + 1
            next_description_start = self.start_of_descriptions[next_description_start_index]
            self.window_description = self.full_description[
                self.current_description_start:next_description_start]

    def is_last_window(self):
        return self.current_description_index == len(self.start_of_descriptions) - 1

    def handle_window_repetitions(self):
        if self.is_relative_window(self.window_description):
            self.extend_window_description()

    def extend_window_description(self):
        try:
            extended_window_index = self.current_description_index + 2
            next_description_start = self.start_of_descriptions[extended_window_index]
            self.window_description = self.full_description[
                self.current_description_start:next_description_start]
        except IndexError:
            self.window_description = self.full_description[self.current_description_start:]

    def is_relative_window(self, description):
        relative_descriptors = [
            "dos",
            "antepecho",
            "tres"
        ]
        for descriptor in relative_descriptors:
            if descriptor in description:
                return True
        return False

    def get_previous_window_description(self):
        try:
            prev_description_index = self.current_description_index - 1
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
            description_start_index = self.full_description.find(
                win_identifier, start)
            start = self.add_description_start(description_start_index)

    def add_description_start(self, description_start_index):
        start = 0
        if description_start_index != -1:
            self.description_start_indexes.append(description_start_index)
            start = description_start_index + 1

        return start
