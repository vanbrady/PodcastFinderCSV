import streamlit as st
import hashlib
import json
import requests
import time
import re
from datetime import date


# Define the cache decorator for storing search results
@st.cache_data(ttl=3600)  # Cache results for 1 hour
def search_podcasts(query):
    api_key = 'GBVQKFSWXVYYDS6DJ8XN'
    api_secret = 'aFaYxShW^MY^dEweJeuQHq7jy2$QGfjdNV544npL'
    url = "https://api.podcastindex.org/api/1.0/search/byterm?q=" + query

    # Calculate the current Unix time
    epoch_time = int(time.time())

    # Build the hash for authorization
    data_to_hash = api_key + api_secret + str(epoch_time)
    sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()

    # Define request headers
    headers = {
        'X-Auth-Date': str(epoch_time),
        'X-Auth-Key': api_key,
        'Authorization': sha_1,
        'User-Agent': 'podcasting-index-python-cli'
    }

    try:
        # Make the request to the Podcast Index API
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract and format the podcast information
        podcasts = []
        for result in data.get("feeds", []):
            podcast = {
                "title":
                result.get("title"),
                "description":
                result.get("description", "No description available"),
                "url":
                result.get("url"),
                "author":
                result.get("author")
            }
            podcasts.append(podcast)

        # Sanitize the query string to create a valid filename
        sanitized_query = re.sub(r'[^\w\-_\. ]', '_', query)
        output_file = f'{sanitized_query}.json'

        # Write the formatted JSON to a file named after the search query
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f'JSON output written to {output_file}')

        return podcasts
    except requests.RequestException as e:
        print(f"Error searching for podcasts: {e}")
        return []


# Streamlit interface
st.title("Podcast Finder")
st.write("Search for podcasts using the Podcast Index API.")

# Get search query from user
query = st.text_input("Enter search query:")

# Perform search when user submits the form
if st.button("Search"):
    if query:
        results = search_podcasts(query)
        if results:
            for podcast in results:
                st.subheader(podcast["title"])
                st.text(podcast["author"])
                st.text(podcast["description"])
                st.markdown(f"[Link to Podcast]({podcast['url']})")
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a search query.")
