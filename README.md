# Library Management System (Python | CLI + Client-Server + SQLite)

A distributed Library Management System built using Python. The project combines a command-line interface (CLI), client-server communication using sockets, and SQLite database integration to simulate a real-world library system with user authentication, book management, borrowing, and returning functionalities.

---

## Project Overview

This system models a real library environment where users interact with a server through a CLI-based client application. The server manages core operations such as user registration, book borrowing, returns, and database updates, while ensuring synchronization between in-memory data and persistent storage.

The project demonstrates advanced Python concepts including modular programming, socket communication, database management, and object-oriented design.

---

## System Architecture

The system is divided into three main layers:

### 1. Client Layer (user.py)
- Handles user interaction via CLI
- Sends requests to the server (signup, signin, borrow, return, view books)
- Receives and displays server responses
- Maintains local user session state

### 2. Server Layer (server.py)
- Central processing unit of the system
- Handles all incoming client requests via sockets
- Parses requests using regex patterns
- Coordinates operations between users, books, and database
- Enforces approval before executing actions

### 3. Data Layer (database.py + library.db)
- SQLite database stores persistent data:
  - users
  - books
  - borrow_history
- Handles all CRUD operations
- Ensures data consistency across sessions

---

## Core Features

- User signup and signin system (with unique ID generation)
- Book management (add, store, and track availability)
- Borrowing system with due-date calculation
- Return system with validation (ensures only borrower can return)
- Borrow history tracking (timestamps for borrow and return)
- Real-time synchronization between server and database
- Socket-based client-server communication
- CLI-based user interaction

---

## Book System Features

Each book contains:
- Title
- Author
- Year
- Borrow duration
- Borrowed status
- Borrow timestamp
- Return timestamp (calculated using timezone-aware datetime logic)

---

## Database Schema

### Users Table
- user_id
- name
- sex
- email
- phone_number

### Books Table
- book_id
- book_name
- year
- author
- borrow_time
- borrowed

### Borrow History Table
- user_id
- name
- sex
- email
- phone_number
- book_borrowed
- datetime_borrowed
- datetime_returned
- returned

---

## Technologies Used

- Python 3
- SQLite (library.db)
- socket programming (TCP server-client model)
- pickle (data serialization)
- regex (request parsing)
- datetime + timezone handling
- Object-Oriented Programming (OOP)
- Modular architecture

---

## Key Concepts Demonstrated

- Client-server architecture using sockets
- Real-world system simulation
- Persistent database management
- Data synchronization between memory and storage
- Command-line interface design
- Input validation and request parsing
- Modular software design principles
- Time-based logic (borrow/return deadlines)

---

## How the System Works

1. Client starts and either signs up or signs in
2. Client sends structured requests to server using sockets
3. Server parses request using regex patterns
4. Server validates user actions (approval system)
5. Server updates:
   - in-memory book/user lists
   - SQLite database
6. Server sends response back to client
7. Client displays result in CLI

---

## Notable Design Decisions

- Use of socket communication instead of local-only CLI makes the system distributed
- SQLite ensures persistent storage across sessions
- Separation into modules improves scalability and readability
- Borrow/return logic includes validation to prevent unauthorized actions
- Timezone-aware timestamps used for accurate tracking

---

## What I Learned

- How to design a multi-layer software system
- How client-server communication works in Python
- How to integrate SQLite with live application logic
- How to structure medium-complexity software projects
- How real-world systems coordinate multiple components
- Importance of validation, state management, and error handling

---

## Future Improvements

- Replace pickle with JSON for safer communication
- Add authentication and password system
- Replace CLI with GUI or web interface
- Improve concurrency handling for multiple clients
- Add encryption for client-server communication
- Refactor into cleaner service-oriented architecture

---

## Conclusion

This project demonstrates a strong foundation in software engineering principles, combining CLI interaction, networking, and database systems. It represents an early but advanced step toward building real-world distributed applications in Python.