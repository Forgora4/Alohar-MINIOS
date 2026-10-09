import os
import time

class alohar:
    def __init__(self, hostname = "aloharos", username="root"):
        self.hostname = hostname
        self.username = username
        self.boot_time = time.time()
        self.is_running = True
        
        self.cmd = {
            "help": self.cmdhelp,
            "clear": self.cmdclear,
            "uptime": self.uptime,
            "exit": self.exit
            # diri ka add sang new commands ninyo like "cd": self.cd
        }
    
    def run(self):
        print("aloharOS CLI")
        print("help for commands ")
        
        while self.is_running:
            raw_input = input ("aloharos# ").strip()
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

    def exit(self, args):
        print("Goodbye!")
        self.is_running = False

    #Diri kamo add new commands, ninyo try lang follow format ko like def 
    # cd(self, args):
    # Command to change directory
    

if __name__ == "__main__":
    app = alohar()
    app.run()