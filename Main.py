import os
import getpass
import hashlib
import hmac
import shutil
import shlex
import struct
import time
from datetime import datetime
# LUIS- Main CLI framework
class alohar:
    def __init__(self, hostname = "aloharos", username="root"):
        self.hostname = hostname
        self.username = username
        self.is_authenticated = False
        # Demo accounts: admin/admin and student/student.
        self.users = {
            "admin": hashlib.sha256("admin".encode()).hexdigest(),
            "student": hashlib.sha256("student".encode()).hexdigest()
        }
        self.boot_time = time.time()
        self.is_running = True
        self.processes = {}
        self.next_pid = 1
        self.total_memory = 4096
        self.used_memory = 0
        
        self.cmd = {
            "help": self.cmdhelp,
            "clear": self.cmdclear,
            "uptime": self.uptime,
            "time": self.show_time,
            "whoami": self.whoami,
            "users": self.list_users,
            "login": self.login,
            "logout": self.logout,
            "systeminfo": self.systeminfo,
            "exit": self.exit,
            "process": self.process,
            "run": self.run_process,
            "kill": self.kill,
            "memory": self.memory,
            "allocate": self.allocate,
            "free": self.free,
            "pwd": self.pwd,
            "ls": self.ls,
            "cd": self.cd,
            "cat": self.cat,
            "read": self.cat,
            "create": self.create_file,
            "write": self.write_file,
            "delete": self.delete_file,
            "mkdir": self.make_directory,
            "rmdir": self.remove_directory
            # diri ka add sang new commands ninyo like "cd": self.cd
        }
    
    def run(self):
        # LIS: User Management - require an account login before using AloharOS.
        self.login()
        print("aloharOS CLI")
        print("help for commands ")
        
        while self.is_running:
            if not self.is_authenticated:
                self.login()

            prompt_time = datetime.now().strftime("%H:%M:%S")
            raw_input = input(f"[{prompt_time}] AloharOS# ").strip()
            if not raw_input:
                continue
            try:
                parts = shlex.split(raw_input)
            except ValueError as e:
                print(f"Invalid command syntax: {e}")
                continue
            cmd = parts[0].lower()
            args = parts[1:]
            
            if cmd in self.cmd:
                self.cmd[cmd](args)
            else:
                print(f"Command is unkown: {cmd}")
        
    def cmdhelp(self, args):
        for cmd in self.cmd:
            print(f"- {cmd}")

    def cmdclear(self, args):
        os.system("cls" if os.name == "nt" else "clear")

    def uptime(self, args):
        seconds = int(time.time() - self.boot_time)
        print(f"Uptime: {seconds}s")

    def show_time(self, args):
        print(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def exit(self, args):
        print("Goodbye!")
        self.is_running = False

    # LIS: User Management - authenticate against the built-in demo accounts.
    def login(self, args=None):
        if self.is_authenticated:
            print(f"Already logged in as {self.username}. Log out first.")
            return

        while not self.is_authenticated:
            print("\n" + "+" + "-" * 38 + "+")
            print(f"|{' ALOHAROS LOGIN ':^38}|")
            print("+" + "-" * 38 + "+")
            username = input("\nUsername: ").strip()
            password = getpass.getpass("Password (input hidden): ")
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            if username in self.users and hmac.compare_digest(
                self.users[username], password_hash
            ):
                self.username = username
                self.is_authenticated = True
                print("\nLogin successful.")
                print(f"\nWelcome, {self.username}!")
                return

            print("Invalid username or password. Please try again.\n")

    def logout(self, args):
        if not self.is_authenticated:
            print("No user is currently logged in.")
            return

        print(f"Goodbye, {self.username}.")
        self.username = None
        self.is_authenticated = False

    def whoami(self, args):
        if not self.is_authenticated:
            print("No user is currently logged in.")
            return
        print(f"Current User: {self.username}")

    def list_users(self, args):
        print("Available users:")
        for username in sorted(self.users):
            print(f"- {username}")

    # LIS: System Information - simulated AloharOS hardware details.
    def systeminfo(self, args):
        architecture = f"{struct.calcsize('P') * 8}-bit"
        current_user = self.username if self.is_authenticated else "None"
        border = "+" + "-" * 42 + "+"
        print(border)
        print(f"|{' ALOHAROS SYSTEM INFORMATION ':^42}|")
        print(border)
        print("\nOS Name: AloharOS Alpha")
        print("Version: 1.0.0")
        print(f"Architecture: {architecture}")
        print("CPU: AloharOS Virtual CPU (4 cores)")
        print("Memory: 4096 MB")
        print(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"User: {current_user}")
        print(f"\n{border}")


    # Ondrej: File management developer
    def pwd(self, args):
        print(os.getcwd())

    # Ondrej: File management developer
    def ls(self, args):
        directory = " ".join(args) if args else "."
        try:
            items = os.listdir(directory)
            for item in sorted(items):
                print(f"  {item}")
        except FileNotFoundError:
            print(f"Directory not found: {directory}")
        except NotADirectoryError:
            print(f"Not a directory: {directory}")
        except PermissionError:
            print(f"Permission denied: {directory}")
        except OSError as e:
            print(f"Error listing directory: {e}")

    # Ondrej: File management developer
    def cd(self, args):
        if not args:
            print("Usage: cd <directory>")
            return
        directory = " ".join(args)
        try:
            os.chdir(directory)
            print(f"Moved to: {os.getcwd()}")
        except FileNotFoundError:
            print(f"Directory not found: {directory}")
        except NotADirectoryError:
            print(f"Not a directory: {directory}")
        except PermissionError:
            print(f"Permission denied: {directory}")

    # Ondrej: File management developer
    def cat(self, args):
        if not args:
            print("Usage: cat <filename>")
            return
        filename = " ".join(args)
        try:
            with open(filename, "r", encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print(f"File not found: {filename}")
        except IsADirectoryError:
            print(f"'{filename}' is a directory, not a file.")
        except PermissionError:
            print(f"Permission denied: {filename}")
        except OSError as e:
            print(f"Error reading file: {e}")


    # Ondrej: File management developer
    def create_file(self, args):
        if not args:
            print("Usage: create <filename>")
            return

        filename = " ".join(args)
        try:
            with open(filename, "x", encoding="utf-8"):
                pass
            print(f"File created: {filename}")
        except FileExistsError:
            print(f"File already exists: {filename}")
        except PermissionError:
            print(f"Permission denied: {filename}")
        except OSError as e:
            print(f"Error creating file: {e}")

    # Ondrej: File management developer
    def write_file(self, args):
        if len(args) < 2:
            print('Usage: write <filename> "<text>"')
            return

        filename = args[0]
        text = " ".join(args[1:])
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(text + "\n")
            print(f"Text added to: {filename}")
        except PermissionError:
            print(f"Permission denied: {filename}")
        except OSError as e:
            print(f"Error writing file: {e}")

    # Ondrej: File management developer
    def delete_file(self, args):
        if not args:
            print("Usage: delete <filename>")
            return

        filename = " ".join(args)
        if not os.path.isfile(filename):
            print(f"File not found: {filename}")
            return

        try:
            os.remove(filename)
            print(f"File deleted: {filename}")
        except PermissionError:
            print(f"Permission denied: {filename}")
        except OSError as e:
            print(f"Error deleting file: {e}")

    # Ondrej: File management developer
    def make_directory(self, args):
        if not args:
            print("Usage: mkdir <foldername>")
            return

        directory = " ".join(args)
        try:
            os.mkdir(directory)
            print(f"Folder created: {directory}")
        except FileExistsError:
            print(f"Folder or file already exists: {directory}")
        except PermissionError:
            print(f"Permission denied: {directory}")
        except OSError as e:
            print(f"Error creating folder: {e}")

    # Ondrej: File management developer
    def remove_directory(self, args):
        if not args:
            print("Usage: rmdir <foldername>")
            return

        directory = " ".join(args)
        if not os.path.isdir(directory):
            print(f"Folder not found: {directory}")
            return

        current_directory = os.path.realpath(os.getcwd())
        target_directory = os.path.realpath(directory)
        try:
            if os.path.commonpath(
                [current_directory, target_directory]
            ) != current_directory or target_directory == current_directory:
                print("Permission denied: choose a folder inside the current directory.")
                return
        except ValueError:
            print("Permission denied: choose a folder inside the current directory.")
            return

        confirmation = input(
            f"Delete folder '{directory}' and all its contents? (y/N): "
        ).strip().lower()
        if confirmation != "y":
            print("Folder deletion cancelled.")
            return

        try:
            shutil.rmtree(directory)
            print(f"Folder deleted: {directory}")
        except PermissionError:
            print(f"Permission denied: {directory}")
        except FileNotFoundError:
            print(f"Folder not found: {directory}")
        except OSError as e:
            print(f"Error deleting folder: {e}")

    # PROCESS MANAGEMENT: Display running processes
    def process(self, args):
        if not self.processes:
            print("No running processes.")
            return

        print("\nPROCESS LIST")
        print("-" * 40)
        print(f"{'PID':<8}{'NAME':<20}{'STATUS'}")
        print("-" * 40)

        for pid, process in self.processes.items():
            print(f"{pid:<8}{process['name']:<20}{process['status']}")

    # PROCESS MANAGEMENT: Start a simulated process
    def run_process(self, args):
        if not args:
            print("Usage: run <process_name>")
            return

        process_name = args[0]
        pid = self.next_pid

        self.processes[pid] = {
            "name": process_name,
            "status": "RUNNING"
        }

        self.next_pid += 1

        print("Process started.")
        print(f"PID: {pid}")
        print(f"Name: {process_name}")
        print("Status: RUNNING")

    # PROCESS MANAGEMENT: Terminate a simulated process
    def kill(self, args):
        if not args:
            print("Usage: kill <PID>")
            return

        try:
            pid = int(args[0])

            if pid in self.processes:
                del self.processes[pid]
                print(f"Process {pid} terminated.")
            else:
                print("Error: Process does not exist.")

        except ValueError:
            print("Error: PID must be a number.")

    # MEMORY MANAGEMENT: Display memory status
    def memory(self, args):
        free_memory = self.total_memory - self.used_memory

        print("\nMEMORY STATUS")
        print("-" * 30)
        print(f"Total Memory: {self.total_memory} MB")
        print(f"Used Memory:  {self.used_memory} MB")
        print(f"Free Memory:  {free_memory} MB")

    # MEMORY MANAGEMENT: Allocate simulated memory
    def allocate(self, args):
        if not args:
            print("Usage: allocate <amount_MB>")
            return

        try:
            amount = int(args[0])

            if amount <= 0:
                print("Error: Amount must be greater than zero.")
                return

            free_memory = self.total_memory - self.used_memory

            if amount > free_memory:
                print("Error: Not enough available memory.")
                return

            self.used_memory += amount
            print(f"{amount} MB allocated.")

        except ValueError:
            print("Error: Please enter a valid number.")

    # MEMORY MANAGEMENT: Release simulated memory
    def free(self, args):
        if not args:
            print("Usage: free <amount_MB>")
            return

        try:
            amount = int(args[0])

            if amount <= 0:
                print("Error: Amount must be greater than zero.")
                return

            if amount > self.used_memory:
                print("Error: Cannot release more memory than allocated.")
                return

            self.used_memory -= amount
            print(f"{amount} MB released.")

        except ValueError:
            print("Error: Please enter a valid number.")


    

    

if __name__ == "__main__":
    app = alohar()
    app.run()
