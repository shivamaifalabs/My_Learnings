import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Visualizer:
    def __init__(self, df):
        self.df = df
        os.makedirs("outputs/plots", exist_ok=True)

    # 1. Avg Salary by Department
    def salary_by_department(self):
        plt.figure(figsize=(8,5))
        sns.barplot(x="Department", y="Salary", data=self.df, estimator=sum)
        plt.title("Total Salary by Department")
        plt.savefig("outputs/plots/salary_by_department.png", dpi=300, bbox_inches="tight")
        plt.close()
        return self

    # 2. Employee count by City (Pie Chart)
    def employees_by_city(self):
        plt.figure(figsize=(7,7))
        self.df["City"].value_counts().plot(kind="pie", autopct="%1.1f%%")
        plt.title("Employees by City")
        plt.savefig("outputs/plots/employees_by_city.png", dpi=300, bbox_inches="tight")
        plt.close()
        return self

    # 3. Salary Distribution (Histogram)
    def salary_distribution(self):
        plt.figure(figsize=(8,5))
        sns.histplot(self.df["Salary"], kde=True)
        plt.title("Salary Distribution")
        plt.savefig("outputs/plots/salary_distribution.png", dpi=300, bbox_inches="tight")
        plt.close()
        return self

    # 4. Salary Boxplot by Department
    def salary_boxplot(self):
        plt.figure(figsize=(8,5))
        sns.boxplot(x="Department", y="Salary", data=self.df)
        plt.title("Salary Range by Department")
        plt.savefig("outputs/plots/salary_boxplot.png", dpi=300, bbox_inches="tight")
        plt.close()
        return self

    # 5. Call all charts
    def build_all(self):
        return self.salary_by_department() \
                   .employees_by_city() \
                   .salary_distribution() \
                   .salary_boxplot()



from visualizations import Visualizer

df = pd.read_csv("sample_data.csv")
Visualizer(df).build_all()
