class Node:
    def __init__(self, key = None, next = None):
        self.key = key
        self.next = next

class MyList:
    def __init__(self):
        self.first = None
        self.last = None

    def add_node(self, a):
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
            return
        while curr != None:
            if count == i:
                if curr.next == None:
                    self.last = curr
                prev.next = curr.next
                break
            prev = curr
            curr = curr.next
            count += 1

    def print_list(self):
        curr = self.first
        while curr != None:
            print(str(curr.key) + ' ', end=' ')
            curr = curr.next

def func(a):
	l = MyList()
	for i in a.rsplit():
		l.add_node(i)
	return l
	
a = input()   
l = func(a)
l.print_list()
#print()
#l = MyList()
#for i in range(3):
    #l.add_node(int(input()))
#l.del_node(2)
#l.del_node(0)
#l.print_list()
