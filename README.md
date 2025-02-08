# GatorLibrary

Overview

GatorLibrary is a software system designed to efficiently manage books, users, and borrowing procedures for a fictional library. The system leverages advanced data structures—Red-Black Trees for book organization and Binary Min-Heaps for priority-based book reservations—to ensure optimal performance and seamless user experience.

Features

PrintBook(bookID): Displays detailed information about a book, including its title, author, and availability status.

PrintBooks(bookID1, bookID2): Lists all books within a specified range of bookIDs.

InsertBook(bookID, bookName, authorName, availabilityStatus, borrowedBy, reservationHeap): Adds a new book to the library with all necessary details.

BorrowBook(patronID, bookID, patronPriority): Allows a patron to borrow an available book or reserve it based on priority if unavailable.

ReturnBook(patronID, bookID): Enables book return and assigns the book to the highest-priority patron in the reservation queue.

DeleteBook(bookID): Removes a book from the library and notifies patrons in the reservation list.

FindClosestBook(targetID): Locates the book with the closest ID to a given target ID, displaying details and handling tie scenarios.

ColorFlipCount(): Tracks and reports color flips (red-black transitions) in the Red-Black Tree during operations.

Data Structures Used

1. Red-Black Tree

A self-balancing binary search tree used for efficient book management. Key advantages include:

Logarithmic Time Complexity: Ensures quick book search, insertion, and deletion.

Balancing Properties: Minimizes performance bottlenecks with controlled re-balancing.

Node Structure: Each node stores book details, including bookID, title, author, availability, borrower details, and a reservation queue.

2. Binary Min-Heap

Used for priority-based book reservations:

Ensures that patrons with the highest priority get the book first.

Efficient extraction of the highest-priority reservation.

Implementation Details

Programming Language: Python

Testing Environment: thunder.cise.ufl.edu server

Operations Tracked:

Book insertion and deletion

Borrowing and returning operations

Reservation prioritization

Color flips in the Red-Black Tree

Development & Testing

The system underwent rigorous testing to ensure correctness and efficiency.

Multiple edge cases were handled to guarantee robustness in different scenarios.

Performance analysis was conducted to validate the efficiency of data structure operations.

Future Enhancements

Graphical User Interface (GUI): To improve usability and visualization.

Multi-copy Book Support: Extending functionality to handle multiple copies per book.

User Authentication & Role Management: Implementing access control for library administrators and patrons.
