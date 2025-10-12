string = "Hi 🙂"
print_bytes = lambda s: print(' '.join(f'{b:02x}' for b in s))

print_bytes(string.encode('utf-8'))
# 48 69 20 f0 9f 99 82
# print_bytes(string.encode('ascii'))
# The string can't be encoded into ascii because its not a valid encoder.
print_bytes(string.encode('utf-16'))
# ff fe 48 00 69 00 20 00 3d d8 42 de - The byte string is longer and has different bytes.

byte16 = string.encode('utf-16')
#print(byte16.decode('utf-8'))
#The utf-16 encoded byte can't be decoded by utf-8, only decoded back into a string by utf-16.
print(byte16.decode('utf-16'))
