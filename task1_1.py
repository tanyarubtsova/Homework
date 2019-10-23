'''
task 1, program 1
'''
class Node:
    def __init__(self, key=None, next=None):
        self.key = key
        self.next = next


class MyList:
    def __init__(self):
        self.first = None
        self.last = None
        self.len = 0


    def add_node(self, a):
        self.len += 1
        if self.first == None:
            self.first = Node(a, None)
            self.last = self.first
        else:
            old_node = self.last
            self.last = Node(a, None)
            old_node.next = self.last


    def find_node(self, a):
        curr = self.first
        while a != curr.key:
            curr = curr.next
        return curr

    def del_node(self, i):
        if self.first == None:
            return
        curr = self.first
        count = 0
        if i == 0:
            self.first = curr.next
            self.len -= 1
            return
        while curr != None:
            if count == i:
                self.len -= 1
                if curr.next == None:
                    self.last = curr
                prev.next = curr.next
                break
            prev = curr
            curr = curr.next
            count += 1

    def print_list(self):
        curr = self.first
        i = 1
        while curr != None:
            if i == self.len:
                print(str(curr.key), end=' ')
            else:
                print(str(curr.key) + ' -> ', end='')
            curr = curr.next
            i += 1
        print()

def func1(a):
    l = MyList()
    while a != '':
        if (a[0] >= '0') and (a[0] <= '9'):
            key = a[0]
            l.add_node(key)
        a = a[1:]
    return l


def func(a):
    l = MyList()
    while a != '':
        if (a[-1] >= '0') and (a[-1] <= '9'):
            key = a[-1]
            l.add_node(key)
        a = a[0:-1]
    return l

