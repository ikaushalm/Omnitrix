import pandas as pd
import os
import webbrowser
import subprocess
from datetime import datetime

# Get the current working directory
current_dir = os.getcwd()
print(f"Current Directory: {current_dir}")

# Define the path to go one directory up
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
print(f"Parent Directory: {parent_dir}")

# Define the path to the PagePush directory inside the parent directory
pagepush_dir = os.path.join(parent_dir, 'PagePush')
print(f"PagePush Directory: {pagepush_dir}")

# Define the directory where CSV files are stored
DIRECTORY = 'logs'
OUTPUT_HTML_FILE = os.path.join(pagepush_dir, 'index.html')  # Updated path
REPO_DIR = pagepush_dir  # Directory where the Git repository is initialized

def git_push():
    """Commit and push the generated HTML file to the Git repository."""
    try:
        # Change to the repository directory
        os.chdir(REPO_DIR)
        
        # Add the HTML file to the staging area
        subprocess.run(["git", "add", OUTPUT_HTML_FILE], check=True)
        
        # Commit the changes
        commit_message = f"Add analysis report: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Push the changes to the remote repository
        subprocess.run(["git", "push", "origin", "main"], check=True)  # Adjust branch name if necessary
        
        print("Changes pushed to remote repository.")
    
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")

def get_latest_csv_file(directory):
    """Get the most recent CSV file in the directory."""
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    if not files:
        raise FileNotFoundError("No CSV files found in the directory.")
    
    # Get the most recent file based on modification time
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)

def process_data(df):
    """Process the data and calculate statistics."""
    df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    if df['Time'].isna().any():
        raise ValueError("Some dates could not be parsed. Check the data format.")
    
    df['Wincount'] = (df['Wincount'] > 0).astype(int)
    df['Losscount'] = (df['Losscount'] > 0).astype(int)
    df['Next Wincount'] = df['Wincount'].shift(-1)
    df['Actual Bet'] = df.apply(
        lambda row: row['Betted On'] if row['Next Wincount'] > 0 else ('B' if row['Betted On'] == 'A' else 'A'),
        axis=1
    )
    df['Correct Prediction'] = (df['Betted On'] == df['Actual Bet']).iloc[:-1]
    df['Correct Prediction'] = df['Correct Prediction'].fillna(False)

    success_rate = (df['Correct Prediction'].iloc[:-1]).mean() * 100
    correct_avg_value = df[df['Correct Prediction']]['CurrentValue'].mean()
    incorrect_avg_value = df[~df['Correct Prediction']]['CurrentValue'].mean()

    return df, success_rate, correct_avg_value, incorrect_avg_value

def generate_html(df, success_rate, correct_avg_value, incorrect_avg_value):
    """Generate an HTML file with analysis results."""
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

    with open(OUTPUT_HTML_FILE, "w") as file:
        file.write(html)
    
    # Optionally open the HTML file in a web browser
    # webbrowser.open(OUTPUT_HTML_FILE)

def analyze_and_push():
    """Main function to analyze data and push results to Git."""
    try:
        file_path = get_latest_csv_file(DIRECTORY)
        print(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)
        df, success_rate, correct_avg_value, incorrect_avg_value = process_data(df)
        generate_html(df, success_rate, correct_avg_value, incorrect_avg_value)
        print(f"HTML report generated: {OUTPUT_HTML_FILE}")
        git_push()
    except Exception as e:
        print(f"An error occurred: {e}")

