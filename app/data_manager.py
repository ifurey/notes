import csv

from .models import Note


class NoteDataManager(object):
    def __new__(cls):
        # Singleton pattern
        if not hasattr(cls, 'instance'):
            cls.instance = super(NoteDataManager, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        self._notes = []


    def _response_template(self, index: int, note) -> dict:
        return {'index': index} | note


    def get_notes_by_user(self, user_name):
        response = []
        for index, item in enumerate(self._notes):
            if item['owner'] == user_name:
                response.append(self._response_template(index, item))
        return response
    

    def get_note(self, index):
        try:
            return self._response_template(index, self._notes[index])
        except IndexError:
            return None


    def add_note(self, note):
        self._notes.append(note)
        return self._response_template(len(self._notes) - 1, note)


    def update_note(self, index, new_note):
        try:
            self._notes[index] = new_note
            return self._response_template(index, self._notes[index])
        except IndexError:
            return False


    def delete_note(self, index):
        try:
            self._notes.pop(index)
            return True
        except IndexError:
            return False


class ListDataManager(object):
    def __new__(cls):
        # Singleton pattern
        if not hasattr(cls, 'instance'):
            cls.instance = super(ListDataManager, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        self._notes = []
        self._users = []


    def _read_entry_by_key(self, list, key, value):
        for item in list:
            if item.get(key) == value:
                return item
        return None


    def _read_entry_by_index(self, list, index):
        try:
            return list[index]
        except IndexError:
            return None


    def _write_entry(self, list: list, entry_value):
        entry_value.id = len(list)
        list.append(entry_value)
        return entry_value.id


    def _update_entry_by_index(self, list, entry_value):
        try:
            list[entry_value.id] = entry_value
            return True
        except IndexError:
            return False


    def _delete_entry(self, list, index):
        try:
            # Entries are replaced with None to keep the list-index/entry-id relation
            list[index] = None
            return True
        except IndexError:
            return False


    def add_note(self, note: Note) -> id:
        return self._write_entry(self._notes, note)
    

    def get_note(self, id: int) -> Note:
        return self._read_entry_by_index(self._notes, id)


class DataManager(object):
    NOTES_FILE_NAME = "notes.csv"
    USERS_FILE_NAME = "users.csv"


    def __new__(cls):
        # Singleton pattern
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataManager, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        try:
            with open(self.NOTES_FILE_NAME, 'r') as file:
                reader = csv.DictReader(file)
                *_, last_entry = reader
                self.next_note_id = last_entry.id + 1
        except FileNotFoundError:
            self.next_note_id = 1

    def _read_entry(self, filename, key, value):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for item in reader:
                if item.get(key) == value:
                    return item
            return None


    def _write_entry(self, filename):
        pass


    def _update_entry(self, filename, key, value):
        pass


    def delete_entry(self, filename, key, value):
        pass


    def get_note(self, note_id: int) -> dict:
        return self._read_entry(self.NOTES_FILE_NAME, 'id', note_id)


    