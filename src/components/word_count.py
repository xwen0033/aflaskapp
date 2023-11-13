import os
import plotly.express as px

# Function to analyze files in a folder
def analyze_folder_word_count(folder_path):
    if os.path.isdir(folder_path):
        file_list = [
            f for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.csv')
        ]

        # Create a list to store word counts for each file
        word_counts = []

        for filename in file_list:
            with open(os.path.join(folder_path, filename), 'r') as file:
                text = file.read()
                words = text.split()
                word_count = len(words)
                word_counts.append({"File": filename, "Word Count": word_count})
        return word_counts
    raise ValueError("Please enter a valid directory path")

def plot_word_count(data):
    fig = px.bar(data, x="File", y="Word Count", title="Word Count Analysis")
    fig.update_xaxes(type='category')
    return fig.to_html(full_html=False)