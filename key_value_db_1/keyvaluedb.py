#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

from exception import InvalidKeyType, KeyValueStoreDumpException


class KeyValueStore(object):

    def __init__(self, file_path=None):
        self.__store = {}
        if file_path:  # load initial db from file
            self.load(file_path)

    def __getitem__(self, item):
        """Syntax sugar for get()"""
        return self.get(item)

    def __setitem__(self, key, value):
        """Syntax sugar for set()"""
        return self.set(key, value)

    def __delitem__(self, key):
        """Syntax sugar for rem()"""
        return self.rem(key)

    def rem(self, key):
        """Delete a key"""
        if key not in self.__store:  # return False instead of an exception
            return False
        del self.__store[key]
        return True

    def set(self, key, value):
        """Set the str value of a key"""
        if isinstance(key, str):
            self.__store[key] = value
            return True
        else:
            raise InvalidKeyType("Only string key type supported.")

    def get(self, key):
        """Get the value of a key"""
        try:
            return self.__store[key]
        except KeyError:
            return False

    def get_all_keys(self):
        """Return a list of all keys in db"""
        return self.__store.keys()

    def get_all_values(self):
        """Return a list of all values in db"""
        return self.__store.values()

    def load(self, file_path):
        """Load key value from the given file path"""
        location = os.path.expanduser(file_path)
        if os.path.exists(location):
            try:
                self.__store = json.load(open(file_path, 'r'))
            except ValueError:
                if os.stat(file_path).st_size == 0:  # file is empty
                    self.__store = {}
                else:
                    raise  # File is not empty, avoid overwriting it
        else:
            self.__store = {}
        return True

    def dump(self, file_path):
        """dump the current in-memory key-value store to file"""
        try:
            json.dump(self.__store, open(file_path, 'wt'))
            return True
        except KeyValueStoreDumpException:
            return False
