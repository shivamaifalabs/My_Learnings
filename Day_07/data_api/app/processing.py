import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ---------- Data Cleaner ----------
class DataCleaner:
    def __init__(self, filepath: str | None = None):
        self.df: pd.DataFrame = pd.DataFrame()
        if filepath:
            self.df = pd.read_csv(filepath)

    def load_df(self, df: pd.DataFrame):
        self.df = df
        return self

    def clean(self):
        if self.df.empty:
            return self

        # 1) Strip spaces from column names
        self.df.columns = self.df.columns.str.strip()

        # 2) Strip spaces inside values
        self.df = self.df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # **3) Replace dirty tokens to real NaN FIRST**
        missing_tokens = ["", " ", "  ", "none", "None", "NONE", "nan", "NaN", "NAN"]
        for col in ["Name", "Department", "City", "AgeGroup"]:
            if col in self.df.columns:
                self.df[col].replace(missing_tokens, pd.NA, inplace=True)

        # **4) Fill NaN values**
        if "City" in self.df.columns:
            self.df["City"].fillna("Unknown", inplace=True)
        if "Department" in self.df.columns:
            self.df["Department"].fillna("Unknown", inplace=True)
        if "AgeGroup" in self.df.columns:
            self.df["AgeGroup"].fillna("Unknown", inplace=True)
        if "Name" in self.df.columns:
            self.df["Name"].fillna("Unknown", inplace=True)

        # **5) Normalize case only AFTER missing values are fixed**
        for col in ["Name", "Department", "City", "AgeGroup"]:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.title()

        # 6) Remove duplicates
        self.df.drop_duplicates(inplace=True)

        return self



# ---------- Report Builder ----------
class ReportBuilder:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.reports: dict[str, pd.DataFrame] = {}

    def department_report(self):
        if "Department" in self.df.columns:
            report = self.df.groupby("Department").agg(
                emp_count=("Name", "count")
            ).reset_index()
            self.reports["department_report.csv"] = report
        return self

    def city_report(self):
        if "City" in self.df.columns:
            report = self.df.groupby("City").agg(
                emp_count=("Name", "count")
            ).reset_index()
            self.reports["city_report.csv"] = report
        return self

    def age_group_report(self):
        if "AgeGroup" in self.df.columns:
            report = self.df.groupby("AgeGroup").agg(
                emp_count=("Name", "count")
            ).reset_index()
            self.reports["age_group_report.csv"] = report
        return self

    def export(self, folder: str):
        os.makedirs(folder, exist_ok=True)
        for filename, df in self.reports.items():
            df.to_csv(os.path.join(folder, filename), index=False)
        return self


# ---------- Visualizer ----------
class Visualizer:
    def __init__(self, df: pd.DataFrame, out_folder: str):
        self.df = df
        self.out_folder = out_folder
        os.makedirs(out_folder, exist_ok=True)

    def employees_by_city(self):
        if "City" not in self.df.columns:
            return self
        plt.figure(figsize=(7, 7))
        self.df["City"].value_counts().plot(kind="pie", autopct="%1.1f%%")
        plt.title("Employees by City")
        plt.savefig(os.path.join(self.out_folder, "employees_by_city.png"), dpi=300)
        plt.close()
        return self

    def employees_by_department(self):
        if "Department" not in self.df.columns:
            return self
        plt.figure(figsize=(8, 5))
        self.df["Department"].value_counts().plot(kind="bar")
        plt.title("Employee Count by Department")
        plt.savefig(os.path.join(self.out_folder, "employees_by_department.png"), dpi=300)
        plt.close()
        return self

    def employees_by_agegroup(self):
        if "AgeGroup" not in self.df.columns:
            return self
        plt.figure(figsize=(8, 5))
        self.df["AgeGroup"].value_counts().plot(kind="bar")
        plt.title("Employee Count by AgeGroup")
        plt.savefig(os.path.join(self.out_folder, "employees_by_agegroup.png"), dpi=300)
        plt.close()
        return self

    def build_all(self):
        return (
            self.employees_by_city()
                .employees_by_department()
                .employees_by_agegroup()
        )


# ---------- High-level processing ----------
def process_csv_file(filepath: str, outputs_folder: str = "outputs") -> dict:
    os.makedirs(outputs_folder, exist_ok=True)

    # cleaning
    cleaner = DataCleaner(filepath).clean()
    cleaned_df = cleaner.df

    cleaned_path = os.path.join(outputs_folder, "cleaned_data.csv")
    cleaned_df.to_csv(cleaned_path, index=False)

    # reports
    reports_folder = os.path.join(outputs_folder, "reports")
    ReportBuilder(cleaned_df) \
        .department_report() \
        .city_report() \
        .age_group_report() \
        .export(reports_folder)

    # plots
    plots_folder = os.path.join(outputs_folder, "plots")
    Visualizer(cleaned_df, plots_folder).build_all()

    return {
        "cleaned_data": cleaned_path,
        "reports_folder": reports_folder,
        "plots_folder": plots_folder,
    }


def stream_process_csv(file_obj, outputs_folder: str = "outputs", chunksize: int = 50_000) -> str:
    os.makedirs(outputs_folder, exist_ok=True)
    out_path = os.path.join(outputs_folder, "stream_processed.csv")

    first_chunk = True
    with open(out_path, "w", newline="") as out_f:
        for chunk in pd.read_csv(file_obj, chunksize=chunksize):
            # minimal dataset — no numeric filtering; just write in chunks
            chunk.to_csv(out_f, index=False, header=first_chunk)
            first_chunk = False

    return out_path
