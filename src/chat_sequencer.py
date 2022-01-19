#!/rhome/q1016330/dev/miniconda/bin/python
"""
Write module docstring here

"""

import csv
import datetime
import os
import argparse
import json
import sys

class ChatSequencer:
    """
    Represents all chats between a single recipient and contacts or other senders

    Parameters
    ----------
    path       : str
        The absolute path to a directory containing chat files
    config     : str
        The absolute path to a *.json config file
    """
    def __init__(self, path: str, config: str) -> None:
        self._path = path
        self._config = config
        self._contacts = []
        self._chats = []

    def get_chats(self) -> list:
        if os.path.isdir(self.path):
            chats = self.get_list_of_chats()
            for chat in chats:
                self.read_chat_file(chat)
        elif os.path.isfile(self.path):
            self.read_chat_file(self.path)

    def get_list_of_chats(self) -> tuple:
        list_of_files = []
        for (dirpath, subdirs, filenames) in os.walk(self._path):
            list_of_files += [os.path.join(dirpath, file) for file in filenames]
            dirname = dirpath.split(sep='/')[-1:]
            if dirname in self._config['dir_names']:
                self._parse_filenames(filenames, dirname)
        return list_of_files

    def _parse_filenames(self, filenames, dirname):
        for file in filenames:
            number, date = file.split(sep='-')
            contact = Contact(number=str(number), name=dirname)
            chat = Chat(
                [Contact(number='19199463554', name='am'),
                contact], datetime.datetime.strptime(date,
                '%Y/%m/%d %H:%M:%S'),
                file=file)
            chat.get_exchanges_from_file()
            self._contacts += contact
            self._chats += chat

    def get_dir_names(self):
        return self._config['dir_names']

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if not os.path.exists(path):
            raise FileExistsError('Input path does not exist')

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        if not os.path.exists(config):
            raise FileExistsError('The config file does not exist')
        with open(config) as config_in:
            self._config = json.load(config_in)


class Chat:
    """
    Represents a series of exchanges between two contacts

    Parameters
    ----------
    contacts : list
        A list containing the two contacts who are exchanging messages
    date     : datetime
        The date of the first exchange
    file     : str
        The csv file with all exchanges between the two contacts in the contacts list

    """
    def __init__(self, contacts: list, date: datetime.datetime, file: str) -> None:
        self._start = date
        self._end = None
        self._file = file
        self._exchanges = []

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file):
        if not os.path.isfile(file):
            raise FileNotFoundError('The chat input file is not found')
        self._file = file

    def get_exchanges_from_file(self):
        with open(self._file) as file_in:
            reader = csv.DictReader(file_in)
            for row in reader:
                exchange = {
                    'date': row['Date'],
                    'sender': row['Sender'],
                    'recipient': row['Recipient'],
                    'message': row['Message']}
                self._exchanges.append(exchange)


class Contact:
    def __init__(self, number: str, name: str) -> None:
        self.number = number
        self.name = name

def parse_args():
    """
    Parse the cli args for this program

    Returns
    -------
        input_path  : the filepath to json config file

    """
    parser = argparse.ArgumentParser(description="chat reader")
    parser.add_argument('-c', '--config_path', type=str, required=True, help='path to config.json')
    parser.add_argument('-i', '--input_directory', type=str, required=True, help='the absolute directory path to csv files')
    return parser.parse_args()


def main():
    """
    Enter docstring here
    """
    args = parse_args()
    config_dict = dict()

    ChatSequencer(path=args.input_directory, config=config_dict)

if __name__ == "__name__":
    main()
