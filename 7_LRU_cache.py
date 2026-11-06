"""
LLD Problem: Design an in-memory LRU cache that has a fixed capacity. Each request would either be GET or PUT, and they should be answered in constant time.
"""

"""
Each PUT needs a key and a value because each GET will need a key to fetch the value.
Think of requesting something on Google. If we search for a "dog", that is the key and the search result is the "value"
Someone will have put the key-value pair into the database or cache.
Then when someone calls using GET("dog"), that'd return the "value" associated with the dog


We'll use a doubly linked list to store the key and value, and our cache would be a hashmap.

Node:
- key: int
- value: int 
- next: Node 
- prev: Node

LRUCache:
- capacity: int
- cache: dict(key: int, value: Node(key, value))
- left: Least Recently Used node # We evict this
- right: Most Recently Used node 

- insert(Node) -> None
- remove(Node) -> None
- put(key, value) -> None
- get(key) -> int


# Whenever we GET something, we will make it the most recently used if it is in the cache
# Whenever we PUT something, we will check capacity. If capacity is full, we will evict the least recently used and insert at the right
"""

class Node:
	def __init__(self, key: int, value: int) -> None:
		self.key = key
		self.val = value

		self.next = None
		self.prev = None

class LRUCache:
	def __init__(self, capacity: int) -> None:
		self.cap = capacity
		self.cache = {} # key: int - value: Node(key, value)
		
		self.left = Node(0, 0) # points to least recently used
		self.right = Node(0, 0) # points to most recently used

		self.left.next = self.right # initialize interconnected. 
		self.right.prev = self.left

	def insert(self, node: Node) -> None:
		# we always insert to the right
		prev, nxt = self.right.prev, self.right

		node.prev = prev
		node.next = nxt

		prev.next = node
		nxt.prev = node


	def remove(self, node: Node) -> None:
		prev, nxt = node.prev, node.next

		prev.next = nxt
		nxt.prev = prev


	def get(self, key: int) -> int:
		if key not in self.cache:
			raise ValueError("Key not found.")

		# if key in self.cache:
		self.remove(self.cache[key]) # remove it
		self.insert(self.cache[key]) # add it to the most recently used position

		return self.cache[key].val

		# return -1 # if it is not present

	def put(self, key : int, value : int) -> None:
		# if key is already in cache then we replace it's value
		if key in self.cache:
			self.remove(self.cache[key])

		self.cache[key] = Node(key, value) # insert into the dictionary
		self.insert(self.cache[key]) # insert into the linked list

		if len(self.cache) > self.cap: # evict
			lru = self.left.next
			
			self.remove(lru) # remove from the linked list
			del self.cache[lru.key] # remove from the hashmap

		return f"Value: {value} successfully added to cache with Key: {key}"


try:
	cache = LRUCache(2)
	print(cache.put(1, 10))
	print(cache.get(1))
	print(cache.put(2, 20))
	print(cache.put(3, 30))
	print(cache.get(2))
	print(cache.get(1))
except ValueError as e:
	print(e)