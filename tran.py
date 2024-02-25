if __name__ == '__main__':
    import sys

    if sys.argv[1] == '-h':
        print("input your c++ array to transform it into python list format")
        sys.exit()
    while (s := input()):
        s = s.replace("]", "}")
        s = s.replace("[", "{")
        s = s.replace("\"", '\'')
        print(s)
        s = s.replace("\'", '\"')
        print(s)
