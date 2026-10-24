# ALOHAR MiniOS

Final project in IT3131.

## Group Members

- Luis Raphael Pestaño Argel
- Hanna Alexandra Dela Cruz Caballe
- Ondrej Stefano Cres Francisco Carpio
- Aron Adriel Tangco Siason
- Reynaldo II Delgado Talabucon
- Annyleise Seguera Torrechilla

## Project Description

Alohar MiniOS is a Python-based Mini Operating System simulator that runs through a Command-Line Interface (CLI). It provides users with basic operating system functionalities such as user authentication, file management, process management, memory management, and system monitoring.

The project demonstrates fundamental operating system concepts using a simplified environment implemented in Python.

## Features

### User Management
- Secure user login system
- User logout functionality
- View current logged-in user
- View available users
- Password hashing using SHA-256

### System Utilities
- Help command
- Clear screen
- System uptime tracking
- Real-time system clock
- System information display
- Exit command

### File Management
- Show current working directory
- List files and folders
- Change directories
- Read text file contents

### Process Management
- View running processes
- Start simulated processes
- Terminate simulated processes

### Memory Management
- View memory status
- Allocate simulated memory
- Release allocated memory

### Error Handling
- Invalid command detection
- Invalid login credential handling
- File and directory error handling
- Invalid PID handling
- Memory allocation validation

## Requirements

- Python 3.x installed
- Windows Command Prompt (CMD) or Terminal

## How to Run

1. Download or clone the repository.
2. Extract the ZIP file.
3. Open the project folder.
4. Locate `Main.py`.
5. Double-click `Main.py` to start AloharOS.
6. Log in using one of the demo accounts below.

### Administrator Account

```text
Username: admin
Password: admin
```

### Student Account

```text
Username: student
Password: student
```

## Available Commands

| Command | Description |
|---|---|
| `help` | Display all available commands |
| `clear` | Clear the terminal screen |
| `uptime` | Show system uptime |
| `time` | Display the current system time |
| `whoami` | Show the currently logged-in user |
| `users` | List available users |
| `login` | Log into the system |
| `logout` | Log out from the system |
| `systeminfo` | Display system information |
| `pwd` | Show the current working directory |
| `ls [directory]` | List files and folders in the current or specified directory |
| `cd <directory>` | Change the current directory |
| `mkdir <foldername>` | Create a folder |
| `rmdir <foldername>` | Delete a folder and its contents after confirmation |
| `create <filename>` | Create an empty file without overwriting an existing file |
| `write <filename> "<text>"` | Append a line to a file, creating it if needed |
| `read <filename>` | Display a text file's contents (`cat` also works) |
| `cat <filename>` | Display a text file's contents |
| `delete <filename>` | Permanently delete a file |
| `process` | Display running processes |
| `run <process_name>` | Start a simulated process |
| `kill <PID>` | Terminate a simulated process |
| `memory` | Display memory usage |
| `allocate <amount_MB>` | Allocate simulated memory |
| `free <amount_MB>` | Release simulated memory |
| `exit` | Exit AloharOS |

## Developers

**Group:** ALOHAR  
