import requests

def search_podcasts(query):
    """
    Search for podcasts using the iTunes Search API.
    
    Args:
    query (str): The search term to find podcasts.
    
    Returns:
    list: A list of dictionaries containing podcast information.
    """
    base_url = "https://itunes.apple.com/search"
    params = {
        "term": query,
        "entity": "podcast",
        "limit": 10  # Adjust this number to get more or fewer results
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        podcasts = []
        for result in data.get("results", []):
            podcast = {
                "title": result.get("collectionName"),
                "description": result.get("description", "No description available"),
                "url": result.get("collectionViewUrl"),
                "author": result.get("artistName")
            }
            podcasts.append(podcast)
        
        return podcasts
    except requests.RequestException as e:
        print(f"Error searching for podcasts: {e}")
        return []
