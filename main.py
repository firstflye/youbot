import os
import googleapiclient.discovery
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

def update_title():
    # 1. Check if Environment Variables exist
    required_vars = ['YT_CLIENT_ID', 'YT_CLIENT_SECRET', 'YT_REFRESH_TOKEN']
    for var in required_vars:
        if var not in os.environ:
            print(f"Error: Missing environment variable {var}")
            return

    # 2. Setup Credentials from GitHub Secrets
    creds_data = {
        "client_id": os.environ['YT_CLIENT_ID'],
        "client_secret": os.environ['YT_CLIENT_SECRET'],
        "refresh_token": os.environ['YT_REFRESH_TOKEN'],
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    
    try:
        creds = Credentials.from_authorized_user_info(creds_data)
        
        # Refresh the token if it's expired
        if creds.expired:
            creds.refresh(google.auth.transport.requests.Request())
            
        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

        # IMPORTANT: Replace this with your actual Video ID once you upload
        # Example: VIDEO_ID = "dQw4w9WgXcQ"
        VIDEO_ID = "YOUR_VIDEO_ID" 

        if VIDEO_ID == "YOUR_VIDEO_ID":
            print("Error: You haven't set your VIDEO_ID yet in main.py")
            return

        # 3. Get current video statistics and snippet
        request = youtube.videos().list(
            part="statistics,snippet",
            id=VIDEO_ID
        )
        response = request.execute()
        
        # Check if the video exists
        if not response.get('items'):
            print(f"Error: No video found with ID: {VIDEO_ID}. Check the ID and privacy settings.")
            return

        video = response['items'][0]
        views = video['statistics']['viewCount']
        snippet = video['snippet']
        
        # 4. Create the new title
        new_title = f"This video has {views} views!"
        
        # Only update if the title has actually changed to save API quota
        if snippet['title'] != new_title:
            print(f"Current Title: {snippet['title']}")
            snippet['title'] = new_title
            
            youtube.videos().update(
                part="snippet",
                body={
                    "id": VIDEO_ID,
                    "snippet": snippet
                }
            ).execute()
            print(f"Successfully updated title to: {new_title}")
        else:
            print(f"No update needed. Title is already: {new_title}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_title()
