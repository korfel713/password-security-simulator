import string
import hashlib


class HashCreation:
    def __init__(self, DB):
        self.DB = DB
        self.sha256_hash = ""
        self.blake2b_hash = ""
        self.md5_hash = ""



    def create_hash_sha256(self, password, output, db_update):
        if not password:
            output("Error: No password entered.")
            return
        self.sha256_hash = hashlib.sha256(password.encode()).hexdigest()
        output(f"sha256 hash: {self.sha256_hash}\n")
        db_update(password,self.sha256_hash)



    def create_hash_blake2b(self, password, output, db_update):
        if not password:
            output("Error: No password entered.")
            return
        self.blake2b_hash = hashlib.blake2b(password.encode()).hexdigest()
        output(f"blake2b hash: {self.blake2b_hash}\n")
        db_update(password,self.blake2b_hash)


    def create_hash_md5(self, password, output, db_update):
        if not password:
            output("Error: No password entered.")
            return
        self.md5_hash = hashlib.md5(password.encode()).hexdigest()
        output(f"md5 hash: {self.md5_hash}\n")
        db_update(password,self.md5_hash)


