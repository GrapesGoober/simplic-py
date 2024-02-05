class SimplicIRParser:
    def from_file(self, filename: str) -> list[tuple]:
        with open(filename, 'r') as file:
            for linenum, line in enumerate(file):
                tokens = line.split('#')[0].split()
                if tokens == []: continue

                match tokens[0]:
                    case 'func':
                        print('\nDefining a new function')
                        print('Name:', tokens[1])
                    case 'label':
                        print('label', tokens[1])
                    case _:
                        print('\t', ' '.join(tokens))


SimplicIRParser().from_file("test_codes\\fib.ir")
                        