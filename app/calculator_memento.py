import pandas as pd

class history_entry:
    def __init__(self, equation, result):
        self.equation = equation
        self.result = result

class user_config:
    def __init__(self, history_size=10, name="User"):
        self.history_size = history_size
        self.name = name

class data_handler:
    def __init__(self, username):
        self.username = username
        self.config = None
        self.history = []
    
    def load_config_from_csv(self):
        try:
            config_df = pd.read_csv("configs/" + self.username + "_config.csv")
            self.config = user_config(
                history_size=int(config_df["History Size"].iloc[0]),
                name=config_df["User Name"].iloc[0]
            )
        except FileNotFoundError:
            self.config = user_config(10, self.username)
    
    def load_history_from_csv(self):
        try:
            history_df = pd.read_csv("history/" + self.username + "_history.csv")
            self.history = [
                history_entry(equation, result)
                for equation, result in zip(history_df["Equation"], history_df["Result"])
            ]
        except FileNotFoundError:
            self.history = []

    def add_history_entry(self, equation, result):
        if len(self.history) >= self.config.history_size:
            self.history.pop(0)
        self.history.append(history_entry(equation, result))

    def get_history_dataframe(self):
        data = {
            "Equation": [entry.equation for entry in self.history],
            "Result": [entry.result for entry in self.history]
        }
        return pd.DataFrame(data)

    def save_history_to_csv(self):
        df = self.get_history_dataframe()
        df.to_csv("history/" + self.config.name + "_history.csv", index=False)

    def save_config_to_csv(self):
        config_data = {
            "History Size": [self.config.history_size],
            "User Name": [self.config.name]
        }
        config_df = pd.DataFrame(config_data)
        config_df.to_csv("configs/" + self.config.name + "_config.csv", index=False)