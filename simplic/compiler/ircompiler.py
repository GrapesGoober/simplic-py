IR = {
    "myfunc" : {
        "return" : "r",
        "args": [
            "a", "b", "c", "d" 
        ],
        "body": {
            "start" : [
                # IR should seemlessly handle 
                # - immediate operands
                # - single assignment with multiple operations
                # - recognizing variable lifetimes
                # - variables that are used consecutively are checked

                "y = 0",            # direct assignment (using set instruction)
                "y = mul a b",      # ALU opcodes add sub lsl lsr mul div and or not
                "y = add y 3",      #   handle immediate values as well

                # memory operations
                "y = mem c",        # memory load
                "y = mem 0x20",     # arbitrary load
                "mem c = b",        # memory store
                "mem 0x20 = d",     # arbitrary store

                # function calls
                "y = call funcname y b d"
            ]
        }
    }
}