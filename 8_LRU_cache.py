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

from time import sleep
class RemoteServer:
	def __init__(self):
		self.data = {
			"dog" : "img_dog",
			"cat" : "img_cat",
			"sea" : "img_sea",
			"ocean": "img_ocean",
			"pizza": "img_pizza",
			"cookie": "img_cookie",
		}

	def request(self, key: str) -> str:
		sleep(1) # simulating delay in request
		if key not in self.data:
			raise KeyError("Requested item not available.")

		return self.data[key]

class Node:
	def __init__(self, key: str, value: str) -> None:
		self.key = key
		self.val = value

		self.next = None
		self.prev = None

class LRUCache:
	def __init__(self, capacity: int) -> None:
		self.cap = capacity
		self._cache = {} # key: int - value: Node(key, value)
		
		self._left = Node(0, 0) # points to least recently used
		self._right = Node(0, 0) # points to most recently used

		self._left.next = self._right # initialize interconnected. 
		self._right.prev = self._left

	# don't need this anymore, handled neatly
	# def contains(self, key: str) -> bool:
	# 	return (key in self._cache)

	def _insert(self, node: Node) -> None:
		# we always insert to the right
		prev, nxt = self._right.prev, self._right

		node.prev = prev
		node.next = nxt

		prev.next = node
		nxt.prev = node


	def _remove(self, node: Node) -> None:
		prev, nxt = node.prev, node.next

		prev.next = nxt
		nxt.prev = prev


	def get(self, key: str) -> str:
		if key not in self._cache:
			raise KeyError("Key not found.")

		# if key in self.cache:
		self._remove(self._cache[key]) # remove it
		self._insert(self._cache[key]) # add it to the most recently used position

		return self._cache[key].val

	def put(self, key : str, value : str) -> None:
		# if key is already in cache then we replace it's value
		if key in self._cache:
			self._remove(self._cache[key])

		self._cache[key] = Node(key, value) # insert into the dictionary
		self._insert(self._cache[key]) # insert into the linked list

		if len(self._cache) > self.cap: # evict
			lru = self._left.next
			
			self._remove(lru) # remove from the linked list
			del self._cache[lru.key] # remove from the hashmap

		return f"Value: {value} successfully added to cache with Key: {key}"

class LocalServer:
	def __init__(self, mainServer: RemoteServer) -> None:
		self.cache = LRUCache(2)
		self.remote = mainServer

	def request(self, key: str) -> str:
		# handle it neatly
		try:
			return self.cache.get(key) # if it is already in the local cache, then simply return it
		except KeyError: # if it is not present
			data = self.remote.request(key) # put it in the cache
			self.cache.put(key, data)
			return data

import time
def main():
	remote = RemoteServer()
	local = LocalServer(remote)

	while True:
		key = input("Search (or 'exit'):")

		if key == "exit":
			break

		try:
			print(local.request(key))
		except KeyError as e:
			print(e)

	
if __name__ == "__main__":
	main()
