

class DoubleLinkedList:
    def __init__(self, _list: list):
        self.nCount = 0     # 节点个数
        self.nHead = DoubleLinkedNode(None, None, None, None)
        self.nHead.prev = self.nHead
        self.nHead.next = self.nHead
        self.node = self.nHead

    def size(self):
        return self.nCount

    def is_empty(self):
        return self.nCount == 0

    def getnode(self, index):
        if index == 0:
            return self.nHead
        if index < 0 or index > self.nCount:
            raise Exception('IndexOutOfBounds')
        if index < self.nCount / 2:
            self.node = self.nHead.next
            i = 0
            while i < index - 1:
                self.node = self.node.next
                i += 1
            return self.node
        # 反向查找剩余部分
        self.node = self.nHead.prev
        rindex = self.nCount - index
        j = 0
        while j < rindex:
            self.node = self.node.prev
            j = j + 1
        return self.node

    def insert(self, index, value):
        now_node = self.getnode(index)
        new_node = DoubleLinkedNode(None,None,now_node.id+1, value)
        new_node.prev = now_node
        new_node.next = now_node.next
        now_node.next.prev = new_node
        now_node.next = new_node
        self.nCount += 1

    def delete(self, index):
        if index == 0:
            raise Exception('0 is not allowed!')
        now_node = self.getnode(index)
        now_node.prev.next = now_node.next
        now_node.next.prev = now_node.prev
        self.nCount -= 1


class DoubleLinkedNode:
    def __init__(self, _prev, _next, _id, _value):
        self.prev = _prev
        self.next = _next
        self.id = _id
        self.value = _value
