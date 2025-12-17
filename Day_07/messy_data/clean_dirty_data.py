import pandas as pd

class DataCleaner:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)

    def clean(self):
        # 1. Strip spaces from column names
        self.df.columns = self.df.columns.str.strip()

        # 2. Strip spaces inside string cells
        self.df = self.df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # 3. Normalize text formats
        text_cols = ["Name", "Department", "City"]
        for col in text_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].str.title()

        # 4. Convert datatypes
        self.df["Salary"] = pd.to_numeric(self.df["Salary"], errors="coerce")
        self.df["Age"] = pd.to_numeric(self.df["Age"], errors="coerce")
        self.df["JoinDate"] = pd.to_datetime(self.df["JoinDate"], errors="coerce")

        # 5. Handle missing values
        self.df.fillna({
            "City": "Unknown",
            "Department": "Unknown",
            "Salary": self.df["Salary"].median(),
            "Age": self.df["Age"].median()
        }, inplace=True)

        # 6. Remove duplicates
        self.df.drop_duplicates(inplace=True)

        return self

    def export(self, outfile="cleaned_employees.csv"):
        self.df.to_csv(outfile, index=False)
        return self


if __name__ == "__main__":
    DataCleaner("employees_dirty.csv").clean().export()
