import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Label, Button, Radiobutton, StringVar, Listbox, Scrollbar, VERTICAL, RIGHT, Y, messagebox, Toplevel
import os
import webbrowser
from pandasgui import show  # For PandasGUI

class BetAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bet Analyzer")
        self.maximize_window()

        self.directory = 'logs'
        self.create_widgets()
        self.list_csv_files()

    def maximize_window(self):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the window size to the screen size
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        self.file_label = Label(self.root, text="Select a CSV file:")
        self.file_label.pack(pady=10)

        self.file_listbox = Listbox(self.root, width=80, height=10)
        self.file_listbox.pack(pady=5, side='left', fill='both')

        self.scrollbar = Scrollbar(self.root, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.file_listbox.yview)

        self.select_button = Button(self.root, text="Select File", command=self.load_file)
        self.select_button.pack(pady=5)

        self.view_option = StringVar(value="Graphs")
        self.graphs_radio = Radiobutton(self.root, text="Graphs", variable=self.view_option, value="Graphs")
        self.graphs_radio.pack(anchor='w')
        self.tables_radio = Radiobutton(self.root, text="Tables - PandasGUI", variable=self.view_option, value="PandasGUI")
        self.tables_radio.pack(anchor='w')
        self.html_radio = Radiobutton(self.root, text="Tables - HTML", variable=self.view_option, value="HTML")
        self.html_radio.pack(anchor='w')
        self.excel_radio = Radiobutton(self.root, text="Tables - Excel", variable=self.view_option, value="Excel")
        self.excel_radio.pack(anchor='w')

        self.analyze_button = Button(self.root, text="Analyze", command=self.analyze_file)
        self.analyze_button.pack(pady=20)

    def list_csv_files(self):
        if not os.path.exists(self.directory):
            messagebox.showerror("Error", "Directory does not exist.")
            return

        files = [f for f in os.listdir(self.directory) if f.endswith('.csv')]
        if not files:
            messagebox.showinfo("Info", "No CSV files found in the directory.")
            return

        self.file_listbox.delete(0, 'end')
        for file in files:
            self.file_listbox.insert('end', file)

    def load_file(self):
        selected_file = self.file_listbox.get(self.file_listbox.curselection())
        if selected_file:
            self.file_path = os.path.join(self.directory, selected_file)
            self.select_button.config(text=os.path.basename(selected_file))

    def analyze_file(self):
        if not hasattr(self, 'file_path'):
            messagebox.showerror("Error", "No file selected.")
            return

        try:
            df = pd.read_csv(self.file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading the CSV file: {e}")
            return

        if 'Time' not in df.columns:
            messagebox.showerror("Error", "'Time' column not found.")
            return

        # Process data
        self.process_data(df)
        
        # Display results based on selected option
        self.display_results(df)

    def process_data(self, df):
        try:
            df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
            if df['Time'].isna().any():
                messagebox.showwarning("Warning", "Some dates could not be parsed. Check the data format.")
        except Exception as e:
            messagebox.showerror("Error", f"Error converting 'Time' column: {e}")
            return

        df['Wincount'] = (df['Wincount'] > 0).astype(int)
        df['Losscount'] = (df['Losscount'] > 0).astype(int)
        df['Next Wincount'] = df['Wincount'].shift(-1)
        df['Actual Bet'] = df.apply(
            lambda row: row['Betted On'] if row['Next Wincount'] > 0 else ('B' if row['Betted On'] == 'A' else 'A'),
            axis=1
        )


        
        # Calculate 'Correct Prediction' excluding the last value
        df['Correct Prediction'] = (df['Betted On'] == df['Actual Bet']).iloc[:-1]

        # Fill NaN values with False (or True depending on your logic)
        df['Correct Prediction'] = df['Correct Prediction'].fillna(False)

        # Compute additional statistics excluding the last record
        self.success_rate = (df['Correct Prediction'].iloc[:-1]).mean() * 100

        # Calculate correct and incorrect average values
        self.correct_avg_value = df[df['Correct Prediction']]['CurrentValue'].mean()
        self.incorrect_avg_value = df[~df['Correct Prediction']]['CurrentValue'].mean()

    def display_results(self, df):
        if self.view_option.get() == "Graphs":
            self.plot_graphs(df)
        elif self.view_option.get() == "PandasGUI":
            self.display_tables_pandasgui(df)
        elif self.view_option.get() == "HTML":
            self.display_tables_html(df, self.success_rate, self.correct_avg_value, self.incorrect_avg_value)
        elif self.view_option.get() == "Excel":
            self.display_tables_excel(df)

    def plot_graphs(self, df):
        sns.set(style="whitegrid")
        plt.figure(figsize=(14, 14))

        # Subplot 1: Success Rate Plot
        plt.subplot(2, 2, 1)
        plt.bar(['Success Rate'], [self.success_rate], color='lightgreen', edgecolor='black')
        plt.title('Success Rate', fontsize=12)
        plt.ylabel('Percentage', fontsize=10)
        plt.ylim(0, 100)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Subplot 2: Betting Comparison Plot
        plt.subplot(2, 2, 2)
        betting_comparison = df.groupby(['Betted On', 'Actual Bet']).size().unstack().fillna(0)
        betting_comparison.plot(kind='bar', stacked=True, ax=plt.gca(), color=['skyblue', 'salmon'])
        plt.title('Betted On vs Actual Bet', fontsize=12)
        plt.xlabel('Betted On', fontsize=10)
        plt.ylabel('Count', fontsize=10)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.legend(title='Actual Bet', title_fontsize='8', fontsize='8')
        plt.grid(True, linestyle='--', alpha=0.7)

        # Subplot 3: Average Current Value Plot
        plt.subplot(2, 2, 3)
        values = [self.correct_avg_value, self.incorrect_avg_value]
        labels = ['Correct Bets', 'Incorrect Bets']
        plt.bar(labels, values, color=['lightgreen', 'salmon'], edgecolor='black')
        plt.title('Average Current Value Comparison', fontsize=12)
        plt.ylabel('Average Current Value', fontsize=10)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Subplot 4: Time Series Plot
        plt.subplot(2, 2, 4)
        df_sorted = df.sort_values('Time')
        plt.plot(df_sorted['Time'], df_sorted['CurrentValue'], marker='o', linestyle='-', color='blue')
        plt.title('Current Value Over Time', fontsize=12)
        plt.xlabel('Time', fontsize=10)
        plt.ylabel('Current Value', fontsize=10)
        plt.xticks(rotation=45, fontsize=8)
        plt.yticks(fontsize=8)
        plt.grid(True, linestyle='--', alpha=0.7)

        plt.tight_layout(pad=0.5)
        plt.show()

    def display_tables_pandasgui(self, df):
        gui = show(df, settings={'block': True})

    def display_tables_html(self, df, success_rate, correct_avg_value, incorrect_avg_value):
        html = f"""
<html>
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap">
    <style>
        body {{
            font-family: 'Roboto Mono', monospace;
            margin: 0;
            padding: 0;
            transition: background-color 0.3s, color 0.3s;
        }}
        .light-mode {{
            background-color: #ffffff;
            color: #000000;
        }}
        .dark-mode {{
            background-color: #121212;
            color: #e0e0e0;
        }}
        .progress-bar-success {{
            transition: width 0.3s;
        }}
        .progress-bar-success.green {{
            background-color: #28a745; /* Bootstrap green */
        }}
        .progress-bar-success.yellow {{
            background-color: #ffc107; /* Bootstrap yellow */
        }}
        .progress-bar-success.red {{
            background-color: #dc3545; /* Bootstrap red */
        }}
        .toggle-content {{
            display: none; /* Hidden by default */
        }}
        .toggle-button {{
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
        }}
        /* Enhanced table styling for light mode */
        .table-custom.light-mode {{
            border: 2px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .table-custom.light-mode thead th {{
            background-color: #007bff;
            color: white;
        }}
        .table-custom.light-mode tbody tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .table-custom.light-mode tbody tr:nth-child(odd) {{
            background-color: #ffffff;
        }}
        .table-custom.light-mode tbody tr:hover {{
            background-color: #e9ecef;
        }}
        /* Enhanced table styling for dark mode */
        .table-custom.dark-mode {{
            border: 2px solid #333;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}
        .table-custom.dark-mode thead th {{
            background-color: #444;
            color: #e0e0e0;
        }}
        .table-custom.dark-mode tbody tr:nth-child(even) {{
            background-color: #1e1e1e;
        }}
        .table-custom.dark-mode tbody tr:nth-child(odd) {{
            background-color: #121212;
        }}
        .table-custom.dark-mode tbody tr:hover {{
            background-color: #333;
        }}
    </style>
    <script>
        function toggleContent() {{
            var content = document.getElementById('actual-bet-data');
            var button = document.getElementById('toggle-button');
            if (content.style.display === 'none') {{
                content.style.display = 'block';
                button.innerText = 'Hide Data with Actual Bet Column';
            }} else {{
                content.style.display = 'none';
                button.innerText = 'Show Data with Actual Bet Column';
            }}
        }}
        
        function toggleMode() {{
            var body = document.body;
            var button = document.getElementById('mode-toggle');
            var tables = document.querySelectorAll('.table-custom');
            var headers = document.querySelectorAll('th');
            
            if (body.classList.contains('dark-mode')) {{
                body.classList.remove('dark-mode');
                body.classList.add('light-mode');
                button.innerText = 'Dark Mode';
                tables.forEach(table => table.classList.remove('dark-mode'));
                tables.forEach(table => table.classList.add('light-mode'));
                headers.forEach(th => th.classList.remove('dark-mode'));
                headers.forEach(th => th.classList.add('light-mode'));
            }} else {{
                body.classList.remove('light-mode');
                body.classList.add('dark-mode');
                button.innerText = 'Light Mode';
                tables.forEach(table => table.classList.remove('light-mode'));
                tables.forEach(table => table.classList.add('dark-mode'));
                headers.forEach(th => th.classList.remove('light-mode'));
                headers.forEach(th => th.classList.add('dark-mode'));
            }}
        }}
    </script>
</head>
<body class="container dark-mode">
    <button id="mode-toggle" class="btn btn-secondary toggle-button" onclick="toggleMode()">Light Mode</button>
    
    <h2 class="mt-4">Detailed Analysis</h2>
    
    <h3>Success Rate:</h3>
    <div class="progress">
        <div class="progress-bar progress-bar-success { 'green' if success_rate > 50 else 'yellow' if success_rate > 45 else 'red' }"
            role="progressbar"
            style="width: {success_rate:.2f}%;"
            aria-valuenow="{success_rate:.2f}"
            aria-valuemin="0"
            aria-valuemax="100">
            {success_rate:.2f}%
        </div>
    </div>
    
    <h3>Win and Loss Counts:</h3>
    {df.groupby('Betted On')[['Wincount', 'Losscount']].sum().to_html(classes='table table-custom dark-mode')}
    
    <h3>Average Current Value:</h3>
    <p>Correct Bets: {correct_avg_value:.2f}</p>
    <p>Incorrect Bets: {incorrect_avg_value:.2f}</p>
    
    <h3>Summary Statistics by Bet Type:</h3>
    {df.groupby('Betted On').agg(
        total_wins=pd.NamedAgg(column='Wincount', aggfunc='sum'),
        total_losses=pd.NamedAgg(column='Losscount', aggfunc='sum'),
        average_value=pd.NamedAgg(column='CurrentValue', aggfunc='mean'),
        min_value=pd.NamedAgg(column='CurrentValue', aggfunc='min'),
        max_value=pd.NamedAgg(column='CurrentValue', aggfunc='max')
    ).reset_index().to_html(classes='table table-custom dark-mode')}
    
    <h3>Data with Actual Bet Column:</h3>
    <button id="toggle-button" class="btn btn-primary" onclick="toggleContent()">Show Data with Actual Bet Column</button>
    <div id="actual-bet-data" class="toggle-content">
        {df.iloc[:-1].to_html(classes='table table-custom dark-mode')}
    </div>
</body>
</html>
"""


        with open("table_analysis.html", "w") as file:
            file.write(html)
        
        webbrowser.open("table_analysis.html")

    def display_tables_excel(self, df):
        with pd.ExcelWriter('table_analysis.xlsx') as writer:
            df.describe(include='all').to_excel(writer, sheet_name='Overall Data Summary')
            df.groupby('Betted On')[['Wincount', 'Losscount']].sum().to_excel(writer, sheet_name='Win and Loss Counts')
            summary = df.groupby('Betted On').agg(
                total_wins=pd.NamedAgg(column='Wincount', aggfunc='sum'),
                total_losses=pd.NamedAgg(column='Losscount', aggfunc='sum'),
                average_value=pd.NamedAgg(column='CurrentValue', aggfunc='mean'),
                min_value=pd.NamedAgg(column='CurrentValue', aggfunc='min'),
                max_value=pd.NamedAgg(column='CurrentValue', aggfunc='max')
            ).reset_index()
            summary.to_excel(writer, sheet_name='Summary Statistics by Bet Type')
            df.head(10).to_excel(writer, sheet_name='Data with Actual Bet Column')

        messagebox.showinfo("Info", "Table analysis exported to 'table_analysis.xlsx'.")

if __name__ == "__main__":
    root = Tk()
    app = BetAnalyzerApp(root)
    root.mainloop()
