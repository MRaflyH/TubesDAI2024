class Individual:
    def __init__(self, data):
        self.data = data
        self.next = None

class Population:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Individual(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    # Method to insert a new node at a specific position
    def insert(self, data, position):
        new_node = Individual(data)
        if position == 0:
            new_node.next = self.head
            self.head = new_node
            return
        current = self.head
        for _ in range(position - 1):
            if current is None:
                raise IndexError("Position out of bounds")
            current = current.next
        new_node.next = current.next
        current.next = new_node

    # Method to remove a node with specific data
    def remove(self, data):
        current = self.head
        if current and current.data == data:
            self.head = current.next
            return
        prev = None
        while current and current.data != data:
            prev = current
            current = current.next
        if current is None:
            return  # Data not found
        prev.next = current.next

    # Method to display the linked list
    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")
