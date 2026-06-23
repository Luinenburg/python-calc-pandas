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
    def __init__(self, config: user_config):
        self.config = config
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
        df.to_csv(self.config.name + "_history.csv", index=False)

    def save_config_to_csv(self):
        config_data = {
            "History Size": [self.config.history_size],
            "User Name": [self.config.name]
        }
        config_df = pd.DataFrame(config_data)
        config_df.to_csv(self.config.name + "_config.csv", index=False)