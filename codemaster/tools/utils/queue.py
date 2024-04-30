from collections import deque


class Queue:
    def __init__(self, iterable=(), maxlen=None, name='', num=0):
        self._container = deque(iterable=iterable, maxlen=maxlen)
        self.name = name
        self.num = num

    @property
    def is_empty(self):
        return not self._container

    def push(self, item):
        self._container.append(item)

    def pop(self):
        return self._container.popleft()

    def peek(self):
        return self._container[0] if not self.is_empty else None

    def __iter__(self):
        return iter(self._container)

    def __len__(self):
        return len(self._container)

    def __str__(self):
        return f"Queue({repr(list(self._container))})"

    def __repr__(self):
        return f"Queue({repr(list(self._container))})"
