import http.client
import json
import streamlit as st
import time

@st.cache_data(ttl=3600)  # Cache results for 1 hour
def find_social_media_profiles(author):
    """
    Find social media profiles for a given podcast author using serper.dev API.

    Args:
    author (str): The name of the podcast author.

    Returns:
    dict: A dictionary of social media platforms and their corresponding profile URLs.
    """
    # Define the headers for the HTTP request
    headers = {
        'X-API-KEY': '54c237af76e25b52d3df0750c34b71e68651f1f7',  # Replace with your actual API key
        'Content-Type': 'application/json'
    }

    social_media_platforms = {
        "linkedin.com/in/": "LinkedIn",
        "twitter.com": "Twitter",
        "facebook.com": "Facebook",
        "instagram.com": "Instagram",
        "youtube.com": "YouTube"
    }

    profiles = {}

    for platform_query, platform_name in social_media_platforms.items():
        # Prepare the search query with the author's name and platform name
        payload = json.dumps({
            "q": f"inurl:{platform_query} {author}"
        })

        # Establish the connection and send the request
        conn = http.client.HTTPSConnection("google.serper.dev")
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")

        # Parse the JSON response
        search_results = json.loads(data)
        try:
            first_url = search_results['organic'][0]['link']
        except (IndexError, KeyError):
            first_url = None

        # Log the profile URL
        print(f"Author: {author} - {platform_name} URL: {first_url}")

        if first_url:
            profiles[platform_name] = first_url

        # Wait for two seconds before making the next API call to avoid rate limits
        time.sleep(2)

    return profiles