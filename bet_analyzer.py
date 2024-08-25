import pandas as pd
import os
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
    if df.empty:
        raise ValueError("DataFrame is empty. No HTML report generated.")
    
    success_rate_data = df[['Time', 'Correct Prediction']].groupby('Time').sum().reset_index()
    win_loss_data = df.groupby('Betted On')[['Wincount', 'Losscount']].sum().reset_index()
    average_value_data = df.groupby('Betted On').agg(
        average_value=('CurrentValue', 'mean')
    ).reset_index()
    
    # Calculate totals for Win and Loss Counts
    totals = win_loss_data[['Wincount', 'Losscount']].sum()
    totals_df = pd.DataFrame({
        'Betted On': ['Total'],
        'Wincount': [totals['Wincount']],
        'Losscount': [totals['Losscount']]
    })

    # Append totals row to win_loss_data
    win_loss_data = pd.concat([win_loss_data, totals_df], ignore_index=True)

    # Prepare data for the new chart
    current_value_data = df[['Time', 'CurrentValue']].groupby('Time').mean().reset_index()

    html = f"""
<html>
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            background-color: #28a745;
        }}
        .progress-bar-success.yellow {{
            background-color: #ffc107;
        }}
        .progress-bar-success.red {{
            background-color: #dc3545;
        }}
        .toggle-content {{
            display: none;
        }}
        .toggle-button {{
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 10px; /* Space between charts */
            height: 100vh; /* Full viewport height */
            padding: 10px; /* Optional padding around the grid */
        }}

        .chart-container {{
            background-color: #fff; /* Background color for containers */
            border: 1px solid #ddd; /* Border around containers */
            border-radius: 8px; /* Rounded corners */
            padding: 10px; /* Padding inside containers */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional shadow for a card-like effect */
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        canvas {{
            width: 100% !important; /* Make sure canvas takes full width of its container */
            height: auto !important; /* Maintain aspect ratio */
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
            
            if (body.classList.contains('dark-mode')) {{
                body.classList.remove('dark-mode');
                body.classList.add('light-mode');
                button.innerText = 'Dark Mode';
                tables.forEach(table => table.classList.remove('dark-mode'));
                tables.forEach(table => table.classList.add('light-mode'));
            }} else {{
                body.classList.remove('light-mode');
                body.classList.add('dark-mode');
                button.innerText = 'Light Mode';
                tables.forEach(table => table.classList.remove('light-mode'));
                tables.forEach(table => table.classList.add('dark-mode'));
            }}
        }}

        document.addEventListener('DOMContentLoaded', function () {{
            var ctx1 = document.getElementById('successRateChart').getContext('2d');
            var successRateChart = new Chart(ctx1, {{
                type: 'line',
                data: {{
                    labels: {success_rate_data['Time'].astype('str').tolist()},
                    datasets: [{{
                        label: 'Correct Predictions',
                        data: {success_rate_data['Correct Prediction'].tolist()},
                        borderColor: '#28a745',
                        backgroundColor: 'rgba(40, 167, 69, 0.2)',
                        fill: true
                    }}]
                }},
                options: {{
                    scales: {{
                        x: {{
                            title: {{
                                display: true,
                                text: 'Time'
                            }}
                        }},
                        y: {{
                            title: {{
                                display: true,
                                text: 'Count'
                            }}
                        }}
                    }}
                }}
            }});

            var ctx2 = document.getElementById('winLossChart').getContext('2d');
            var winLossChart = new Chart(ctx2, {{
                type: 'bar',
                data: {{
                    labels: {win_loss_data['Betted On'].tolist()},
                    datasets: [
                        {{
                            label: 'Wins',
                            data: {win_loss_data['Wincount'].tolist()},
                            backgroundColor: '#007bff'
                        }},
                        {{
                            label: 'Losses',
                            data: {win_loss_data['Losscount'].tolist()},
                            backgroundColor: '#dc3545'
                        }}
                    ]
                }},
                options: {{
                    scales: {{
                        x: {{
                            title: {{
                                display: true,
                                text: 'Bet Type'
                            }}
                        }},
                        y: {{
                            title: {{
                                display: true,
                                text: 'Count'
                            }}
                        }}
                    }}
                }}
            }});

            var ctx3 = document.getElementById('averageValueChart').getContext('2d');
            var averageValueChart = new Chart(ctx3, {{
                type: 'pie',
                data: {{
                    labels: {average_value_data['Betted On'].tolist()},
                    datasets: [{{
                        label: 'Average Current Value',
                        data: {average_value_data['average_value'].tolist()},
                        backgroundColor: ['#007bff', '#28a745']
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'top',
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(tooltipItem) {{
                                    return tooltipItem.label + ': $' + tooltipItem.raw.toFixed(2);
                                }}
                            }}
                        }}
                    }}
                }}
            }});

            var ctx4 = document.getElementById('currentValueChart').getContext('2d');
            var currentValueChart = new Chart(ctx4, {{
                type: 'line',
                data: {{
                    labels: {current_value_data['Time'].astype('str').tolist()},
                    datasets: [{{
                        label: 'Current Value',
                        data: {current_value_data['CurrentValue'].tolist()},
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0, 123, 255, 0.2)',
                        fill: true
                    }}]
                }},
                options: {{
                    scales: {{
                        x: {{
                            title: {{
                                display: true,
                                text: 'Time'
                            }}
                        }},
                        y: {{
                            title: {{
                                display: true,
                                text: 'Current Value'
                            }}
                        }}
                    }}
                }}
            }});
        }});
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
    {win_loss_data.to_html(index=False, classes='table table-custom dark-mode', border=0)}

    <h3>Charts:</h3>

    <div class="chart-grid">
        <div class="chart-container">
            <canvas id="successRateChart"></canvas>
        </div>
         <div class="chart-container">
            <canvas id="currentValueChart"></canvas>
        </div>
        <div class="chart-container">
            <canvas id="winLossChart"></canvas>
        </div>
        <div class="chart-container">
            <canvas id="averageValueChart"></canvas>
        </div>
       
    </div>
    





    
    <h3>Average Current Value:</h3>
    <p>Correct Bets: ${correct_avg_value:.2f}</p>
    <p>Incorrect Bets: ${incorrect_avg_value:.2f}</p>
    
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
        {df.to_html(classes='table table-striped table-custom')}
    </div>
</body>
</html>
"""

    # Save the HTML content to the file
    with open(OUTPUT_HTML_FILE, 'w') as file:
        file.write(html)
    print(f"HTML report generated at {OUTPUT_HTML_FILE}")

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

if __name__ == "__main__":
    analyze_and_push()
