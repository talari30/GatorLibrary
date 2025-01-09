import time
import sys
class RBTreeNode:
    def __init__(self, book_id, book_name, author_name, availability_status, borrowed_by):
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.availability_status = availability_status
        self.borrowed_by = borrowed_by
        self.reservation_heap = []  # Binary Min-heap for reservations

        # Red-Black Tree properties
        self.color = "RED"
        self.left = None
        self.right = None
        self.parent = None

class MinHeap:
    def __init__(self):
        self.heap = []

    def heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index] < self.heap[parent_index]:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def heapify_down(self, index):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index

        if left_child_index < len(self.heap) and self.heap[left_child_index] < self.heap[smallest]:
            smallest = left_child_index

        if right_child_index < len(self.heap) and self.heap[right_child_index] < self.heap[smallest]:
            smallest = right_child_index

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.heapify_down(smallest)

    def push(self, element):
        self.heap.append(element)
        self.heapify_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)
        return root
    def __iter__(self):
        return iter(self.heap)

class GatorLibrary:
    def __init__(self):
        self.red_black_tree = RedBlackTree()
        self.reservation_heap = MinHeap()

    def PrintBook(self, book_id):
        found_book = self._find_book(self.red_black_tree.root, book_id)
        if found_book:
            print(f"BookID: {found_book.book_id}, '\n' BookName: {found_book.book_name}, '\n' "
                  f"Author: {found_book.author_name}, '\n' Availability: {found_book.availability_status}, '\n' "
                  f"BorrowedBy: {found_book.borrowed_by}")
        else:
            print(f"Book {book_id} not found in the Library")

    def _find_book(self, node, book_id):
        if node == self.red_black_tree.NIL:
            return None  # Book not found, return None

        if node.book_id == book_id:
            return node

        if book_id < node.book_id:
            return self._find_book(node.left, book_id)
        else:
            return self._find_book(node.right, book_id)
        
    def PrintBooks(self, book_id1, book_id2): # to print the books in range of Book_ID1,Book_ID2
        for book_id in range(book_id1, book_id2 + 1):
            found_book = self._find_book(self.red_black_tree.root, book_id)
            if found_book:
                print(f"BookID: {found_book.book_id}, BookName: {found_book.book_name}, "
                      f"Author: {found_book.author_name}, Availability: {found_book.availability_status}, "
                      f"BorrowedBy: {found_book.borrowed_by}")
            # else:
            #     print(f"Book {book_id} not found in the Library")
   

    def BorrowBook(self, patron_id, book_id, patron_priority):
        book_node = self._find_book(self.red_black_tree.root, book_id)

        if book_node:
            if book_node.availability_status == "available":
                # Book is available, update status and record borrower
                book_node.availability_status = "borrowed"
                book_node.borrowed_by = patron_id
                print(f"Book {book_id} borrowed by Patron {patron_id}")
            else:
                # Book is currently unavailable, create reservation node in the heap
                reservation_node = (patron_id, patron_priority, time.time())
                if not book_node.reservation_heap:
                    book_node.reservation_heap = MinHeap()  # Initialize the heap if not already done
                book_node.reservation_heap.push(reservation_node)
                print(
                    f"Book {book_id} is currently unavailable. Reservation made for Patron {patron_id} with priority {patron_priority}")
        else:
            print(f"Book {book_id} not found in the Library")
    def ReturnBook(self, patron_id, book_id):
        book_node = self._find_book(self.red_black_tree.root, book_id)

        if book_node:
            if book_node.availability_status == "borrowed" and book_node.borrowed_by == patron_id:
                book_node.availability_status = "available"
                book_node.borrowed_by = None
                print(f"Book {book_id} returned by Patron {patron_id}")

                # Check if there are reservations for the returned book
                if book_node.reservation_heap:
                    # Assign the book to the patron with the highest priority in the Reservation Heap
                    reservation = book_node.reservation_heap.pop()
                    assigned_patron_id, _, _ = reservation
                    book_node.availability_status = "borrowed"
                    book_node.borrowed_by = assigned_patron_id
                    print(f"Book {book_id} assigned to Patron {assigned_patron_id}")
            else:
                print(f"Book {book_id} is either not borrowed by Patron {patron_id} or not found in the Library")
        else:
            print(f"Book {book_id} not found in the Library")
    

    def _notify_patrons(self, reservation_heap):
        if reservation_heap:
            while reservation_heap.heap:
                patron_id, _, _ = reservation_heap.pop()
                print(f"Patron {patron_id}, the book you reserved is no longer available.")

    
    def FindClosestBook(self, target_id):
        closest_books = self._find_closest_books(self.red_black_tree.root, target_id)
        
        if closest_books:
            for book in closest_books:
                print(f"BookID: {book.book_id}, BookName: {book.book_name}, "
                      f"Author: {book.author_name}, Availability: {book.availability_status}, "
                      f"BorrowedBy: {book.borrowed_by}")
        else:
            print("No books found in the Library")

    def _find_closest_books(self, node, target_id):
        closest_books = []
        
        while node != self.red_black_tree.NIL:
            closest_books.append(node)
            
            if target_id < node.book_id:
                node = node.left
            elif target_id > node.book_id:
                node = node.right
            else:
                return [node]

        # Find the closest books on both sides
        closest_books_on_left = self._find_closest_book_on_side(node.left, target_id, False)
        closest_books_on_right = self._find_closest_book_on_side(node.right, target_id, True)

        closest_books.extend(closest_books_on_left)
        closest_books.extend(closest_books_on_right)

        return closest_books

    def _find_closest_book_on_side(self, node, target_id, is_right_side):
        closest_books = []

        while node:
            closest_books.append(node)

            if is_right_side:
                if target_id < node.book_id:
                    node = node.left
                else:
                    node = node.right
            else:
                if target_id > node.book_id:
                    node = node.right
                else:
                    node = node.left

        return closest_books


    def Quit(self):
        print("Program Terminated!")




class RedBlackTree:
    def __init__(self):
        self.NIL = RBTreeNode(-1, "", "", "", "")  # Sentinel node with NIL properties
        self.root = self.NIL
        self._color_flip_count = 0  # Update color flips after rotation
    def InsertBook(self, book_id, book_name, author_name, availability_status, borrowed_by):
        new_node = RBTreeNode(book_id, book_name, author_name, availability_status, borrowed_by)
         # Check if the parent is not None before accessing its color
        if new_node.parent is not None and new_node.color == "RED" and new_node.parent.color == "RED":
            self._color_flip_count += 1

        
        self._insert(new_node)
        self._fix_insert(new_node)
       


    def _insert(self, node):
        current = self.root
        parent = None

        while current != self.NIL:
            parent = current
            if node.book_id < current.book_id:
                current = current.left
            else:
                
                current = current.right

        node.parent = parent
        if parent is None:
            self.root = node
        elif node.book_id < parent.book_id:
            parent.left = node
        else:
            parent.right = node

        node.left = self.NIL
        node.right = self.NIL
        node.color = "RED"

    def _fix_insert(self, node):
        while node.parent and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                    self._color_flip_count += 1  # Update color flips
                    
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._right_rotate(node.parent.parent)
                    self._color_flip_count += 1  # Update color flips
            else:
                uncle = node.parent.parent.left
                if uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                    self._color_flip_count += 1  # Update color flips
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._left_rotate(node.parent.parent)
                    self._color_flip_count += 1  # Update color flips

        self.root.color = "BLACK"

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y
        # Update color flips
        if x.color != y.color:
            self._color_flip_count += 1

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right

        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y
        y.parent = x
        # Update color flips
        if x.color != y.color:
            self._color_flip_count += 1
    #searching function
    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        while node != self.NIL and key != node.book_id:
            if key < node.book_id:
                node = node.left
            else:
                node = node.right
        return node
    
    #delete function
    def DeleteBook(self, z):
        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "BLACK":
            self._delete_fixup(x)
         # Update color flips after deletion
        if y_original_color == "BLACK" and x.color == "RED":
            self._color_flip_count += 1
        reservations = list(map(str, z.reservation_heap))
        print(f"Book {z.book_id} is no longer available. Reservations made by Patrons {', '.join(reservations)} have been cancelled!")
    def _transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

#_delete_fixup is function used to fix the tree when a node is deleted
    def _delete_fixup(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._left_rotate(x.parent)
                    w = x.parent.right
                    self._color_flip_count += 1  # Update color flips after rotation
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self._right_rotate(w)
                        w = x.parent.right
                        self._color_flip_count += 1  # Update color flips after rotation
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._right_rotate(x.parent)
                    w = x.parent.left
                    self._color_flip_count += 1  # Update color flips after rotation
                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self._left_rotate(w)
                        w = x.parent.left
                        self._color_flip_count += 1  # Update color flips after rotation
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"
    def ColorFlipCount(self):
        print( self._color_flip_count)

def main(test_file):
    glibrary = GatorLibrary()  # Create an instance of your GatorLibrary
    output_file_name = f'output_{test_file.split(".")[0]}.txt'  # Assuming test_file is like 'test_1.txt'

    # Open the output file in write mode
    with open(output_file_name, 'w') as output_file:
        # Redirect the print statements to the output file
        original_stdout = sys.stdout  # Save a reference to the original standard output
        sys.stdout = output_file

        # Open and read the input file
        with open(test_file, 'r') as file:  # Ensure test_file is a string
            for line in file:
                line = line.strip()
                if line.startswith('#') or line == "":
                    continue  # Skip comments and empty lines
                try:
                    exec(line)
                except Exception as e:
                    print(f"Error executing command '{line}': {e}")

        # Reset the standard output to its original value
        sys.stdout = original_stdout

    glibrary.Quit()  # Indicate the program has ended

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 gatorlibrary.py test_file.txt")
        sys.exit(1)
    main(sys.argv[1])

