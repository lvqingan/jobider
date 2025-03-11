import json

from errors.error_codes import ParserErrorCodes

class KeyNotFoundException(Exception):
    def __init__(self, target_dict, key_name, message = None):
        self.key_name = key_name
        self.target_dict = target_dict
        self.error_code = ParserErrorCodes.KEY_NOT_FOUND
        if message is None:
            self.message = f'[{key_name}] not found in {json.dump(target_dict)}'
        else:
            self.message = message
        super().__init__(self.message)