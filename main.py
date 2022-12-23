import sys, math



class Node:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.symbol = symbol
        self.freq = int(freq)
        self.right = right
        self.left = left

    def code(self, dict, pref):
        if self.symbol is not None:
            dict[self.symbol] = pref
        else:
            self.left.code(dict, pref + '0')
            self.right.code(dict, pref + '1')

    def height(self):
        if self.symbol is not None:
            return 1
        else:
            lheight = self.left.height()
            rheight = self.right.height()
            return max(rheight + 1, lheight + 1)


def encode(f1, f2):
    F = open(f1)
    count = [x for x in F.read()]
    F.close()

    # создание словаря: символ -> частота
    chars = dict()
    for x in count:
        if x in chars.keys():
            chars[x] += 1
        else:
            chars[x] = 1
    chars = dict(sorted(chars.items(), key=lambda item: item[1]))

    # создание списка звеньев
    nodes = []
    for i in chars.items():
        nodes.append(Node(i[1], symbol=i[0]))

    # создание дерева
    while len(nodes) > 1:
        left = nodes.pop(0)
        right = nodes.pop(0)
        nodes.append(Node(left.freq + right.freq, left=left, right=right))
        nodes = sorted(nodes, key=lambda x: x.freq)
    tree = nodes[0]

    # cоздание словарая с кодами
    code = {}
    tree.code(code, "")

    # кодирование файла
    output = ""
    for ch in count:
        output += code[ch]
    n = int('1' + output, 2)
    n = n.to_bytes((n.bit_length() + 7) // 8, 'big')

    # кодирование словаря
    len_of_dict = max(len(i) for i in code.values()) + 1
    len_of_dict = math.ceil(len_of_dict / 8)

    # запись в файл
    with open(f2, 'wb') as f:
        f.write(len(code).to_bytes(1, 'big'))
        f.write(len_of_dict.to_bytes(1, 'big'))
        for i in code:
            f.write(ord(i).to_bytes(2, 'big'))  # 2 байта на запись ключа
            symbol_code = int('1' + code[i], 2).to_bytes(len_of_dict, 'big')  # количество байтов на запись значения
            f.write(symbol_code)
        f.write(n)


def decode(f1, f2):
    with open(f1, 'rb') as f:
        data = f.read()
    numb_of_keys = int.from_bytes(data[0:1], 'big')  # количество ключей
    len_of_value = int.from_bytes(data[1:2], 'big')  # длина каждого закодированного ключа
    data = data[2:]

    new_dict = {}  # новый словарь
    for i in range(numb_of_keys):
        key = chr(int.from_bytes(data[:2], 'big'))  # ключ исходного словаря
        value = str(bin(int.from_bytes(data[2:2 + len_of_value], 'big')))[3:]  # значение исходного словаря
        data = data[2 + len_of_value:]  # обновление индексов
        new_dict[value] = key


    symbols_decode = int.from_bytes(data, 'big')
    n = str(bin(symbols_decode))[3:]
    output = ''

    i = 1
    while len(n) != 0:

        key = n[:i]
        if key in new_dict.keys():
            output += new_dict[key]
            n = n[i:]
            i = 0
        else:
            i += 1
    with open(f2, 'w') as f:
        f.write(output)


if __name__ == '__main__':
    pars = sys.argv
    try:
        if pars[1] == '--encode':
            file1 = pars[2]
            file2 = pars[3]
            encode(file1, file2)
        elif pars[1] == '--decode':
            file1 = pars[2]
            file2 = pars[3]
            decode(file1, file2)
    except Exception:
        print("Неизвестная ошибка: проверьте правильность введённых данных")

    # encode("input.txt", "output.txt")
    # decode("output.txt", "input2.txt")
