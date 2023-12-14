class Memory:
    
    def __init__(self) -> None:
        self.MASK = 0xFFFF
        self.__words = {}

    def read(self, address: int) -> int:
        return self.__words[address] if address in self._words else 0
    
    def write(self, address: int, value: int) -> None:
        self.__words[address] = value & self.MASK
        
    def load(self, filename: str) -> None:
        with open(filename, 'r') as f:
            words = f.read().split()
            self._words = {}
            for i, v in enumerate(words):
                v = int(v, 16)
                if i > self.MASK:
                    raise Exception("Can't load (file too large)")
                if v > self.MASK:
                    raise Exception("Can't load (value overflow)")
                self._words[i] = v
