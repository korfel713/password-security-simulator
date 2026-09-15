# Password Security Authentication Simulator (P.A.S.S.)

P.A.S.S. is a Python desktop application for exploring password-security concepts through an interactive GUI. The project includes password creation, strength evaluation, hashing, brute-force simulation, temporary password storage, and result visualization.

This repository is my personal portfolio version of a team project originally developed at Florida Polytechnic University. The original shared repository remains unchanged.

## Features

- Create custom passwords or generate randomized passwords
- Evaluate password strength using length and character-composition checks
- Demonstrate common hashing algorithms
- Simulate password attacks using a wordlist and character-based brute force
- Store session data in an in-memory SQLite database
- Visualize brute-force and evaluation results through Matplotlib
- Navigate the application through a Tkinter / ttkbootstrap interface

## Technologies

- Python
- Tkinter / ttkbootstrap
- SQLite
- Matplotlib
- Pillow
- hashlib
- Threading

## Running the Project

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

Then run the application from the code directory:

```bash
cd "Code Files"
python Gui.py
```

The original team project used a large password wordlist containing more than two million entries. To keep this portfolio repository lightweight, this version includes a small sample wordlist. If the original `Resources/2151220-passwords.txt` file is added locally, the application will automatically use it instead.

## Project Structure

```text
Code Files/
    Gui.py
    password_creation.py
    password_Strength.py
    brute_force_attack.py
    hash_creation.py
    stored_passwords.py
    Final_Visual.py
Resources/
    security_image.jpg
    common-passwords-sample.txt
requirements.txt
```

## Team Project

Original team members:

- Sean Thompson
- TJ Inman
- Darian Hendry
- Aurora Lipps
- Jayden Lopez

Original shared repository:

https://github.com/korfel713/Password-Authentication-Security-Simulator-P.A.S.S-

This portfolio repository is intended to present the project more clearly for recruiting and portfolio purposes. It does not represent the project as solo work.

## Portfolio Notes

The portfolio copy removes IDE metadata and Python cache files from the original repository and adds clearer setup documentation. The core project source remains based on the team's application.
