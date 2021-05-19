

class ResponseStack:
    def __init__(self):
        self.__stack = []

    def is_empty(self):
        return self.__stack == []

    def push(self, item):
        self.__stack.append(item)

    def pop(self):
        if self.is_empty():
            return
        else:
            return self.__stack.pop()

    def top(self):
        if self.is_empty():
            return
        else:
            return self.__stack[-1]

    def calc(self):
        pass
