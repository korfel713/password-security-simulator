import itertools
import os
import threading
import time

#class that holds functions for brute force attack
class BruteForce:
    def __init__(self, DB):
        self.DB = DB

        #threading to not freeze the gui, and variables
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()

        self.start_time = None
        self.elapsed_time = 0
        self.counter = 1
        self.max_length = 0

        self.thread = None

    #begin the attack, set variables, start the brute force thread.
    def start_attack(self, password, charset, output, db_update):
        if not password:
            output("Error: No password entered.")
            return

        self.max_length = 12
        self.stop_event.clear()
        self.pause_event.set()
        self.elapsed_time = 0
        self.start_time = time.time()
        self.counter = 1
        self.thread = threading.Thread(
            target=self.brute_force,
            args=(self.max_length, charset, password, output, db_update),
            daemon=True
        )
        self.thread.start()

    def brute_force(self, max_length, charset, password, output, db_update):
        output(f"Starting attack on {password}...")

        # Check a password wordlist before starting character-by-character brute force.
        # The original team project used a large 2M+ password file. This portfolio
        # version includes a small sample list so the repository stays lightweight.
        resource_dir = os.path.join(os.path.dirname(__file__), "..", "Resources")
        full_wordlist = os.path.join(resource_dir, "2151220-passwords.txt")
        sample_wordlist = os.path.join(resource_dir, "common-passwords-sample.txt")
        wordlist_path = full_wordlist if os.path.exists(full_wordlist) else sample_wordlist

        if os.path.exists(wordlist_path):
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    self.counter += 1
                    if self.stop_event.is_set():
                        return
                    self.pause_event.wait()

                    test = line.strip()
                    if test == password:
                        output(f"Found password in password file: {test}")
                        output(f"Number of attempts: {self.counter}")
                        self.elapsed_time += time.time() - self.start_time
                        output(f"Time: {self.elapsed_time:.2f} seconds.")
                        db_update(password, self.elapsed_time, self.counter)
                        self.counter = 1
                        return

        #Up to the max length of the password allowed, try the full charset with one character, then 2, so on.
        for length in range(1, max_length + 1):
            for attempt in itertools.product(charset, repeat=length):
                if self.stop_event.is_set():
                    return
                self.pause_event.wait()
                guess = ''.join(attempt)
                #If found, display to gui and update database.
                # or alternative case for hitting maximum allotted time (5 min)
                if guess == password or (time.time() + self.elapsed_time - self.start_time) > 300:
                    if guess == password:
                        output(f"Found password by brute force: {guess}.")
                        self.elapsed_time += time.time() - self.start_time
                        output(f"Time: {self.elapsed_time:.2f} seconds.")
                    else:
                        output(f"Reached max time for brute force.")
                        self.elapsed_time += time.time() - self.start_time
                        output(f"Time: {self.elapsed_time:.2f} seconds.")
                        self.elapsed_time = 999999

                    output(f"Number of attempts: {self.counter}\n")
                    db_update(password, self.elapsed_time, self.counter)
                    self.counter = 1
                    return
                else:
                    self.counter+=1
        #this is unlikely to run because we're getting into 26^12 attempts.
        output("Password has characters not in selected charset, choose another and try again.")

    #Pause the attack. Reset the pause, save the time ran so far, send to gui, reset time for next session.
    def pause_attack(self, output):
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.elapsed_time += time.time() - self.start_time
            output(f"Paused at {self.elapsed_time:.2f} seconds.")
            output(f"Number of attempts so far: {self.counter}.\n")
            self.start_time = None
        #resume, start function and then timer.
        else:
            self.pause_event.set()
            self.start_time = time.time()
            output("Resumed.")

    #Stop attack, reset the pause, reset the timer in case it's still paused, send to output. No database output here.
    def end_attack(self, output):
        self.stop_event.set()
        self.pause_event.set()  # in case it's paused, reset
        if self.start_time is None:
            self.start_time = time.time()
        self.elapsed_time += time.time() - self.start_time
        output(f"Attack stopped early at {self.elapsed_time:.2f}")
        output(f"Number of attempts: {self.counter}\n")
        self.counter = 1