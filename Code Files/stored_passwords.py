import sqlite3

### logging print statements stored in between triple hashes,
# they are temporary and can be removed

## Database class, creates a local database and provides key functions
# functions: access, input_pass, input_hash, keyfinder, passupdate, close
#
class DB():
    def __init__(self):
        # global connection as the DB is temporary and must persist until destroyed
        global connection
        connection = sqlite3.connect(":memory:")
        print(f'Logs - DB Connection established.')
        # build DB schema
        cursor = connection.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS passwords (
                pass_key INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                pass_text TEXT NOT NULL UNIQUE,
                bruteforce_time REAL NOT NULL,
                bruteforce_attempts INTEGER NOT NULL,
                quality_score INTEGER NOT NULL,
                if_generated INTEGER NOT NULL,
                overall_score REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS hashes (
                pass_key INTEGER NOT NULL,
                hash_type INTEGER NOT NULL,
                hash_text TEXT NOT NULL,
                UNIQUE(pass_key, hash_type),
                PRIMARY KEY (pass_key, hash_type)
            );
        ''')

    # function for accessing the database
    # type - quick access for specific queries, may be passwords, valid, hashes, or custom
    # custom - custom query string for related type
    def access(self, type, custom=""):
        # connecting cursor to the DB to execute queries
        cursor = connection.cursor()
        # type cases
        if type == 'passwords':
            ###
            print(f"Logs - Password table selection query ran.")
            ###
            cursor.execute('''SELECT * FROM passwords;''')
        elif type == 'valid':
            ###
            print(f"Logs - Valid password table selection query ran.")
            ###
            cursor.execute('''SELECT * FROM passwords WHERE 
                    bruteforce_time > 0 AND 
                    bruteforce_attempts > 0 AND
                    quality_score > 0 AND
                    overall_score > 0;''')
        elif type == 'hashes':
            ###
            print(f"Logs - Hashes table selection query ran.")
            ###
            cursor.execute('''SELECT * FROM hashes ORDER BY pass_key, hash_type;''')
        elif type == 'custom':
            # error handling for custom queries
            try:
                ###
                print(f"Logs - Custom query to run: {custom}")
                ###
                cursor.execute(custom)
            except:
                print('Invalid Custom Query.')
                return 1
        else:
            # if function was called with incorrect type
            print('Invalid DB Access Type.')
            return 1
        # return query results
        return cursor.fetchall()

    # function for inserting into passwords table
    # takes all variables used for one row insertion
    # MUST prefix text string with r'' to input sanitize
    # allows for temporary table insertion using only password text and ifgenerated
    def input_pass(self, text, ifgen, time=0, attempts=0, qual=0, score=0):
        # connecting cursor to the DB to execute queries
        cursor = connection.cursor()
        # query creation
        query = (f"INSERT INTO passwords "
                 f"(pass_text, bruteforce_time, bruteforce_attempts, quality_score, if_generated, overall_score) "
                 f"VALUES ('{text}', {time}, {attempts}, {qual}, {ifgen}, {score})")
        ###
        print(f"Logs - Password table insertion query to run: {query}")
        ###
        # attempt to run query
        try:
            cursor.execute(query)
            return f"Password Saved: {text}"
        except:
            print(f"Logs - Password '{text}' already exists")
            return f"Error: Password already exists."

    # function for inserting into hashes table
    # takes variables used for one row insertion
    # example call: input_hash(r'originaltext', 2, 'hashedtext')
    # in this case, we use an integer as a semantic notation for a hash type
    # ex. 2 = SHA256
    # takes password text to pull the associated key
    def input_hash(self, passtext, type, hashtext):
        # connecting cursor to the DB to execute queries
        cursor = connection.cursor()
        # find pass key using helper function
        passkey = self.keyfinder(passtext)
        if passkey == -1:
            return -1
        # query creation
        query = f"INSERT INTO hashes VALUES ({passkey}, {type}, '{hashtext}')"
        ###
        print(f"Logs - Hashes table insertion query to run: {query}")
        ###
        # attempt to run query
        try:
            cursor.execute(query)
            return f"Hash '{hashtext}' Saved for Password '{passtext}'"
        except:
            print(f"Logs - Hash '{hashtext}' for '{passtext}' already exists")
            return f"Error: Password already exists."

    # helper function to return the key number for a specific password
    # by passing password as string
    def keyfinder(self, passtext):
        # connecting cursor to the DB to execute queries
        cursor = connection.cursor()
        # query creation
        query = f"SELECT pass_key FROM passwords WHERE pass_text = '{passtext}';"
        ###
        print(f"Logs - Keyfinder query to run: {query}")
        ###
        # query execution and result casting
        cursor.execute(query)
        res = cursor.fetchall()
        # case handling for invalid password search
        if res == []:
            print('No matching password stored.')
            return -1
        return res[0][0]

    # function for finishing unfinished data entries in passwords table
    # can be used one temporary value at a time
    # input parameters example: passupdate(passtext, qual=3)
    def passupdate(self, passtext, time=0, attempts=0, qual=0, score=0):
        # connecting cursor to the DB to execute queries
        cursor = connection.cursor()
        # find pass key using helper function
        passkey = self.keyfinder(passtext)
        if passkey == -1:
            return -1
        # determine whether original values exist and replace undetermined variables
        if time == 0:
            query = f"SELECT bruteforce_time FROM passwords WHERE pass_text = '{passtext}';"
            cursor.execute(query)
            time = cursor.fetchall()[0][0]
        if attempts == 0:
            query = f"SELECT bruteforce_attempts FROM passwords WHERE pass_text = '{passtext}';"
            cursor.execute(query)
            attempts = cursor.fetchall()[0][0]
        if qual == 0:
            query = f"SELECT quality_score FROM passwords WHERE pass_text = '{passtext}';"
            cursor.execute(query)
            qual = cursor.fetchall()[0][0]
        if score == 0:
            query = f"SELECT overall_score FROM passwords WHERE pass_text = '{passtext}';"
            cursor.execute(query)
            score = cursor.fetchall()[0][0]

        # final score formula
        if time != 0 and attempts != 0 and qual != 0:
            if time <= 350:
                bfscore = time/350
            elif time >= 999999:
                bfscore = 1
            score = (50*(qual/10)) + (50*bfscore)
            print(f'Logs - Calculated final score: {score}')

        # create final update query
        query = (f"UPDATE passwords SET bruteforce_time = {time}, "
                 f"bruteforce_attempts = {attempts}, "
                 f"quality_score = {qual}, "
                 f"overall_score = {score} "
                 f"WHERE pass_key == '{passkey}';")
        ###
        print(f"Logs - Updater query to run: {query}")
        ###
        cursor.execute(query)

    def hashfinder(self, passtext):
        # connecting cursor to the DB to execute queries
        cursor = connection.cursor()
        # find pass key using helper function
        passkey = self.keyfinder(passtext)
        if passkey == -1:
            return -1
        # create hashfinder query
        query = (f"SELECT * FROM hashes WHERE pass_key = '{passkey}';")
        ###
        print(f"Logs - Hashfinder query to run: {query}")
        ###
        cursor.execute(query)
        # return results
        return cursor.fetchall()

    # cleanup function to ensure temporary database is deleted on application close
    def close(self):
        ###
        print(f"Logs - Cleaning temporary database.")
        ###
        connection.close()