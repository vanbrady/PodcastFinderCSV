import requests
from bs4 import BeautifulSoup

def find_social_media_profiles(author):
    """
    Find social media profiles for a given podcast author.
    
    Args:
    author (str): The name of the podcast author.
    
    Returns:
    dict: A dictionary of social media platforms and their corresponding profile URLs.
    """
    search_url = f"https://www.google.com/search?q={author} podcast social media"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        social_media_platforms = {
            "twitter.com": "Twitter",
            "facebook.com": "Facebook",
            "instagram.com": "Instagram",
            "linkedin.com": "LinkedIn",
            "youtube.com": "YouTube"
        }
        
        profiles = {}
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/url?q='):
                url = href.split('/url?q=')[1].split('&')[0]
                for platform, name in social_media_platforms.items():
                    if platform in url:
                        profiles[name] = url
                        break
        
        return profiles
    except requests.RequestException as e:
        print(f"Error finding social media profiles: {e}")
        return {}
