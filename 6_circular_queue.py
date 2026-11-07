"""
LLD Problem: Design a Circular Queue

A circular queue (aka ring buffer / circular buffer) is a linear data structure in which the operations are performed based on the FIFO principle. 

The last position is connected back to the first position to make a circle.
"""

"""
CircularQueue: k (size)
- enQueue(value)
- deQueue()
- Front() -> return element at the front; if not return -1
- Rear() -> return element at the rear
- isEmpty()
- isFull()
"""

class CircularQueue:
    def __init__(self, k: int):
        self.queue = [0] * k
        self.k = k
        self.size = 0 # starting size = 0
        self.front = 0
        self.rear = 0
        

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False

        self.queue[self.rear] = value
        self.rear = (self.rear + 1) % self.k # maintain circular nature. adding at the last index should lead rear back to 0

        self.size += 1

        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False

        self.front = (self.front + 1) % self.k # maintain circular nature -> removing the last element should lead front back to 0

        self.size -= 1

        return True

    def Front(self) -> int:
        if self.isEmpty():
            return -1

        return self.queue[self.front]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1

        return self.queue[(self.rear - 1) % self.k] # maintain circular nature

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.k


def main():
    cique = CircularQueue(3)
    print(cique.enQueue(1))
    print(cique.enQueue(2))
    print(cique.enQueue(3))
    print(cique.enQueue(4))
    print(cique.Rear())
    print(cique.isFull())
    print(cique.deQueue())
    print(cique.enQueue(4))
    print(cique.Rear())

if __name__ == "__main__":
    main()