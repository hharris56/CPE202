#Name:
#Section: 11
#Data Definition

class HuffmanNode:
	def __init__(self, char, freq):
		self.char = int(char)
		self.freq = int(freq)
		self.left = None
		self.right = None
		
	def __repr__(self):
		return "| Char: %s Freq: %s | LEFT(%s) RIGHT(%s)" % (self.char, self.freq, self.left, self.right)
#		return "| Char: %s Freq: %s Code: %s |" % (self.char, self.freq, self.code)
	
	def is_leaf(self):
		return self.right == self.left == None
		# add any necessary functions you need

class OrderedLink:
	def __init__(self, first = None, last = None, size = 0):
		self.first = first
		self.last = last
		self.size = size
		
	def __repr__(self):
		return "%s" % (self.first)
		
	# -> boolean
	# returns if the list is empty
	def is_empty(self):
		return self.first == None

	# -> val
	# returns the first value in the list
	def pop(self):
		temp = self.first.val
		if self.first == self.last:
			self.first = None
			self.last = None
		else:
			self.first = self.first.next
		self.size -= 1
		return temp
	
	# val ->
	# accepts a val, places value in list
	def insert(self, val, node = "first"):
		# emptycase
		if self.is_empty():
			newnode = OrderedNode(val)
			self.first = newnode
			self.last = newnode
		else:
			if node == "first":							# start at first node
				node = self.first
			if comes_before(val, node.val):				# node comes before
				newnode = OrderedNode(val)				# create newnode
				if node != self.first:
					# previous node updated
					node.prev.next = newnode
					newnode.prev = node.prev
					# current node updated
					node.prev = newnode
					newnode.next = node
				else:									# node is first node
					newnode.next = node
					node.prev = newnode
					self.first = newnode
			if comes_before(node.val, val):				# node comes after
				if node.next == None:					# last node case
					newnode = OrderedNode(val)
					node.next = newnode
					newnode.prev = node
					self.last = newnode
				else:									# recurrsion case
					return self.insert(val, node.next)
		self.size += 1

class OrderedNode:
	def __init__(self, val, prev = None, next = None):
		self.val = val
		self.prev = prev
		self.next = next
		
	def __repr__(self):
#		return "%s NEXT: %s" % (self.val, self.next)
		return "%s" % (self.val)
			
#returns true if tree rooted at node a comes before tree rooted at node b 
def comes_before (a, b) :
	if a.freq == b.freq:
		return a.char < b.char
	else:
		return a.freq < b.freq

# string -> list
# accepts a string, returns a list of character occurences in file with name string
def cnt_freq(filename):
	chars = [0]*256
	file = open(filename, "r")
	for line in file:
		for char in line:
			ascii = ord(char)
			chars[ascii] += 1
	file.close()
	return chars


# list -> list
# accepts a list of character occurences, returns a list of huffman nodes
def create_huff_list(chars):
	nodelist = OrderedLink()
	for i in range(len(chars)):
		if chars[i] > 0:
			newnode = HuffmanNode(i, chars[i])
			nodelist.insert(newnode)
	return nodelist

# node node -> int
# accepts two nodes, returns the sum of their frequencies
def new_freq(a, b):
	return a.freq + b.freq
	
# node node -> char
# accepts two nodes, returns the min of their characters
def new_char(a, b):
	return min(a.char, b.char)
	
# list -> node
# accepts a node list, creates a newnode from the first 2 nodes
def create_huff_node(hufflist):
	a = hufflist.pop()
	b = hufflist.pop()
	freq = new_freq(a, b)
	char = new_char(a, b)
	newnode = HuffmanNode(char, freq)
	newnode.left = a
	newnode.right = b
	return newnode
	
# list -> HuffmanNode
# accepts a list of charater frequencies, returns the root node of a huffman tree
def create_huff_tree(chars):
	hufflist = create_huff_list(chars)
	while hufflist.size != 1:
		newnode = create_huff_node(hufflist)
		hufflist.insert(newnode)
	return hufflist.first.val

# node -> 

def find_code(node, array, currcode = ""):
	if node.is_leaf():
		array[node.char] = currcode
	else:
		if node.right != None:
			coderight = currcode + "1"
			find_code(node.right, array, coderight)
		if node.left != None:
			codeleft = currcode + "0"
			find_code(node.left, array, codeleft)

# node -> list
# accepts the root node of a huffman tree, returns a list of codes for each char
def create_code (node):
	codelist = [""]*256
	find_code(node, codelist)
	return codelist
	
	
###								PART B									###

def huffman_encode(in_file, out_file):
	freq_array = cnt_freq(in_file)
	hufftree = create_huff_tree(freq_array)
	codelist = create_code(hufftree)
	try:
		input = open(in_file, "r")
		output = open(out_file, "w")
	except:
		raise OSError
	newstring = ""
	for line in input:
		for char in line:
			codechar = codelist[ord(char)]
			newstring += codechar
	output.write(newstring)
	input.close()
	output.close()
	


def huffman_decode(freq_array, encoded_file, decode_file):
	hufftree = create_huff_tree(freq_array)
	try:
		infile = open(encoded_file, "r")
		outfile = open(decode_file, "w")
	except:
		raise OSError
	node = hufftree
	newstring = ""
	for line in infile:
		for char in line:
			if char == "0":
				node = node.left
			if char == "1":
				node = node.right
			if node.is_leaf():
				newstring += (chr(node.char))
				node = hufftree
	outfile.write(newstring)
	infile.close()
	outfile.close()
				
def tree_preord (node, string = ''):
	if node.is_leaf():
		string += '1' + str(chr(node.char))
		return string
	if node.left != None:
		string = tree_preord(node.left, string + '0')
	if node.right != None:
		string = tree_preord(node.right, string)
	return string

