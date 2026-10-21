import os
import getpass
import hashlib
import hmac
import struct
import time
from datetime import datetime

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
            "cat": self.cat
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
            parts = raw_input.split()
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


    #Show current working directory path
    def pwd(self, args):
        print(os.getcwd())

        #List files and folders in the current directory
    def ls(self, args):
        try:
            items = os.listdir('.')
            for item in sorted(items):
                print(f"  {item}")
        except Exception as e:
            print(f"Error listing directory: {e}")

            #Change directory (e.g., cd folder_name or cd ..)
    def cd(self, args):
        if not args:
            print("Usage: cd <directory>")
            return
        try:
            os.chdir(args[0])
            print(f"Moved to: {os.getcwd()}")
        except FileNotFoundError:
            print(f"Directory not found: {args[0]}")
        except NotADirectoryError:
            print(f"Not a directory: {args[0]}")
        except PermissionError:
            print(f"Permission denied: {args[0]}")

            #Read and display the contents of a text file
    def cat(self, args):
        if not args:
            print("Usage: cat <filename>")
            return
        try:
            with open(args[0], 'r', encoding='utf-8') as f:
                print(f.read())
        except FileNotFoundError:
            print(f"File not found: {args[0]}")
        except IsADirectoryError:
            print(f"'{args[0]}' is a directory, not a file.")
        except Exception as e:
            print(f"Error reading file: {e}")
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

    #Diri kamo add new commands, ninyo try lang follow format ko like def 
    # cd(self, args):
    # Command to change directory
    

    

if __name__ == "__main__":
    app = alohar()
    app.run()
