from typing import Tuple


class HashTable:
    #hash table with linked list
    """
    Data type of storing keys efficiently.
    """

    def __init__(self, size):
        self.__items = [[] for _ in range(size)]
        self.__size = size

    def hash(self, key) -> int:
        """
        Hash of the key to find approximate position in HashTable
        """
        key_sum = sum(ord(chr) - ord('0') for chr in key)
        return key_sum % self.__size

    def add(self, key):
        """
        Add key to HashTable
        :param key:
        :return:
        """
        if self.contains(key):
            return self.getPosition(key)
        self.__items[self.hash(key)].append(key)
        return self.getPosition(key)

    def contains(self, key):
        return self.getPosition(key) != (-1, -1)

    def remove(self, key):
        """
        Removes item for HashTable
        :param key:
        """
        pos = self.getPosition(key)
        if pos[0] == -1:
            return
        self.__items[pos[0]][pos[1]] = None

    def __str__(self) -> str:
        result = "Symbol Table (kept as a Hash Table using Lists)\n"
        for i in range(self.__size):
            result = result + str(i) + "->" + str(self.__items[i]) + "\n"
        return result

    def getPosition(self, key) -> Tuple[int, int]:
        """
        Calculates the position of the given key, if key is not found, it return (-1, -1) position
        """
        list_position = self.hash(key)
        list_index = 0
        for item in self.__items[list_position]:
            if item != key:
                list_index += 1
            else:
                break
        if list_index >= len(self.__items[list_position]):
            return -1, -1
        return list_position, list_index