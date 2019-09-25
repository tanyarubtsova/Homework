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
	while(a != 0):
		l.add_node(a % 10)
		a = a // 10
	return l
	
def sum(a1, b1):
	c = MyList()
	a = a1.first
	b = b1.first
	inmind = 0;
	while a != None and b != None:
		s = a.key + b.key + inmind
		inmind = s // 10
		s = s % 10
		c.add_node(s)
		a = a.next
		b = b.next
	while a != None:
		s = a.key + inmind
		inmind = s // 10
		s = s % 10
		c.add_node(s)
		a = a.next
	while b != None:
		s = b.key + inmind
		inmind = s // 10
		s = s % 10
		c.add_node(s)
		b = b.next
	if inmind != 0:
		c.add_node(inmind)
	return c
	
a = int(input())
b = int(input())
al = func(a)
bl = func(b)
c = sum(al, bl)
c.print_list()
