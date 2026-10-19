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

    #Diri kamo add new commands, ninyo try lang follow format ko like def 
    # cd(self, args):
    # Command to change directory
    

    

if __name__ == "__main__":
    app = alohar()
    app.run()
