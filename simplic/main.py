from microcontroller import SimplicMicrocontroller

filename = "simplic\\test_codes\\fib.hex"

if __name__ == '__main__':

    mc = SimplicMicrocontroller()
    mc.load_program(filename)
    mc.run()
