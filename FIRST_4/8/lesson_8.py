# python 3.7+
from __future__ import annotations  # для того, чтобы работала аннотация класса в самом себе (либо питон 3.10+)

from hashlib import sha3_256
from collections import Counter, deque
from typing import Optional, Union, Sequence, Tuple


class Node:
    left_value: Union[Node, str] = None
    left_weight: int = None
    left_str: str = None  # для отображения сокращенного названия (если включить принты), когда у нас появляется нода, а не буква, а то с учетом __repr__ выходит больно жирная строка
    main_value: Optional[str] = ''
    main_weight: int = None
    right_value: Union[Node, str] = None
    right_weight: int = None
    right_str: str = None
    lvl: str = ''

    def __init__(self, left_part: Optional[Union[Node, Tuple[str, int]]] = None, right_part: Optional[Union[Node, Tuple[str, int]]] = None,
                 main_part: Optional[Tuple[str, int]] = None) -> None:
        left_part_is_node = isinstance(left_part, Node)
        right_part_is_node = isinstance(right_part, Node)

        if main_part:  # если есть значение - значит у нас конечный пункт графа, он же - буква.
            self.main_value = main_part[0]
            self.main_weight = main_part[1]
        else:  # иначе у нас нода
            self.left_value = left_part if left_part_is_node else Node(main_part=left_part)
            self.left_weight = left_part.main_weight if left_part_is_node else left_part[1]
            self.left_str = f'_N:{left_part.main_weight}' if left_part_is_node else self.left_value
            self.right_value = right_part if right_part_is_node else Node(main_part=right_part)
            self.right_weight = right_part.main_weight if right_part_is_node else right_part[1]
            self.right_str = f'_N:{right_part.main_weight}' if right_part_is_node else self.right_value
            self.main_weight = self.left_weight + self.right_weight

    def make_lvls(self, s='') -> None:
        """
        проходимся по всему дереву и получаем коды для каждого символа
        """
        self.lvl = s
        if self.left_value:
            self.left_value.make_lvls(f'{self.lvl}0')
        if self.right_value:
            self.right_value.make_lvls(f'{self.lvl}1')

    def __repr__(self) -> str:
        if self.main_value:
            return f"'{self.main_value}':{self.main_weight}[{self.lvl}]"
        return f'({self.left_str})(_N:{self.main_weight})({self.right_str})'

    def __str__(self) -> str:
        return self.__repr__()

    def print_node_and_lvl(self):
        # только для примера из методы
        spaces = ' ' * 10
        print(f'{" " * 10}{" " * 20}{str(self)}')
        l = self.left_value
        r = self.right_value
        print(f'{" " * 10}{str(l)}{" " * 10} --- {" " * 10}{str(r)}')
        ll = l.left_value
        lr = l.right_value
        rl = r.left_value
        rr = r.right_value
        print(f'{str(ll)} --- {str(lr)}{spaces}{rl} --- {rr}')
        lrl = lr.left_value
        lrr = lr.right_value
        rll = rl.left_value
        rlr = rl.right_value
        print(f'{" " * 10}{str(lrl)} --- {str(lrr)}{" " * 5}{rll} --- {rlr}')
        rlll = rll.left_value
        rllr = rll.right_value
        print(f'{" " * 50}{str(rlll)} --- {str(rllr)}')


class Tree:
    _root: Node
    encode_dct: dict
    decode_dct: dict

    def __init__(self, dct):
        self.encode_dct = dict(dct)
        self.decode_dct = dict()
        self._make_tree_structure()

    @staticmethod
    def get_idx_for_insert(l: Sequence[Union[Node, Tuple[str, int]]], n: int) -> int:
        def get_weight(v: Union[Node, Tuple[str, int]]):
            return v.main_weight if isinstance(v, Node) else v[1]

        for i, v in enumerate(l):
            if n <= get_weight(v):
                return i
        return len(l)

    def _make_tree_structure(self) -> None:
        # сортировка в таком порядке тут не обязательна, просто для удобства
        # можно было бы отсортировать по убыванию только по значению словаря и работать с конца через простой list и pop()
        q = deque(sorted(self.encode_dct.items(), key=lambda x: x[::-1]))

        # как оказалось в методе сортировка идет по возрастанию индексов, но убыванию самих значений =(
        # получилось повторить через groupby, переносить сюда такую сортировку не стал.
        # в моем варианте сортировки немного поменяются местами значения.
        # q = deque([('r', 1), ('!', 1), ('p', 2), ('o', 2), (' ', 2), ('b', 3), ('e', 4)])

        # print(q)  # принты оставил специально, если вдруг появится желание посмотреть на преобразования
        while len(q) > 1:
            x, y = q.popleft(), q.popleft()
            n = Node(x, y)
            q.insert(Tree.get_idx_for_insert(q, n.main_weight), n)
            # print(q)
        self._root = q[0]
        self._root.make_lvls()
        self._make_decode_dict()
        # self._root.print_node_and_lvl()  # только для примера из методы

    def _make_decode_dict(self, node: Node = None) -> None:
        n = node if node else self._root
        if n.main_value:
            self.decode_dct[n.main_value] = n.lvl
        else:
            self._make_decode_dict(n.left_value)
            self._make_decode_dict(n.right_value)

    def encode(self, string: str) -> str:
        return ''.join([self.decode_dct[c] for c in string])


def part_1():
    print('# 1. Определение количества различных подстрок с использованием хэш-функции.')
    # Пусть дана строка S длиной N, состоящая только из маленьких латинских букв.
    # Требуется найти количество различных подстрок в этой строке.

    s = 'position'  # в данном примере уникальных будет на 2 меньше, т.к. дублируются буквы O, I
    substrs = [s[i:i + n] for n in range(1, len(s)) for i in range(len(s)) if len(s[i:i + n]) == n]  # формируем подстроки
    substrs_hash = [sha3_256(v.encode('utf8')).hexdigest() for v in substrs]  # получаем хэши
    print(f'Для строки "{s}":\n'
          f' - подстроки: {substrs}\n'
          f' - их кол-во: {len(substrs)}\n'
          f' - среди них уникальных: {len(set(substrs_hash))}\n')


def part_2():
    print('# 2. Закодируйте любую строку из трех слов по алгоритму Хаффмана.')

    def format_byte_print(lst):
        """
        группирует по 4 символа
        '0110001001100101' -> '0110 0010 0110 0101'
        """
        return ''.join([f'{lst[i:i + 4]} ' for i in range(0, len(lst), 4)])

    s = 'hello beautiful world'
    # s = 'beep boop beer!'  # пример из методы
    print(s, '\n')
    tree = Tree(Counter(s))
    print(tree.encode_dct, '\n')
    print(tree.decode_dct, '\n')
    s_bytes = ''.join([f'{(ord(c)):08b}' for c in s])  # прверащаем все в одну строку
    s_bytes = format_byte_print(s_bytes)  # группируем по 4
    print(s_bytes, '\n')
    # print('0110 0010 0110 0101 0110 0101 0111 0000 0010 0000 0110 0010 0110 1111 0110 1111 0111 0000 0010 0000 0110 0010 0110 0101 0110 0101 0111 0010 0010 000')  # для проверки примера из методы
    s_encode_bytes = tree.encode(s)
    s_encode_bytes = format_byte_print(s_encode_bytes)
    print(s_encode_bytes, '\n')
    # print('0011 1110 1011 0001 0010 1010 1100 1111 1000 1001')


def main():
    part_1()
    part_2()


if __name__ == '__main__':
    main()
