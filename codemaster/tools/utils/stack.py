from collections import deque


class Stack:
    def __init__(self, iterable=(), maxlen=None, name='', num=0):
        self._container = deque(iterable=iterable, maxlen=maxlen)
        self.name = name
        self.num = num

    def __iter__(self):
        return iter(self._container)

    @property
    def is_empty(self):
        return not self._container

    def push(self, item):
        self._container.append(item)

    def pop(self):
        return self._container.pop()

    def peek(self):
        return self._container[-1] if not self.is_empty else None

    def __len__(self):
        return len(self._container)

    def __str__(self):
        return f"stack({repr(list(self._container))})"

    def __repr__(self):
        return f"stack({repr(list(self._container))})"
