# Main File
#this File Hold the code for the Gui using tkinter.
#classes have been made for each page of the gui tha teahc represents a diffrent functionalitiy of the simulator.
#each of these gui pages link to their given python code file where the actuall code of
# the simulater for said function is held.

#libraries Imported
import string

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import Final_Visual
import stored_passwords
import password_creation
import brute_force_attack
import hash_creation
import password_Strength
import Final_Visual
#------------------------------------------------------------------------------------------#
#class that creates and holds the pages for the gui
class App(ttk.Window):
    def __init__(self):
        #difrent bootstrap themes: morph, flatly, darkly, yeti, journal, cyborg, superhero, vapor
        # super().__init__(themename="morph")
        # super().__init__(themename="flatly")
        super().__init__(themename="darkly")
        # super().__init__(themename="yeti")
        # super().__init__(themename="journal")
        # super().__init__(themename="cyborg")
        # super().__init__(themename="superhero")
        # super().__init__(themename="vapor")

        
        # create temporary database and setup close protocol
        self.DB = stored_passwords.DB()
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.title("Password Security & Authentication Simulator")

        # Container that holds all pages
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        self.frames = {}

        # Create all pages and store them
        for F in (StartPage, PasswordCreationPage, PasswordPage, BruteForcePage, StoredPasswords, DocumentationPage, HashPage, FinalPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        # if any password exists checker
        if page in [PasswordPage, BruteForcePage, HashPage, FinalPage]:
            if self.DB.access('passwords') == []:
                messagebox.showerror("Error", "Please create/generate a password before opening this page.")
            else:
                # final page has extra condition - must have at least one valid password to check
                if page == FinalPage:
                    if self.DB.access('valid') == []:
                        messagebox.showerror("Error",
                        "Please create a valid password (all prior modules completed) before opening this page.")
                    else:
                        frame.tkraise()
                else:
                    frame.tkraise()
        else:
            frame.tkraise()
        # create event for ensuring pages are updated
        frame.event_generate("<<ChangedFrame>>")
        
    # protocol for closing window and database
    def close(self):
        self.DB.close()
        self.destroy()

    # reset database
    def clear_passwords(self):
        self.DB.close()
        # re-call DB initializer
        self.DB = stored_passwords.DB()
#------------------------------------------------------------------------------------------#
# Front Page
class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)

        # Make layout responsive
        self.columnconfigure(0, weight=1)

        # Title
        title = ttk.Label(
            self,
            text="Password Security & Authentication Simulator",
            font=("Arial", 16, "bold")
        )
        title.grid(row=0, column=0, pady=10)

        # Image
        image = Image.open("../Resources/security_image.jpg")
        image = image.resize((300, 200))
        self.photo = ImageTk.PhotoImage(image)

        image_label = ttk.Label(self, image=self.photo)
        image_label.grid(row=1, column=0, pady=10)

        #button container
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, pady=10)

        # Configure columns inside button frame
        for i in range(2):
            button_frame.columnconfigure(i, weight=1)

        # Row 1 buttons
        ttk.Button(
            button_frame,
            text="Password Creation",
            command=lambda: controller.show_frame(PasswordCreationPage)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            button_frame,
            text="Password Security Check",
            command=lambda: controller.show_frame(PasswordPage)
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Row 2 buttons
        ttk.Button(
            button_frame,
            text="Brute Force Attack",
            command=lambda: controller.show_frame(BruteForcePage)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            button_frame,
            text="Hash Maker",
            command=lambda: controller.show_frame(HashPage)
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Row 3 buttons
        ttk.Button(
            button_frame,
            text="Stored Passwords",
            command=lambda: controller.show_frame(StoredPasswords)
        ).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(
            button_frame,
            text="Useful Information",
            command=lambda: controller.show_frame(DocumentationPage)
        ).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Final button full width
        ttk.Button(
            button_frame,
            text="Final",
            command=lambda: controller.show_frame(FinalPage)
        ).grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Quit button full width
        ttk.Button(
            button_frame,
            text="Quit",
            command=controller.destroy
        ).grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
#------------------------------------------------------------------------------------------#
# Password Creation Page
class PasswordCreationPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=100)
        self.show_password = BooleanVar(value=False)

        self.controller = controller
        self.pc = password_creation.PasswordCreation(controller.DB)

        title_font = ("Segoe UI", 18, "bold")
        section_font = ("Segoe UI", 10)

        # Allow frame to expand
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Password Creation", font=title_font).grid(row=0, column=0, pady=10)

        # Entry field for user password
        self.entry = ttk.Entry(self, show="*")
        self.entry.grid(row=2, column=0, pady=5)

        #allowes for user to choose between seeing password or keeping it hided as its typed in.
        ttk.Checkbutton(
            self,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password
        ).grid(row=3, column=0, pady=5)

        # Display Frame
        display_frame = ttk.Frame(self, borderwidth=2, relief="sunken")
        display_frame.grid(row=1, column=0, sticky="nsew", pady=10)

        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)

        #disables typing in display screen
        self.display = Text(display_frame, height=10,state="disabled")
        self.display.grid(row=0, column=0, sticky="nsew")

        # Buttons
        ttk.Button(self, text="Create own Password",
                   command=self.create_password).grid(row=4, column=0, pady=0)

        ttk.Button(self, text="Back to Home",
                   command=lambda: controller.show_frame(StartPage)).grid(row=5, column=0, pady=10)

        # sliders and generation
        generation_frame = ttk.Frame(self, borderwidth=2, relief="sunken")
        generation_frame.grid(row=4, column=1, pady=5)

        ttk.Button(generation_frame, text="Generate a Password",
                   command=self.generate_password).grid(row=0, column=0, pady=5)

        qtylabel = ttk.Label(generation_frame, text="Number of Passwords to Generate: 1")
        qtylabel.grid(row=1,column=0)
        self.qtytext = qtylabel

        qty = ttk.Scale(generation_frame, length=100, orient="horizontal", from_=1, to=50, command=self.upd_qty)
        qty.grid(row=2,column=0)
        self.qtynum = qty
        self.qty = 1

        lenlabel = ttk.Label(generation_frame, text="Length of Passwords to Generate: 12")
        lenlabel.grid(row=3,column=0)
        self.lentext = lenlabel

        lenn = ttk.Scale(generation_frame, length=100, orient="horizontal",from_=1,to=30, command=self.upd_len)
        lenn.grid(row=4,column=0)
        #lenn.set(12)
        self.test = lenn
        self.lenn = 12

    # slider update functions
    def upd_qty(self, e):
        self.qtytext.config(text=f'Number of Passwords to Generate: {int(self.qtynum.get())}')
        self.qty=int(self.qtynum.get())

    def upd_len(self, e):
        self.lentext.config(text=f'Length of Passwords to Generate: {int(self.test.get())}')
        self.lenn=int(self.test.get())

    #locks and unlocks display screen
    def write_output(self, text):
        self.display.config(state="normal")
        self.display.insert(END, text + "\n")
        self.display.config(state="disabled")
        self.display.see(END)

    #prints out the create password that the user inputted
    def create_password(self):
        password = self.entry.get()
        result = self.pc.user_create(password)
        self.write_output(result)

    #prints out generated password for user to see
    def generate_password(self):
        for i in range(self.qty):
            result = self.pc.generate(self.lenn)
            self.write_output(result)

    #shows/hides the password as its being entered
    def toggle_password(self):
        if self.show_password.get():
            self.entry.config(show="")
        else:
            self.entry.config(show="*")
#------------------------------------------------------------------------------------------#
# Password Strength Page
class PasswordPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)

        self.controller = controller
        self.evaluator = password_Strength.PasswordEvaluation(controller.DB)
        self.current = None

        # layout
        self.columnconfigure(0, weight=1)

        # Title
        ttk.Label(
            self,
            text="Password Security Check Page",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, pady=10)

        # splits frame
        main_frame = ttk.Frame(self)
        main_frame.grid(row=1, column=0)

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=0)

        # scroll bar ui
        selector_frame = ttk.Frame(main_frame)
        selector_frame.grid(row=0, column=0, sticky="n", padx=(10, 2), pady=10)

        ttk.Label(selector_frame, text="Available Passwords").grid(row=0, column=0)

        canvas_container = Frame(selector_frame, borderwidth=0, highlightthickness=0)
        canvas_container.grid(row=1, column=0)

        self.canvas = Canvas(canvas_container, width=220, height=180, highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        scrollbar = ttk.Scrollbar(
            canvas_container,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.selectframe = Frame(self.canvas, borderwidth=0, highlightthickness=0)
        self.canvas.create_window((0, 0), window=self.selectframe, anchor="nw")

        self.selectframe.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # initial load
        self.updateselect()
        self.bind("<<ChangedFrame>>", lambda e: self.updateselect())

        # display box
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=0, column=1, sticky="n", padx=(2, 10), pady=10)

        self.display = Text(display_frame, height=15, width=55, state="disabled")
        self.display.grid(row=0, column=0)

        # buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, pady=15)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        ttk.Button(
            button_frame,
            text="Evaluate Password",
            command=self.run_evaluation
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            button_frame,
            text="Back to Home",
            command=lambda: controller.show_frame(StartPage)
        ).grid(row=0, column=1, padx=10)

    # update list
    def updateselect(self):
        for widget in self.selectframe.winfo_children():
            widget.destroy()

        data = self.controller.DB.access('passwords')

        for i, password in enumerate(data):
            pwd = password[1]

            Button(
                self.selectframe,
                text=pwd,
                width=26,
                command=lambda p=pwd: self.selectpass(p)
            ).grid(row=i, column=0, pady=2)

        self.canvas.create_window((0, 0), window=self.selectframe, anchor="nw")

    # Password Selected
    def selectpass(self, password):
        self.current = password
        msg = self.evaluator.select(password)
        self.write_output(msg)

    # Evaluation
    def run_evaluation(self):
        if not self.current:
            self.write_output("Please select a password first.")
            return

        result = self.evaluator.evaluate()
        self.write_output(result)

    # Output
    def write_output(self, text):
        self.display.config(state="normal")
        self.display.insert(END, text + "\n")
        self.display.config(state="disabled")
        self.display.see(END)
#------------------------------------------------------------------------------------------#
# Brute Force Page
class BruteForcePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=100)
        # assign parent class for use in DB - may need to be used for other pages
        self.controller = controller

        #Import brute force class for database updating
        from brute_force_attack import BruteForce
        self.bruteforce = BruteForce(self.controller.DB)

        # Allow frame to expand
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Brute Force Attack Simulation Page").grid(row=0, column=0, sticky="n", pady=10,
                                                                        columnspan=5)
        # Display Frame
        display_frame = ttk.Frame(self, borderwidth=2, relief="sunken")
        display_frame.grid(row=1, column=1, sticky="nsew", pady=10)

        # Make display frame expandable
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)

        # Text widget
        self.display = Text(display_frame, height=10, state="disabled")
        self.display.grid(row=0, column=1, sticky="nsew")

        ##### reusable password selector module
        # currently selected password placeholder
        self.current = None

        # outer layer frame to contain both the scrollbar and the selection buttons
        superframe = Frame(self, width=250, height=200)
        superframe.grid(row=1, column=0)

        # build scrollbar canvas
        canvas = Canvas(superframe, width=200)
        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(superframe, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="nsew", rowspan=2)
        canvas.configure(yscrollcommand=scrollbar.set)

        # create frame for scrollbar and create scroll events
        selectionframe = Frame(canvas, width=200, height=200)
        canvas.create_window((0, 0), window=selectionframe, anchor="nw")
        selectionframe.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        selectionframe.grid(row=0, column=0, sticky="nsew")
        selectionframe.grid_propagate(False)
        Label(superframe, text="Available Passwords:").grid(row=0, column=0, sticky="nsew")

        # add canvas and selection frame to object to be called in selection updates
        self.canvas = canvas
        self.selectframe = selectionframe
        # initial update selection for first build
        self.updateselect('')
        # bind an event on password creation/generation to rerun this stage
        self.bind("<<ChangedFrame>>", lambda e: [self.updateselect(e)])

        # Buttons:
        ttk.Button(self, text="Start Attack",
                   command=self.start_attack).grid(row=2, column=0, pady=5)
        ttk.Button(self, text="Pause/Resume",
                   command=self.pause_attack).grid(row=3, column=0, pady=5)
        ttk.Button(self, text="End Attack",
                   command=self.end_attack).grid(row=4, column=0, pady=5)
        ttk.Button(self, text="Back to Home",
                   command=lambda: controller.show_frame(StartPage)).grid(row=3, column=1, pady=10)

    ##### end selector module

    # event-binded function to add a selector for each password made
    def updateselect(self, event):
        selectiter = 1
        # database access point
        data = self.controller.DB.access('passwords')
        for password in data:
            currentpass = password[1]
            selectorbutton = Button(self.selectframe, text=currentpass,
                                    command=lambda name=currentpass: self.selectpass(name))
            # making space for buttons
            selectorbutton.grid(row=selectiter, column=0, sticky="w")
            self.selectframe.grid(rowspan=selectiter)
            selectiter += 1
            self.canvas.create_window((0, selectiter), window=self.selectframe, anchor="nw")
            self.selectframe.configure(height=(40 * selectiter))

    # function to store selected password to object variable
    def selectpass(self, password):
        self.current = password
        ###
        self.display.config(state="normal")
        self.display.insert(END, f"\nSelected Password: {self.current}\n")
        self.display.config(state="disabled")
        self.display.see(END)
        ###
        ##### end selector module

    #Button functions, an output display, and a database updater.
    def start_attack(self):
        if self.bruteforce.counter == 1:
            charsets = {
                "Lowercase": string.ascii_lowercase,
                "Letters": string.ascii_letters,
                "Alphanumeric": string.ascii_letters + string.digits,
                "All (with symbols)": string.ascii_letters + string.digits + "!@#$%^&*"
            }
            selected_charset = None
            for name, charset in charsets.items():
                if all(c in charset for c in self.current):
                    selected_charset = charset
                    break
            self.display.config(state="normal")
            self.display.insert(END, f"Selected Charset: {selected_charset}\n")
            self.display.config(state="disabled")
            self.display.see(END)
            self.bruteforce.start_attack(self.current, selected_charset, self.write_output, self.db_update)
        else:
            messagebox.showerror("Error", "An attack is already running.")

    def pause_attack(self):
        if self.bruteforce.counter > 1:
            self.bruteforce.pause_attack(self.write_output)
        else:
            messagebox.showerror("Error", "No attack is currently running.")

    def end_attack(self):
        if self.bruteforce.counter > 1:
            self.bruteforce.end_attack(self.write_output)
        else:
            messagebox.showerror("Error", "No attack is currently running.")

    def write_output(self, text):
        self.display.config(state="normal")
        self.display.insert(END, text + "\n")
        self.display.config(state="disabled")
        self.display.see(END)

    def db_update(self, password, elapsed_time, num_attempts):
        self.after(0, lambda: self.controller.DB.passupdate(password, time=elapsed_time, attempts=num_attempts))

#------------------------------------------------------------------------------------------#
# Stored Passwords Page
class StoredPasswords(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=100)
        # assign parent class for use in DB - may need to be used for other pages
        self.controller = controller

        # Allow frame to expand
        self.columnconfigure(0, weight=1)
        
        # assign default validity
        self.showvalid = 0

        ttk.Label(self, text="Stored Passwords").grid(row=0, column=0, sticky="n", pady=10)

        # Display Frame
        display_frame = ttk.Frame(self, borderwidth=2, relief="sunken")
        display_frame.grid(row=1, column=0, sticky="nsew", pady=10)

        # Make display frame expandable
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)

        # Tree widget
        self.DBtree = ttk.Treeview(display_frame,
                              columns=("Key", "Password", "Brute Force Time",
                                       "Brute Force Attempts",
                                       "Quality", "Generated?", "Score"),
                              show="headings")
        # formatting
        self.DBtree.heading("Key", text="#")
        self.DBtree.heading("Password", text="Password Text")
        self.DBtree.heading("Brute Force Time", text="Brute Force Time")
        self.DBtree.heading("Brute Force Attempts", text="Brute Force Attempts")
        self.DBtree.heading("Quality", text="Quality Score")
        self.DBtree.heading("Generated?", text="Generated Password?")
        self.DBtree.heading("Score", text="Overall Score")
        self.DBtree.grid(row=0, column=0, sticky="nsew")
        # populate data using helper function
        self.updatetree('')
        self.bind("<<ChangedFrame>>", lambda e: [self.updatetree(e)])
        
        # valid checker button to filter stored passwords by completion
        switch = IntVar()
        ttk.Checkbutton(self, text="Show Only Valid Passwords", variable=switch,
                        onvalue=1, offvalue=0, command=lambda:self.validfilter(switch)).grid(row=2, column=0, pady=5)

        # Clear button to remove stored history
        ttk.Button(self, text="Clear Password History",
                   command=self.clear).grid(row=3, column=0, pady=5)

        ttk.Button(self, text="Back to Home",
                   command=lambda: controller.show_frame(StartPage)).grid(row=4, column=0, pady=10)

    # function to clear the stored data
    def clear(self):
        # call parent class to clear data
        self.controller.clear_passwords()
        self.updatetree('')

    # helper function to reset the tree
    def updatetree(self, event):
        ###
        print("Logs - Storage Tree updated.")
        ###
        # clear tree
        for item in self.DBtree.get_children():
            self.DBtree.delete(item)
        # check if results are filtering valid only
        if self.showvalid == 1:
            data = self.controller.DB.access('valid')
        else:
            # rebuild tree using data from passwords table
            data = self.controller.DB.access('passwords')
        for row in data:
            # edge case handling
            if row[2] == 0 or row[3] == 0:
                row = (row[0], row[1], "Incomplete", "Incomplete", row[4], row[5], "Incomplete")
            elif row[2] == 999999:
                row = (row[0], row[1], "Reached Time Limit", row[3], row[4], row[5], row[6])
            if row[4] == 0:
                row = (row[0], row[1], row[2], row[3], "Incomplete", row[5], "Incomplete")
            self.DBtree.insert("", END, values=row)
            
    # function for checker button to update validity filter
    def validfilter(self, switch):
        if switch.get() == 0:
            self.showvalid = 0
            self.updatetree('')
        elif switch.get() == 1:
            self.showvalid = 1
            self.updatetree('')
#------------------------------------------------------------------------------------------#
useful_information_text = """
PASSWORD SECURITY INFORMATION

1. What Makes a Strong Password
- At least 12 characters
- Mix of uppercase, lowercase, digits, and symbols
- Avoid dictionary words and personal info

2. Why Hashing Matters
- Passwords are never stored directly
- Hashing is one-way and irreversible
- Salting prevents identical hashes

3. Brute Force Risks
- Short passwords are cracked quickly
- Attackers can try billions of guesses per second

4. Best Practices
- Use a password manager
- Enable multi-factor authentication (MFA)
- Never reuse passwords
- Prefer adaptive hashing (bcrypt, Argon2)

5. Common Attacks
- Dictionary attacks
- Credential stuffing
- Rainbow tables (prevented by salting)
"""
#------------------------------------------------------------------------------------------#
#Documentation Page for usfel information
class DocumentationPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=100)
        self.controller = controller

        # Allow centering
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ttk.Label(
            self,
            text="Password & Security Information",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, pady=10, sticky="n")

        # Scrollable text area
        text_frame = ttk.Frame(self)
        text_frame.grid(row=1, column=0, pady=10)

        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.textbox = Text(text_frame, wrap="word", height=25, width=80, state="disabled")
        self.textbox.grid(row=0, column=0)

        scrollbar = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.textbox.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.textbox.configure(yscrollcommand=scrollbar.set)

        # Load content button
        ttk.Button(
            self,
            text="Display Information",
            command=self.load_info
        ).grid(row=2, column=0, pady=10)

        ttk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame(StartPage)
        ).grid(row=3, column=0, pady=10)

    def load_info(self):
        self.textbox.config(state="normal")
        self.textbox.delete("1.0", END)
        self.textbox.insert(END, useful_information_text)
        self.textbox.config(state="disabled")
        self.textbox.see(END)
#------------------------------------------------------------------------------------------#
# Hash Page
class HashPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)

        # assign parent class for use in DB - may need to be used for other pages
        self.controller = controller

        from hash_creation import HashCreation
        self.hash = HashCreation(self.controller.DB)

        ##### reusable password selector module
        # currently selected password placeholder
        self.current = None

        # layout
        self.columnconfigure(0, weight=1)

        # Title
        ttk.Label(
            self,
            text="Hash Creation Page",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, pady=10)

        # splits frame
        main_frame = ttk.Frame(self)
        main_frame.grid(row=1, column=0)

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=0)

        # scroll bar ui
        selector_frame = ttk.Frame(main_frame)
        selector_frame.grid(row=0, column=0, sticky="n", padx=(10, 2), pady=10)

        ttk.Label(selector_frame, text="Available Passwords").grid(row=0, column=0)

        canvas_container = Frame(selector_frame, borderwidth=0, highlightthickness=0)
        canvas_container.grid(row=1, column=0)

        self.canvas = Canvas(canvas_container, width=220, height=180, highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        scrollbar = ttk.Scrollbar(
            canvas_container,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.selectframe = Frame(self.canvas, borderwidth=0, highlightthickness=0)
        self.canvas.create_window((0, 0), window=self.selectframe, anchor="nw")

        self.selectframe.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # initial update selection for first build
        self.updateselect()
        # bind an event on password creation/generation to rerun this stage
        self.bind("<<ChangedFrame>>", lambda e: self.updateselect())

        # Display Frame
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=0, column=1, sticky="n", padx=(2, 10), pady=10)

        # Text widget
        self.display = Text(display_frame, height=15, width=55, state="disabled")
        self.display.grid(row=0, column=0)

        # buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, pady=15)

        ttk.Button(
            button_frame,
            text="SHA256",
            command=self.hashsha256
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="BLAKE2B",
            command=self.hashblake2b
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            button_frame,
            text="MD5",
            command=self.hashmd5
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            button_frame,
            text="Back to Home",
            command=lambda: controller.show_frame(StartPage)
        ).grid(row=1, column=0, columnspan=3, pady=10)

        # Tree widget
        self.DBtree = ttk.Treeview(self,
                                   columns=("Key", "Hash Type", "Hash Text"),
                                   show="headings")
        # formatting
        self.DBtree.heading("Key", text="Password #")
        self.DBtree.heading("Hash Type", text="Hash Type")
        self.DBtree.heading("Hash Text", text="Hash Text")
        self.DBtree.grid(row=1, column=2, sticky="nsew")
        # populate data using helper function
        self.updatetree()

    # helper function to reset the tree
    def updatetree(self):
        ###
        print("Logs - Hashes Tree updated.")
        ###
        # clear tree
        for item in self.DBtree.get_children():
            self.DBtree.delete(item)
        # rebuild tree using data from hashes table
        data = self.controller.DB.access('hashes')
        for row in data:
            if row[1] == 0:
                type='SHA256'
            elif row[1] == 1:
                type='BLAKE2B'
            elif row[1] == 2:
                type='MD5'
            row = (row[0],type,row[2])
            self.DBtree.insert("", END, values=row)

    # event-binded function to add a selector for each password made
    def updateselect(self):
        for widget in self.selectframe.winfo_children():
            widget.destroy()

        # database access point
        data = self.controller.DB.access('passwords')

        for i, password in enumerate(data):
            currentpass = password[1]

            Button(
                self.selectframe,
                text=currentpass,
                width=26,
                command=lambda name=currentpass: self.selectpass(name)
            ).grid(row=i, column=0, pady=2)

        self.canvas.create_window((0, 0), window=self.selectframe, anchor="nw")

    # function to store selected password to object variable
    def selectpass(self, password):
        self.current = password
        ###
        self.display.config(state="normal")
        self.display.insert(END, f"\nSelected Password: {self.current}\n\n")
        self.display.config(state="disabled")
        self.display.see(END)
        ###

    ##### end selector module

    def hashsha256(self):
        self.hash.create_hash_sha256(self.current, self.write_output, self.db_update_sha256)

    def hashblake2b(self):
        self.hash.create_hash_blake2b(self.current, self.write_output, self.db_update_blake2b)

    def hashmd5(self):
        self.hash.create_hash_md5(self.current, self.write_output, self.db_update_md5)

    def write_output(self, text):
        self.display.config(state="normal")
        self.display.insert(END, text + "\n")
        self.display.config(state="disabled")
        self.display.see(END)

    def db_update_sha256(self, password, sha256_hash):
        self.after(0, lambda: [self.controller.DB.input_hash(password, 0, sha256_hash), self.updatetree()])

    def db_update_blake2b(self, password, blake2b_hash):
        self.after(0, lambda: [self.controller.DB.input_hash(password, 1, blake2b_hash), self.updatetree()])

    def db_update_md5(self, password, md5_hash):
        self.after(0, lambda: [self.controller.DB.input_hash(password, 2, md5_hash), self.updatetree()])
# ------------------------------------------------------------------------------------------#
# Visualization Page
class FinalPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=15)

        self.controller = controller
        self.current = None

        # ---------------- GRID ----------------
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # ---------------- TITLE ----------------
        ttk.Label(
            self,
            text="Final Security Dashboard",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=10)

        # =====================================================
        # TOP LEFT - PASSWORD SELECTOR
        # =====================================================
        selector_frame = ttk.Frame(self)
        selector_frame.grid(row=1, column=0, sticky="nsew")

        ttk.Label(selector_frame, text="Passwords").grid(row=0, column=0)

        canvas_container = Frame(selector_frame)
        canvas_container.grid(row=1, column=0)

        self.canvas = Canvas(canvas_container, width=220, height=200)
        self.canvas.grid(row=0, column=0)

        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.selectframe = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.selectframe, anchor="nw")

        self.selectframe.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.bind("<<ChangedFrame>>", lambda e: self.updateselect())
        self.updateselect()

        # =====================================================
        # TOP MIDDLE - SCORE
        # =====================================================
        self.score_label = ttk.Label(
            self,
            text="Total Score: N/A",
            font=("Segoe UI", 14, "bold")
        )
        self.score_label.grid(row=1, column=1)

        # =====================================================
        # TOP RIGHT - HASH TABLE (FIXED REUSE STYLE)
        # =====================================================
        hash_frame = ttk.Frame(self)
        hash_frame.grid(row=1, column=2, sticky="nsew")

        ttk.Label(hash_frame, text="Hash Table").grid(row=0, column=0)

        self.hash_tree = ttk.Treeview(
            hash_frame,
            columns=("Key", "Type", "Hash"),
            show="headings",
            height=8
        )

        self.hash_tree.heading("Key", text="Password #")
        self.hash_tree.heading("Type", text="Hash Type")
        self.hash_tree.heading("Hash", text="Hash Text")
        self.hash_tree.grid(row=1, column=0, sticky="nsew")

        # =====================================================
        # BOTTOM LEFT - SCATTER PLOT
        # =====================================================
        self.scatter_frame = ttk.Frame(self)
        self.scatter_frame.grid(row=2, column=0, sticky="nsew")

        self.fig1 = Figure(figsize=(3, 3))
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Attempts")
        self.ax1.set_title("Brute Force Result")

        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.scatter_frame)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack()

        # =====================================================
        # BOTTOM MIDDLE - BREAKDOWN
        # =====================================================
        self.breakdown = Text(self, height=10, width=40)
        self.breakdown.grid(row=2, column=1)
        self.breakdown.config(state="disabled")

        # =====================================================
        # BOTTOM RIGHT - PIE CHART
        # =====================================================
        self.pie_frame = ttk.Frame(self)
        self.pie_frame.grid(row=2, column=2, sticky="nsew")

        # =====================================================
        # BOTTOM CENTER - BACK TO HOME BUTTON
        # =====================================================
        ttk.Button(self, text="Back to Home",
                   command=lambda: controller.show_frame(StartPage)).grid(row=3, column=1, pady=2)

    # =====================================================
    # PASSWORD SELECTOR
    # =====================================================
    def updateselect(self):
        for w in self.selectframe.winfo_children():
            w.destroy()

        data = self.controller.DB.access('valid')

        for i, row in enumerate(data):
            pwd = row[1]

            Button(
                self.selectframe,
                text=pwd,
                width=25,
                command=lambda p=pwd: self.selectpass(p)
            ).grid(row=i, column=0, pady=2)

        self.canvas.create_window((0, 0), window=self.selectframe, anchor="nw")

    def selectpass(self, password):
        self.current = password

        self.update_hashes()
        self.update_score()
        self.update_breakdown()
        self.update_graphs()

    # =====================================================
    # HASH TABLE (FIXED - MATCHES HASH PAGE LOGIC)
    # =====================================================
    def update_hashes(self):
        for item in self.hash_tree.get_children():
            self.hash_tree.delete(item)

        if not self.current:
            return

        data = self.controller.DB.hashfinder(self.current)

        for row in data:
            key, htype, htext = row

            if htype == 0:
                htype = "SHA256"
            elif htype == 1:
                htype = "BLAKE2B"
            elif htype == 2:
                htype = "MD5"

            self.hash_tree.insert("", END, values=(key, htype, htext))

    # =====================================================
    # SCORE (FIXED SAFE LOOKUP)
    # =====================================================
    def update_score(self):
        data = self.controller.DB.access('passwords')

        for row in data:
            if row[1] == self.current:
                brute_time = row[2]
                attempts = row[3]
                quality = row[4]
                score = row[6]

                self.score_label.config(text=f"Total Score: {score:.2f}/100")

                self.current_score = score
                self.brute_time = brute_time
                self.attempts = attempts
                self.quality = quality
                return

    # =====================================================
    # BREAKDOWN
    # =====================================================
    def update_breakdown(self):
        self.breakdown.config(state="normal")
        self.breakdown.delete("1.0", END)

        self.breakdown.insert(END,
f"""Score Breakdown

Quality: {self.quality}
Brute Force Time: {self.brute_time:.2f}
Attempts: {self.attempts}

Formula:
(50 * Quality/10) + (50 * Time/350)
""")

        self.breakdown.config(state="disabled")

    # =====================================================
    # GRAPHS (REAL MATPLOTLIB EMBEDDING FIX)
    # =====================================================
    def update_graphs(self):
        for w in self.pie_frame.winfo_children():
            w.destroy()

        # ---- scatter plot ----
        self.ax1.scatter(self.brute_time, self.attempts)
        self.canvas1.draw()

        # ---- pie chart ----
        # brute force time is capped at 300 because of the 5 minute cap
        if self.brute_time <= 350:
            bfscore = self.brute_time / 350
        elif self.brute_time >= 999999:
            bfscore = 1

        fig2 = Figure(figsize=(3, 3))
        ax2 = fig2.add_subplot(111)

        labels = ["Quality", "Brute Force"]
        values = [(50*self.quality/10), (50*bfscore)]

        ax2.pie(values, labels=labels, autopct="%1.1f%%")
        ax2.set_title("Score Influence")

        canvas2 = FigureCanvasTkAgg(fig2, master=self.pie_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack()
# ------------------------------------------------------------------------------------------#
# Run the app
app = App()
app.mainloop()