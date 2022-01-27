#!/usr/bin/python3

class DataError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ConfigError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class dbError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
class BackUpError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
class NotReadyError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ItemError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class FileError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
