import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import messagebox, filedialog, Text, Scrollbar

class StudentPerformanceAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Analysis - Farid Gul Shakir")

        # Frame for input
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.label = tk.Label(self.frame, text="Upload Student Performance CSV File:")
        self.label.pack()

        self.upload_button = tk.Button(self.frame, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.run_button = tk.Button(self.frame, text="Run Analysis", command=self.run_analysis, state=tk.DISABLED)
        self.run_button.pack(pady=10)

        self.file_path = ""

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if self.file_path:
            messagebox.showinfo("File Selected", f"File uploaded: {self.file_path}")
            self.run_button.config(state=tk.NORMAL)

    def run_analysis(self):
        try:
            # Load the data
            print(f"Attempting to read the file: {self.file_path}")
            if self.file_path.endswith('.csv'):
                data = pd.read_csv(self.file_path)
            else:
                data = pd.read_excel(self.file_path)

            print(f"Data loaded successfully:\n{data.head()}")  # Show the first few rows

            # Check for required columns
            required_columns = ['math_score', 'science_score', 'english_score', 'history_score',
                                'geography_score', 'art_score', 'physical_education_score',
                                'computer_science_score', 'foreign_language_score', 'psychology_score']
            if not all(col in data.columns for col in required_columns):
                raise ValueError("The required columns are missing in the data.")

            scores = data[required_columns]

            # Calculate statistics for each subject
            stats_results = {}
            for subject in scores.columns:
                mean = np.mean(scores[subject])
                median = np.median(scores[subject])
                variance = np.var(scores[subject], ddof=1)  # Sample variance
                std_dev = np.std(scores[subject], ddof=1)    # Sample standard deviation
                skewness = stats.skew(scores[subject])
                kurtosis = stats.kurtosis(scores[subject])

                # Confidence interval
                confidence_level = 0.95
                degrees_freedom = len(scores[subject]) - 1
                sample_mean = np.mean(scores[subject])
                sample_standard_error = stats.sem(scores[subject])
                confidence_interval = stats.t.interval(confidence_level, degrees_freedom,
                                                        loc=sample_mean, scale=sample_standard_error)

                # Format confidence interval
                confidence_interval_formatted = f"({confidence_interval[0]:.2f}, {confidence_interval[1]:.2f})"

                # Normality test (Shapiro-Wilk)
                shapiro_test = stats.shapiro(scores[subject])
                p_value = shapiro_test.pvalue

                stats_results[subject] = {
                    "Mean": mean,
                    "Median": median,
                    "Variance": variance,
                    "Standard Deviation": std_dev,
                    "Skewness": skewness,
                    "Kurtosis": kurtosis,
                    "Confidence Interval": confidence_interval_formatted,
                    "P-Value (Shapiro-Wilk)": p_value
                }

            # Display results in a more structured way
            self.display_results(stats_results)

            # Plotting as a bar chart
            self.plot_bar_chart(scores)

        except FileNotFoundError:
            messagebox.showerror("Error", "File not found. Please upload a valid file.")
        except pd.errors.EmptyDataError:
            messagebox.showerror("Error", "No data found in the file. Please upload a valid file.")
        except pd.errors.ParserError:
            messagebox.showerror("Error", "Error parsing the file. Please ensure it is a valid CSV or Excel file.")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            print(f"Error occurred: {str(e)}")  # Print the error to console for debugging

    def display_results(self, stats_results):
        results_window = tk.Toplevel(self.root)
        results_window.title("Statistical Results - Farid Gul Shakir")

        # Create a frame for scrolling
        frame = tk.Frame(results_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrollbar
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, padx=10, pady=10)
        text_widget.pack(expand=True, fill='both')

        for subject, results in stats_results.items():
            text_widget.insert(tk.END, f"\n--- {subject} ---\n")
            for key, value in results.items():
                if isinstance(value, (float, int)):
                    text_widget.insert(tk.END, f"{key}: {value:.2f}\n")
                else:
                    text_widget.insert(tk.END, f"{key}: {value}\n")
            text_widget.insert(tk.END, "\n")

        text_widget.insert(tk.END, "\n--- Your Name ---\nFarid Gul Shakir\n")  # Your name at the bottom
        text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
        scrollbar.config(command=text_widget.yview)  # Link scrollbar to text widget

    def plot_bar_chart(self, scores):
        means = scores.mean()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=means.index, y=means.values, palette='viridis')
        plt.title('Average Scores by Subject - Farid Gul Shakir')
        plt.ylabel('Average Score')
        plt.xlabel('Subjects')
        plt.ylim(0, 100)  # Assuming scores are out of 100

        # Add average values on top of the bars
        for index, value in enumerate(means):
            plt.text(index, value + 1, f"{value:.2f}", ha='center')

        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentPerformanceAnalysisApp(root)
    root.mainloop()