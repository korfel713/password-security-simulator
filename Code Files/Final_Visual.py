import matplotlib.pyplot as plt


class FinalVisual:
    def __init__(self, DB):
        self.DB = DB

    # -------------------------------------------------
    # GET SELECTED PASSWORD (LATEST ENTRY SAFE DEFAULT)
    # -------------------------------------------------
    def get_current_password(self):
        data = self.DB.access("passwords")
        if not data:
            return None
        return data[-1][1]  # last inserted password

    # -------------------------------------------------
    # FULL PASSWORD ROW
    # -------------------------------------------------
    def get_password_row(self, password):
        data = self.DB.access(
            "custom",
            f"SELECT * FROM passwords WHERE pass_text = '{password}'"
        )
        return data[0] if data else None

    # -------------------------------------------------
    # HASH DATA
    # -------------------------------------------------
    def get_hashes(self, password):
        passkey = self.DB.keyfinder(password)
        return self.DB.access(
            "custom",
            f"SELECT * FROM hashes WHERE pass_key = {passkey}"
        )

    # -------------------------------------------------
    # OVERALL SCORE
    # -------------------------------------------------
    def overall_score(self, brute_attempts, quality):
        # normalize brute force impact (simple scaling)
        brute_score = min(brute_attempts / 10000, 10)
        return round((brute_score * 0.5) + (quality * 0.5), 2)

    # -------------------------------------------------
    # BRUTE FORCE SCATTER DATA
    # -------------------------------------------------
    def brute_force_graph(self, attempts, time_value):
        x = list(range(1, int(time_value) + 1))
        if not x:
            return [], []

        y = []
        step = max(attempts / len(x), 1)

        for i in range(len(x)):
            y.append(step * (i + 1))

        return x, y

    def create_bruteforce_plot(self, password):
        row = self.get_password_row(password)
        if not row:
            return None, (0, 0)

        time_value = row[2]
        attempts = row[3]

        x, y = self.brute_force_graph(attempts, time_value)

        fig, ax = plt.subplots()
        ax.scatter(x, y)
        ax.set_title("Brute Force Simulation")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Attempts")

        return fig, (x, y[-1] if y else 0)

    # -------------------------------------------------
    # PIE CHART
    # -------------------------------------------------
    def create_pie(self, brute_score, eval_score):
        fig, ax = plt.subplots()

        ax.pie(
            [brute_score, eval_score],
            labels=["Brute Force", "Evaluation"],
            autopct="%1.1f%%"
        )

        ax.set_title("Score Influence")

        return fig