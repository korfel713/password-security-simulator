#tests password security
class PasswordEvaluation:
    def __init__(self, DB):
        self.DB = DB
        self.current_password = None

    def select(self, password):
        self.current_password = password
        return f"Selected password: {password}"

    def evaluate(self):
        if not self.current_password:
            return "Error: No password selected."

        password = self.current_password

        #quality score calcualtor
        quality = 0
        feedback = []

        if len(password) >= 12:
            quality += 3
        elif len(password) >= 8:
            quality += 2
        else:
            quality += 1
            feedback.append("Increase password length (12+ recommended).")

        if any(c.islower() for c in password):
            quality += 1
        else:
            feedback.append("Add lowercase letters.")

        if any(c.isupper() for c in password):
            quality += 2
        else:
            feedback.append("Add uppercase letters.")

        if any(c.isdigit() for c in password):
            quality += 2
        else:
            feedback.append("Add numbers.")

        if any(not c.isalnum() for c in password):
            quality += 2
        else:
            feedback.append("Add special characters.")

        # penalties
        common = ["password", "123456", "qwerty", "admin"]
        if password.lower() in common:
            # 4/21 - quality cannot be set to zero, as it is used for other logic, so forced to zero
            quality = 1
            feedback.append("This is a very common password.")

        quality = min(quality, 10)



        # store into database
        try:
            self.DB.passupdate(
                password,
                qual=quality
            )
        except:
            return "Error: Could not update database entry."

        #evalualtion output
        result = f"""
Password Evaluation Results
----------------------------
Password: {password}

Quality Score: {quality}/10

"""

        if feedback:
            result += "\nSuggestions:\n- " + "\n- ".join(feedback)

        return result.strip()