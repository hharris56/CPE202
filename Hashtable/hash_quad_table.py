class HashTableQuadPr:                                                  #quadratic probing
	def __init__(self, cap = 251):
		self.cap = cap
		self.table = [None]*self.cap
		self.count = 0
		self.alph = None

	def __repr__(self):
		return "\nTable: %s\nCapacity: %s\nCount: %s\nAlphebetical: %s" % (self.table, self.cap, self.count, self.alph)

	def myhash(self, key, size):
		output = 0
		for i in range(len(key)):
			output += (ord(key[i])*31**(min(len(key), 8) - 1 - i))
		return int(output % size)

	def insert(self, key, line):
		hashval = self.myhash(key, self.cap)
		n = 0
		placed = False
		while self.table[(hashval + n**2) % self.cap] != None:
			if self.table[(hashval + n**2) % self.cap][0] == key:			# duplicate
				if line not in self.table[(hashval + n**2) % self.cap][1]:	# check to see if duplicate line
					self.table[(hashval + n**2) % self.cap][1].append(line)
				placed = True
				break
			else:
				n += 1
		if placed == False:												# not a duplicate
			if type(line) != list:										# make val into array if not already (rehash passes array to this function)
				line = [line]
			self.table[(hashval + n**2) % self.cap] = (key, line)
			self.count += 1
		if self.get_load_fact() > 0.75:									# rehash
			newhash = HashTableQuadPr(self.cap*2+1)
			for val in self.table:
				if val != None:
					newhash.insert(val[0], val[1])
			self.cap = newhash.cap
			self.table = newhash.table
			self.count = newhash.count

	def find(self, key):
		hashval = self.myhash(key, self.cap)
		n = 0
		found = False
		while self.table[(hashval + n**2) % self.cap] != None:
			if self.table[(hashval + n**2) % self.cap][0] == key:
				found = True
				break
			else:
				n += 1
		return found

	def get(self, key):
		hashval = self.myhash(key, self.cap)
		n = 0
		while self.table[(hashval + n**2) % self.cap] != None:
			if self.table[(hashval + n**2) % self.cap][0] == key:
				return self.table[(hashval + n) % self.cap][1]
			else:
				n += 1
		return found

	def read_stop(self, filename):
		file = open(filename, "r")
		i = 0
		for line in file:
			stripline = line.rstrip("\r\n")
			self.insert(stripline, None)
		file.close()

	def read_file(self, filename, stop_table):
		file = open(filename, "r")
		i = 0
		for line in file:
			i += 1
			stripline = line.rstrip("\r\n")
			for word in stripline.split():
				newword = self.make_word(word)
				if not stop_table.find(word):
					self.insert(newword, i)
					self.order(newword)
		file.close()

	def order(self, key):
		if self.alph == None:
			self.alph = [key]
		for i in range(len(self.alph)):
			if key == self.alph[i]:
				break
			if key < self.alph[i]:
				self.alph.insert(i, key)
				break
			elif i == len(self.alph) - 1:
				self.alph.append(key)

	def save_concordance(self, output_filename):
		file = open(output_filename, "w")
		for key in self.alph:
			stringoccur = ""
			stringkey = "%s:\t" % key
			occur = self.get(key)
			for num in occur:
				stringoccur += "%s " % num
			stringoccur = stringoccur[:-1]								# remove unwanted space
			outstring = stringkey + stringoccur + "\n"
			if self.alph.index(key) == len(self.alph) - 1:
				outstring = outstring[:-1]
			file.write(outstring)
		file.close()

	def get_tablesize(self):
		return self.cap

	def make_word(self, word):
		output = ""
		for letter in word:
			if letter.isalpha():
				output += (letter.lower())
		return output

	def get_load_fact(self):
		return self.count / self.cap