import streamlit as st
import pandas as pd
from podcast_finder import search_podcasts
from social_media_finder import find_social_media_profiles
from csv_exporter import generate_csv

st.set_page_config(page_title="Podcast Finder", page_icon="🎙️", layout="wide")

st.title("🎙️ Podcast Finder")

# User input
user_input = st.text_input("Enter a topic or key-phrase to search for podcasts:", "")

if user_input:
    st.subheader("Search Results")
    
    # Search for podcasts
    podcasts = search_podcasts(user_input)
    
    if podcasts:
        # Create a list to store all podcast data
        all_podcast_data = []
        
        for podcast in podcasts:
            st.write(f"### {podcast['title']}")
            st.write(f"**Description:** {podcast['description']}")
            st.write(f"**URL:** {podcast['url']}")
            
            # Find social media profiles
            social_media_profiles = find_social_media_profiles(podcast['author'])
            
            if social_media_profiles:
                st.write("**Social Media Profiles:**")
                for platform, url in social_media_profiles.items():
                    st.write(f"- {platform}: {url}")
            else:
                st.write("No social media profiles found.")
            
            st.write("---")
            
            # Add podcast data to the list
            podcast_data = {
                "Title": podcast['title'],
                "Description": podcast['description'],
                "URL": podcast['url'],
                "Author": podcast['author']
            }
            podcast_data.update(social_media_profiles)
            all_podcast_data.append(podcast_data)
        
        # Generate CSV
        if all_podcast_data:
            csv_data = generate_csv(all_podcast_data)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="podcast_results.csv",
                mime="text/csv"
            )
    else:
        st.write("No podcasts found. Try a different search term.")
else:
    st.write("Enter a topic or key-phrase to search for podcasts.")

# Add some styling
st.markdown(
    """
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
