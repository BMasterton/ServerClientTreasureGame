# #!/usr/bin/python3
#
# # Question 1
# # print('''
# #         Create a command-line python program which takes a single utf-8 character as an
# #         argument:
#
# #         ./q_1.py A
# #         # OR
# #         python q_1.py A
#
# #         ... will pass the string "A" as its only argument. Reminder: command-line arguments
# #         in python can be accessed via sys.argv (an array), and so:
#
# #         import sys
# #         print(sys.argv[1])
#
# #         ... will print "B" if invoked with "B" as the argument. (argv[0] is the name of the
# #         python script, eg "q_1.py" in this case.)
#
#
#
# #         Your program should take the character (string) argument and:
#
# #         1) Convert it to a single byte (instead of a string) corresponding to the utf-8
# #            code for the character (eg "A" should result in the value being decimal 65, "B"
# #            would be decimal 66, etc.
#
# #         2) Swap the bits of the value as follows:
# #             - the seventh and eighth bits (counting from the left) should be swapped.
# #             - the fifth and sixth bits should be swapped.
#
# #         3) Convert the result back into a single-character string, and print it.
#
#
# #         As test cases:
# #             - Running "./q_1.py A" at the command line should print out "B".
# #             - Running "./q_1.py B" at the command line should print out "A".
# #             - Running "./q_1.py D" at the command line should print out "H".
# #             - Running "./q_1.py H" at the command line should print out "D".
# #             - Running "./q_1.py J" at the command line should print out "E".
# #             - Running "./q_1.py E" at the command line should print out "J".
# #     ''')
#
#
#
#
# # REMEMBER: a byte is the same thing as an integer between 0 and 255
#
# # Solution 1
# import sys
#
#
# the_arg = sys.argv[1].encode('utf-8')   # Encoding as utf-8 to convert ASCII string to bytes
#
# the_byte = the_arg[0]   # First (should be the only) byte
#
#
# original_first_four = (the_byte & 240)   # 240 == 0b11110000
#
# bit_5 = (the_byte & 8) >> 1   # mask out the value of bit 5, and shift it to position 6
# bit_6 = (the_byte & 4) << 1   # mask out the value of bit 6, and shift it to position 5
#
# bit_7 = (the_byte & 2) >> 1   # same for bits 7 and 8
# bit_8 = (the_byte & 1) << 1
#
#
# # bitwise OR will merge all non-zero bits into one byte...
#
# final_int = original_first_four | bit_5 | bit_6 | bit_7 | bit_8
#
# # can also use the |= operator to combine the OR and the assignment (=)...
#
# #final_int = original_first_four | bit_5
# #final_int |= bit_6
# #final_int |= bit_7
# #final_int |= bit_8
#
# # can also construct the final byte and do the bit masking and shifting together...
#
# #final_int = (the_byte & 240)   # Mask out first four
# #final_int |= (the_byte & 8) >> 1
# #final_int |= (the_byte & 4) << 1
# #final_int |= (the_byte & 2) >> 1
# #final_int |= (the_byte & 1) << 1
#
#
# # Easy way of creating a bstring of length 1 from an integer...
#
# output_bstring = int.to_bytes(final_int, 1, 'big')   # byte order doesn't matter, because only 1 byte
#
#
# # Can also do this to convert one (or more) integers into the corresponding byte string...
#
# #output_bstring = bytes( [ final_int ] )
#
#
# # Finally, convert to a normal string and then print!
#
# string_output = output_bstring.decode('utf-8')
# print(string_output)
#
# # Can also just print byte strings ("bytes") directly:
#
# # print(output_bstring)
#


## Question 2

#!/usr/bin/python3

# Erase the intructions (this print statement) after beginning/when you're done :)
# print('''
#         Create a command-line python program which takes a single utf-8 character as an
#         argument:
#
#         ./q_2.py A
#         # OR
#         python q_2.py A
#
#         ... will pass the string "A" as its only argument. Reminder: command-line arguments
#         in python can be accessed via sys.argv (an array), and so:
#
#         import sys
#         print(sys.argv[1])
#
#         ... will print "B" if invoked with "B" as the argument. (argv[0] is the name of the
#         python script, eg "q_2.py" in this case.)
#
#
#
#         Your program should take the character (string) argument and:
#
#         1) Convert it to a single byte (instead of a string) corresponding to the utf-8
#            code for the character (eg "A" should result in the value being decimal 65, "B"
#            would be decimal 66, etc.
#
#         2) Take that byte, and treat the first four and last four bits as two separate
#            binary values. Eg. 'A' as a byte, which is decimal 65, and 0b01000001 in binary
#            would produce the decimal numbers 4 (0b0100) and 1 (0b0001).
#
#         3) Multiply the two numbers together, and print the result.
#
#
#         As test cases:
#             - Running "./q_2.py A" at the command line should print out "4".
#             - Running "./q_2.py B" at the command line should print out "8".
#             - Running "./q_2.py D" at the command line should print out "16".
#             - Running "./q_2.py H" at the command line should print out "32".
#             - Running "./q_2.py E" at the command line should print out "20".
#             - Running "./q_2.py J" at the command line should print out "40".
#     ''')

# # Solution 2
# import sys
#
# inputVal = sys.argv[1]
## string to byte value you encode it and then you grab the first substring at position 0 which is byte one
# val1 = inputVal.encode('utf-8')
# val2 = val1[0]
#
# firstFour = (val2 & 240) >> 4 # we mask by 240 as we want 0b11110000 then we shift to the right 4 to get 00001111
#
# lastFour = (val2 & 15) # we mask by 00001111 and dont need to shift as were already at the position we want 00001111
#
# print(firstFour * lastFour)
#


##Question 3

#!/usr/bin/python3

# Erase the intructions (this print statement) after beginning/when you're done :)
# print('''
#         Create a command-line python program which takes a string as an argument:
#
#         ./q_3.py ABCDEFG
#         # OR
#         python q_3.py ABCDEFG
#
#         ... will pass the string "ABCDEFG" as its only argument. Reminder: command-line
#         arguments in python can be accessed via sys.argv (an array), and so:
#
#         import sys
#         print(sys.argv[1])
#
#         ... will print "ABCDEFG" if invoked with "ABCDEFG" as the argument. (argv[0] is
#         the name of the python script, eg "q_3.py" in this case.)
#
#
#
#         Your program should take the string argument and:
#
#         1) Convert it to a byte string (bytes), so that we can work with each individual
#            byte (integer).
#
#         2) Build a new bytes value from the original with all bytes that have bit 6 set
#            to 1 removed, and then convert the result back to a string and print.
#
#
#         As test cases:
#             - Running "./q_3.py ABCDEFGHIJKLMNOPQRSTUVWXYZ" at the command line should
#               print out "ABCHIJKPQRSXYZ"
#             - Running "./q_3.py WELCOMETOTHEMACHINE" at the command line should print out
#               "CHACHI"
#     ''')
#


##Solution 4
# #!/usr/bin/python3
#
# import sys
#
#
# the_arg = sys.argv[1].encode('utf-8')   # Encoding as utf-8 to convert ASCII string to bytes
#
# new_bytes = []
#
# for b in the_arg:
#     if b & 0b00000100: # mask it and if its 0 keep going
#         continue
#
#     new_bytes.append(b)
#
# print(bytes(new_bytes).decode('utf-8'))
#


## Question 4
#!/usr/bin/python3

# Erase the intructions (this print statement) after beginning/when you're done :)
# print('''
#         Create a command-line python program which takes a string as an argument:
#
#         ./q_4.py ABCDEFG
#         # OR
#         python q_4.py ABCDEFG
#
#         ... will pass the string "ABCDEFG" as its only argument. Reminder: command-line
#         arguments in python can be accessed via sys.argv (an array), and so:
#
#         import sys
#         print(sys.argv[1])
#
#         ... will print "ABCDEFG" if invoked with "ABCDEFG" as the argument. (argv[0] is
#         the name of the python script, eg "q_4.py" in this case.)
#
#
#
#         Your program should take the string argument and:
#
#         1) Convert it to a byte string (bytes), so that we can work with each individual
#            byte (integer).
#
#         2) Build a new bytes value from the original where the last 4 bits of each byte
#            are flipped, eg: 0b01010101
#                     becomes 0b01011010
#
#
#         As test cases:
#             - Running "./q_4.py ABCDEFG" at the command line should
#               print out "NMLKJIH"
#             - Running "./q_4.py GIBSON" at the command line should print out
#               "HFM\@A"
#     ''')
#

## Solution 4
#
# import sys
#
# the_bytes = sys.argv[1].encode('utf-8')
#
# new_ints = [] # will become an array of ints that we need to decode
#
# for tb in the_bytes:
#     new_byte = tb ^ 0b00001111 # remember: '^' is the bitwise 'XOR' operator
#     new_ints.append(new_byte)

# print(bytes(new_ints).decode('utf-8')) # easier version of grabbing the correct values from teh int ones in the array to be made back into strings
# for value in new_ints:
#     print((int.to_bytes(value, 1, 'big')).decode('utf-8'))

# # Question 5
# !/usr/bin/python3

# Erase the intructions (this print statement) after beginning/when you're done :)
# print('''
#         Create a command-line python program which takes a string as an argument:
#
#         ./q_5.py ABCDEFG
#         # OR
#         python q_5.py ABCDEFG
#
#         ... will pass the string "ABCDEFG" as its only argument. Reminder: command-line
#         arguments in python can be accessed via sys.argv (an array), and so:
#
#         import sys
#         print(sys.argv[1])
#
#         ... will print "ABCDEFG" if invoked with "ABCDEFG" as the argument. (argv[0] is
#         the name of the python script, eg "q_4.py" in this case.)
#
#
#
#         Your program should take the string argument and:
#
#         1) Convert it to a byte string (bytes), so that we can work with each individual
#            byte (integer).
#
#         2) For each byte in the input:
#             - Flip all odd bits, eg: 0b11111111
#                              becomes 0b01010101
#
#             - Read each pair of two bits as a separate binary number, and multiply them all
#               together. Eg. if the byte after flipping even bits is 10110110, then we
#               end up with 10 11 01 10 as our pairs of bits, which is 2 3 1 2 in decimal,
#               and 2 x 3 x 1 x 2 = 12
#
#             - Convert the multiplication result (12 in our example) back to a byte, and use
#               that as the replacement value for each byte in the string.
#
#         3) Print out the final new string.
#
#
#         A full example: the input string is "ATTT", then:
#
#             - A = integer 65 = 0b01000001
#
#                after flipping: 0b11101011 => 11 10 10 11
#                                           => 3 x 2 x 2 x 3
#                                           => 36
#
#             - T = integer 84 = 0b01010100
#                after flipping: 0b11111110 => 11 11 11 10
#                                           => 3 x 3 x 3 x 2
#                                           => 54
#
#             - ASCII / utf-8 value decimal 36 is a '$'
#             - ASCII / utf-8 value decimal 54 is a '6'
#
#         So, this example will print "$666".
#
#
#     ''')
#

## Solution 5
# #!/usr/bin/python3
#
# import sys
#
# the_bytes = sys.argv[1].encode('utf-8')
#
# new_ints = []
#
# for tb in the_bytes:
#     small_ints = []
#
#     for shift_val in (6, 4, 2, 0):
#         small = (tb >> shift_val) & 3
#
#         if small & 2:   # first bit is set
#             small = small & 1   # Just take the second bit, first flips to zero
#         else:   # first bit NOT set
#             small = (small & 1) + 2   # take the second bit, and add 2 to set the first bit
#
#         small_ints.append(small)
#
#     product = 1
#     for si in small_ints:
#         product = product * si
#
#     new_ints.append(product)
#
# print(bytes(new_ints).decode('utf-8'))

