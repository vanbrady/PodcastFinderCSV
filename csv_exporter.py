import pandas as pd
import io

def generate_csv(podcast_data):
    """
    Generate a CSV file from the podcast data.
    
    Args:
    podcast_data (list): A list of dictionaries containing podcast information.
    
    Returns:
    str: CSV data as a string.
    """
    df = pd.DataFrame(podcast_data)
    
    # Reorder columns to have Title, Description, URL, and Author first
    columns = ['Title', 'Description', 'URL', 'Author'] + [col for col in df.columns if col not in ['Title', 'Description', 'URL', 'Author']]
    df = df[columns]
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()
