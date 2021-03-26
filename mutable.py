import ctypes
class dy_array:
    def __init__(self, list=[]):
        self.capacity = 100
        self.num = 0
        self.a = self.new_array(self.capacity)
        if len(list) >= self.capacity:
            self._resize(len(list) * 2)
        for i in range(len(list)):
            self.a[i] = list[i]
            self.num = len(list)

    def size(self) -> int:
        return self.num

    def to_list(self) -> list:
        l = []
        for i in range(self.num):
            l.append(self.a[i])
        return l

    def from_list(self, l: list):
        if len(l) >= self.capacity:
            self._resize(len(l))
        if len(l) > 0:
            for i in range(len(l)):
                self.a[i] = l[i]
        self.num = len(l)
        return self

    def append_to_tail(self, obj):
        if self.num == self.capacity:
            self._resize(self.capacity * 2)
        self.a[self.num] = obj
        self.num += 1

    def append_to_head(self, value):
        if self.num == self.capacity:
            self._resize(self.capacity * 2)
        for i in range(self.num, 0, -1):
            self.a[i] = self.a[i - 1]
        self.a[0] = value
        self.num += 1

    def map(self, f):
        for i in range(self.num):
            self.a[i] = f(self.a[i])

    def reduce(self, f, initial_state):
        element = 0
        state = initial_state
        for i in range(self.num):
            state = f(state, self.a[element])
            element += 1
        return state

    def find(self, value):
        for i in self.to_list():
            if i is value:
                return True
        return False

    def filter(self, value):
        lst_filter = []
        for i in self.a[:self.num]:
            if i is not value:
                lst_filter.append(i)
        return lst_filter

    def empty(self):
        return None

    def remove(self, value):
        for i in range(self.num):
            if self.a[i] == value:
                for j in range(i, self.num - 1):
                    self.a[j] = self.a[j + 1]
                self.a[self.num - 1] = None
                self.num -= 1
                return
        raise ValueError('not found')

    def combine(self, dy1, dy2):
        if dy1 is None:
            if dy2.num >= self.capacity:
                self._resize(dy2.num * 2)
            for i in range(dy2.num):
                self.a[i] = dy2.a[i]
                self.num += 1
        elif dy2 is None:
            if dy1.num >= self.capacity:
                self._resize(dy1.num * 2)
            for i in range(dy1.num):
                self.a[i] = dy1.a[i]
                self.num += 1
        else:
            if (dy1.num + dy2.num) >= self.capacity:
                self._resize((dy1.num + dy2.num) * 2)
            for i in range(dy1.num):
                self.a[i] = dy1.a[i]
                self.num += 1
            for j in range(dy1.num, dy1.num + dy2.num):
                self.a[j] = dy2.a[j - dy1.num]
                self.num += 1

    def new_array(self, n):
        return (n * ctypes.py_object)()

    def _resize(self, n: int):
        N = self.new_array(n)
        for k in range(self.num):
            N[k] = self.a[k]
        self.a = N
        self.capacity = n

    def is_empty(self):
        return self.num == 0

    def __iter__(self):
        self.k = 0
        return self

    def __next__(self):
        if self.k < self.num:
            m = self.a[self.k]
            self.k += 1
            return m
        else:
            raise StopIteration