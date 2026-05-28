import os
import googleapiclient.discovery
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

def update_title():
    # Load credentials from GitHub Secrets
    creds_data = {
        "client_id": os.environ['YT_CLIENT_ID'],
        "client_secret": os.environ['YT_CLIENT_SECRET'],
        "refresh_token": os.environ['YT_REFRESH_TOKEN'],
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    creds = Credentials.from_authorized_user_info(creds_data)
    
    # Refresh token if expired
    if creds.expired:
        creds.refresh(google.auth.transport.requests.Request())
        
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    # Replace with your actual Video ID
    VIDEO_ID = "YOUR_VIDEO_ID" 

    # Get video stats
    request = youtube.videos().list(part="statistics,snippet", id=VIDEO_ID)
    response = request.execute()
    
    video = response['items'][0]
    views = video['statistics']['viewCount']
    snippet = video['snippet']
    
    new_title = f"This video has {views} views!"

    if snippet['title'] != new_title:
        snippet['title'] = new_title
        youtube.videos().update(part="snippet", body={"id": VIDEO_ID, "snippet": snippet}).execute()
        print(f"Updated title to: {new_title}")
    else:
        print("Title is already up to date.")

if __name__ == "__main__":
    update_title()
