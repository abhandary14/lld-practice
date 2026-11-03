"""
LLD Problem: Design a Circular Double Ended Queue

A circular queue (aka ring buffer / circular buffer) is a linear data structure which acts like a double ended queue, allowing operations at both the front and the rear. 

The last position is connected back to the first position to make a circle.
"""

"""
CircularQueue: k (size)
- insertFront(value)
- insertLast(value)
- deleteFront()
- deleteLast()
- getFront() -> return -1 if doesn't exist
- getRear() -> return -1 if doesn't exist
- isEmpty()
- isFull()
"""

class CircularDeque:
    def __init__(self, k: int):
        self.queue = [0] * k
        self.k = k

        self.size = 0

        self.front = 0
        self.rear = -1

    def insertFront(self, value: int) -> bool:
        if self.isFull():
            return False

        self.front = (self.front - 1) % self.k
        self.queue[self.front] = value

        self.size += 1

        return True

    def insertRear(self, value: int) -> bool:
        if self.isFull():
            return False

        self.rear = (self.rear + 1) % self.k
        self.queue[self.rear] = value

        self.size += 1

        # -> when we insert the fist element, the front and the rear are the same
        if self.size == 1:
            self.rear = self.front 

        return True

    def deleteFront(self) -> bool:
        if self.isEmpty():
            return False

        self.front = (self.front + 1) % self.k
        self.size -= 1

        return True

    def deleteRear(self) -> bool:
        if self.isEmpty():
            return False

        # add self.k to handle the case if rear becomes negative
        self.rear = (self.rear - 1 + self.k) % self.k
        self.size -= 1

        return True

    def getFront(self) -> int:
        if self.isEmpty():
            return -1

        return self.queue[self.front]

    def getRear(self) -> int:
        if self.isEmpty():
            return -1

        return self.queue[self.rear]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.k


def main():
    cideuqe = CircularDeque(3)
    
    print(cideuqe.insertRear(1))
    print(cideuqe.insertRear(2))
    print(cideuqe.insertFront(3))
    print(cideuqe.insertFront(4))
    print(cideuqe.getRear())
    print(cideuqe.isFull())
    print(cideuqe.deleteRear())
    print(cideuqe.insertFront(4))
    print(cideuqe.getFront())

if __name__ == "__main__":
    main()