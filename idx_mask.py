# code to print from 2 power 0 to 2 power 31 as hexdecimal with fixed width




for i in range(32):
    print(f"0x{2 ** i:08X}", end = " ,") # no new line  and 8 digit hexdecimal with leading zeros

