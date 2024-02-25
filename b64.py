import sys

import base64

if __name__ == '__main__':
    if sys.argv[1]=='-h':
        print("-e to encode")
        print("-d to decode")
    elif sys.argv[1]=='-e':
        string = sys.argv[2]
        print(base64.b64encode(string))
    elif sys.argv[1]=='-d':
        string = sys.argv[2]
        print(base64.b64decode(string))