BLOCK_LENGTH = 256
MOCK_CHAR = '~'
KEY_TRIES = 2 ** 15
FILENAME = 'encrypted.txt'


def main():
    with open(FILENAME, 'rb') as f:
        text = f.read()

    for key in range(KEY_TRIES):
        print('Trying key ' + str(key))
        decoded = decode(text, key)
        print(decoded)
        if isValid(decoded):
            return


def decode(text, key):
    plain = list(MOCK_CHAR * BLOCK_LENGTH)
    for i in range(len(text)):
        plainIndex = findIndex(key, i)
        if plainIndex is None:
            return
        plain[plainIndex] = chr(text[i] ^ i ^ plainIndex)
    for c in plain:
        if c == MOCK_CHAR:
            return
    return ''.join(plain)


def isValid(decoded):
    return decoded is not None and '{FLG:' in decoded


def findIndex(key, index):
    for i in range(BLOCK_LENGTH):
        if 3 ** (key + i) % 257 - 1 == index:
            return i


if __name__ == '__main__':
    main()
