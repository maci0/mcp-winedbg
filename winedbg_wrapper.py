import subprocess
import pty
import os
import select
import threading
import shutil

class WineDbgWrapper:
    def __init__(self):
        self.process = None
        self.master_fd = None
        self.slave_fd = None
        self.thread = None
        self.started = threading.Event()
        if not self.is_winedbg_installed():
            raise RuntimeError("winedbg is not installed. Please install it to use this wrapper.")

    def is_winedbg_installed(self):
        return shutil.which("winedbg") is not None

    def _run_in_thread(self, command):
        self.master_fd, self.slave_fd = pty.openpty()
        self.process = subprocess.Popen(
            command,
            shell=True,
            stdin=self.slave_fd,
            stdout=self.slave_fd,
            stderr=self.slave_fd,
            close_fds=True
        )
        self.started.set()
        self.process.wait()

    def start(self, command):
        self.thread = threading.Thread(target=self._run_in_thread, args=(command,))
        self.thread.start()
        self.started.wait()
        return self.read_output()

    def read_output(self):
        if not self.master_fd:
            return ""
        
        output = ""
        while True:
            r, _, _ = select.select([self.master_fd], [], [], 0.1)
            if not r:
                break
            data = os.read(self.master_fd, 1024)
            if not data:
                break
            output += data.decode(errors='ignore')
        return output

    def send_command(self, command):
        if not self.process:
            return "winedbg not running."
        
        os.write(self.master_fd, (command + '\n').encode())
        return self.read_output()

    def run(self, executable):
        return self.start(f"winedbg {executable}")

    def attach(self, pid):
        return self.start(f"winedbg --pid {pid}")

    def quit(self):
        response = self.send_command("quit")
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
        if self.master_fd:
            os.close(self.master_fd)
            self.master_fd = None
        if self.slave_fd:
            os.close(self.slave_fd)
            self.slave_fd = None
        if self.thread:
            self.thread.join()
            self.thread = None
        return response

    def detach(self):
        return self.send_command("detach")

    def kill(self):
        return self.send_command("kill")

    def cont(self):
        return self.send_command("cont")

    def break_at(self, location):
        return self.send_command(f"break {location}")

    def watch(self, address):
        return self.send_command(f"watch {address}")

    def info_break(self):
        return self.send_command("info break")

    def delete_breakpoint(self, number):
        return self.send_command(f"delete {number}")

    def backtrace(self):
        return self.send_command("bt")

    def frame(self, number):
        return self.send_command(f"frame {number}")

    def up(self):
        return self.send_command("up")

    def down(self):
        return self.send_command("down")

    def step(self):
        return self.send_command("step")

    def next(self):
        return self.send_command("next")

    def stepi(self):
        return self.send_command("stepi")

    def nexti(self):
        return self.send_command("nexti")

    def finish(self):
        return self.send_command("finish")

    def print_var(self, expression):
        return self.send_command(f"print {expression}")

    def examine_memory(self, address):
        return self.send_command(f"x {address}")

    def info_locals(self):
        return self.send_command("info locals")

    def info_args(self):
        return self.send_command("info args")

    def info_proc(self):
        return self.send_command("info proc")

    def info_threads(self):
        return self.send_command("info threads")

    def info_share(self):
        return self.send_command("info share")