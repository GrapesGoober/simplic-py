import json

class Memory:
    BIT_SIZE = 16
    _words: dict = {}

    def __init__(self, filename: str):
        with open(filename, 'r') as f:
            self._words = json.load(f)

        self._words = {int(key): int(value) for key, value in self._words.items()}

        for i, v in self._words.items():
            if i > (2 ** self.BIT_SIZE):
                raise Exception(f'Address {i} too large for {self.BIT_SIZE} bits')
            if v > (2 ** self.BIT_SIZE):
                raise Exception(f'Value {v} too large for {self.BIT_SIZE} bits')

    def read(self, address: int) -> int:
        return self._words[address] if address in self._words else 0
    
    def write(self, address: int, value: int) -> None:
        self._words[address] = value & (2 ** self.BIT_SIZE)

