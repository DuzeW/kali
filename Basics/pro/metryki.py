import csv
import pandas as pd
from datetime import datetime
import os

class MetricsLogger:
    def __init__(self, file_name="metrics.csv", excel_name="metrics.xlsx"):
        self.file_name = file_name
        self.excel_name = excel_name
        self.columns = [
            "Task", "Agent", "Model", "Response Time (s)",
            "Success", "Response Size (tokens)", "Error Count", "Details"
        ]
        self._initialize_file()

    def _initialize_file(self):
        try:
            with open(self.file_name, mode="x", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.columns)
        except FileExistsError:
            pass

    def log(self, task, agent, model, response_time, success, response_size, error_count, details):
        row = [
            task, agent, model, response_time, success,
            response_size, error_count, details
        ]
        # Append to CSV
        with open(self.file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
        self._update_excel()

    def _update_excel(self):
        try:
            df = pd.read_csv(self.file_name)
            df.to_excel(self.excel_name, index=False)
        except Exception as e:
            print(f"Error updating Excel file: {e}")