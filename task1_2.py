'''
task 1, program 2
'''
'''
Example:
Input: 1->2->3 + 1->1->1
Output: 2 -> 3 -> 4
'''
from task1_1 import *
	
def sum(a1, b1):
	c = MyList()
	a = a1.first
	b = b1.first
	inmind = 0;
	while a != None and b != None:
		s = int(a.key) + int(b.key) + inmind
		inmind = s // 10
		s = s % 10
		c.add_node(s)
		a = a.next
		b = b.next
	while a != None:
		s = int(a.key) + inmind
		inmind = s // 10
		s = s % 10
		c.add_node(s)
		a = a.next
	while b != None:
		s = int(b.key) + inmind
		inmind = s // 10
		s = s % 10
		c.add_node(s)
		b = b.next
	if inmind != 0:
		c.add_node(inmind)
	return c
	

a, b = input().split('+')
al = func1(a)
bl = func1(b)
c = sum(al, bl)
c.print_list()
