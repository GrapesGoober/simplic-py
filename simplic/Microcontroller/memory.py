import intelhex

class Memory:
    words = {}
    def read(self, address):
        return self.words[address] if address in self.words else 0
    def write(self, address, value):
        self.words[address] = value
    def load_from(self, filename):
        pass
