import pandas as pd
from datetime import datetime

class DataPipeline:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)

    # 1. Clean Data
    def clean(self):
        self.df.columns = self.df.columns.str.strip()
        self.df.drop_duplicates(inplace=True)
        self.df.fillna({"Department": "Unknown"}, inplace=True)
        self.df["Salary"] = pd.to_numeric(self.df["Salary"], errors="coerce")
        self.df["JoinDate"] = pd.to_datetime(self.df["JoinDate"], errors="coerce")
        return self

    # 2. Validate Data
    def validate(self):
        today = datetime.today()
        invalid = self.df[
            (self.df["Age"] < 18) | (self.df["Age"] > 60) |
            (self.df["Salary"] <= 0) |
            (self.df["JoinDate"].isna()) |
            (self.df["JoinDate"] > today)
        ]
        self.df = self.df.drop(invalid.index)
        self.invalid = invalid
        return self

    # 3. Transform Data
    def transform(self):
        self.df["TotalBonus"] = self.df["Salary"] * 0.10
        self.df["AgeGroup"] = pd.cut(
            self.df["Age"],
            bins=[0, 25, 45, 100],
            labels=["Young", "Adult", "Senior"]
        )
        return self

    # 4. Aggregate
    def aggregate(self):
        self.summary = self.df.groupby("Department").agg(
            avg_salary=("Salary", "mean"),
            total_bonus=("TotalBonus", "sum"),
            emp_count=("Name", "count")
        ).reset_index()
        return self

    # 5. Export
    def export(self, outfolder="outputs"):
        self.df.to_csv(f"{outfolder}/valid.csv", index=False)
        self.invalid.to_csv(f"{outfolder}/invalid.csv", index=False)
        self.summary.to_csv(f"{outfolder}/summaries.csv", index=False)
        return self

if __name__ == "__main__":
    DataPipeline("employees.csv") \
        .clean() \
        .validate() \
        .transform() \
        .aggregate() \
        .export()
