import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import pyperclip  # Library to handle clipboard functionality

def extract_video_url(page_url):
    # Make a request to fetch the HTML content
    response = requests.get(page_url)
    if response.status_code != 200:
        print("Error fetching the webpage")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the video element and get the 'data-mp4-link' attribute
    video_player = soup.find(id="UIVideoPlayer")
    if video_player:
        mp4_link = video_player.get('data-mp4-link')
        if mp4_link:
            # Extract the video link
            video_data = mp4_link.split("etv")[1]
            full_video_url = "https://cdn1.einthusan.io/etv" + video_data
            return full_video_url
        else:
            print("MP4 link not found in the video player element.")
            return None
    else:
        print("Video player element not found.")
        return None

def open_video_in_browser(video_url):
    if video_url:
        webbrowser.open(video_url)
        print(f"Opened video in browser: {video_url}")
    else:
        print("Invalid video URL.")

def open_video_in_player(video_url, player_path):
    if video_url:
        print(f"Opening video in video player: {video_url}")
        os.system(f'"{player_path}" {video_url}')  # Use the absolute path of the player
    else:
        print("Invalid video URL.")

def copy_to_clipboard(text):
    pyperclip.copy(text)
    print(f"Video URL copied to clipboard: {text}")

if __name__ == "__main__":
    # Example URL (replace with actual URL)
    page_url = input("Enter the webpage URL: ")

    # Step 1: Extract the video URL
    video_url = extract_video_url(page_url)

    if video_url:
        # Step 2: Automatically copy the link to the clipboard
        copy_to_clipboard(video_url)

        # Step 3: Choose action: Open in browser or video player
        action = input("Enter 'browser' to open the video in a browser or 'player' to open it in a video player: ").strip().lower()

        if action == "browser":
            # Open video in the browser
            open_video_in_browser(video_url)
        elif action == "player":
            # Open video in video player
            player_path = input("Enter the full path to your video player executable (e.g., C:\\Program Files\\VideoLAN\\VLC\\vlc.exe): ").strip()
            open_video_in_player(video_url, player_path)
        else:
            print("Invalid action. Please choose 'browser' or 'player'.")
    else:
        print("Could not extract video URL.")