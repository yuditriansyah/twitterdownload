import os
import time
import requests
import base64
from io import BytesIO
import tweepy
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3.exceptions
import concurrent.futures

# Load env vars
load_dotenv()
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
TARGET_USERNAME = os.getenv("TARGET_USERNAME")

# Setup API
if not all([TWITTER_BEARER_TOKEN, IMGBB_API_KEY, TARGET_USERNAME]):
    raise ValueError("Missing required environment variables. Please check your .env file.")

# Remove @ symbol from username if present
if TARGET_USERNAME.startswith('@'):
    TARGET_USERNAME = TARGET_USERNAME[1:]

twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

# Create a requests session with retry strategy
def create_robust_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.timeout = 30  # 30 second timeout
    return session

# Create robust session for image downloads
robust_session = create_robust_session()

def load_processed_ids():
    if not os.path.exists("processed_ids.txt"):
        return set()
    with open("processed_ids.txt", "r") as f:
        return set(f.read().splitlines())

def save_processed_id(tweet_id):
    with open("processed_ids.txt", "a") as f:
        f.write(f"{tweet_id}\n")

def upload_to_imgbb(image_data, filename):
    """Upload image to ImgBB and return the URL"""
    try:
        # Convert image data to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # ImgBB API endpoint
        url = "https://api.imgbb.com/1/upload"
        
        # Prepare payload
        payload = {
            'key': IMGBB_API_KEY,
            'image': image_base64,
            'name': filename
        }
        
        # Make request with shorter timeout
        response = requests.post(url, data=payload, timeout=15)  # Reduced from 30 to 15
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                image_url = result['data']['url']
                return image_url
            else:
                print(f"ImgBB API error: {result.get('error', 'Unknown error')}")
                return None
        else:
            print(f"ImgBB upload failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error uploading to ImgBB: {e}")
        return None

def save_uploaded_url(tweet_id, index, url):
    """Save uploaded image URL to a file"""
    with open("uploaded_images.txt", "a") as f:
        f.write(f"{tweet_id}_{index}: {url}\n")

def download_and_upload(tweet_id, photo_url, index):
    max_retries = 2  # Reduced from 3 to 2
    for attempt in range(max_retries):
        try:
            print(f"Attempting to download image (attempt {attempt + 1}/{max_retries})")
            response = robust_session.get(photo_url, timeout=15)  # Reduced timeout from 30 to 15
            if response.status_code == 200:
                file_name = f"{tweet_id}_{index}.jpg"
                
                # Upload to ImgBB
                uploaded_url = upload_to_imgbb(response.content, file_name)
                
                if uploaded_url:
                    print(f"✅ Uploaded {file_name} to ImgBB: {uploaded_url}")
                    save_uploaded_url(tweet_id, index, uploaded_url)
                    return True
                else:
                    print(f"❌ Failed to upload {file_name} to ImgBB")
                    return False
            else:
                print(f"Failed to download image from {photo_url}. Status code: {response.status_code}")
                return False
        except (requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout, 
                urllib3.exceptions.ProtocolError,
                requests.exceptions.ChunkedEncodingError) as e:
            print(f"Network error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 1  # Reduced backoff from 2 to 1 second
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print(f"Failed to download after {max_retries} attempts")
                return False
        except Exception as e:
            print(f"Error downloading/uploading image: {e}")
            return False
    return False

def run_bot():
    print("Bot started. Checking tweets every 1 minute...")
    
    try:
        user = twitter_client.get_user(username=TARGET_USERNAME)
        user_id = user.data.id
        print(f"Found user: {TARGET_USERNAME} (ID: {user_id})")
    except Exception as e:
        print(f"Error getting user info: {e}")
        return

    while True:
        try:
            processed_ids = load_processed_ids()
            print(f"Loaded {len(processed_ids)} processed tweet IDs")

            # Add timeout and error handling for Twitter API calls
            try:
                # Increased max_results from 5 to 20 for faster processing
                tweets = twitter_client.get_users_tweets(
                    id=user_id,
                    max_results=20,  # Increased from 5 to 20
                    expansions=["attachments.media_keys"],
                    media_fields=["url", "type"]
                )
            except (tweepy.TooManyRequests, tweepy.Unauthorized) as e:
                # Re-raise these specific exceptions to be handled by outer try-except
                raise e
            except Exception as api_error:
                print(f"Twitter API error: {api_error}")
                print("This might be a temporary network issue. Waiting 30 seconds before retry...")
                time.sleep(30)  # Reduced from 120 to 30 seconds
                continue

            if tweets.data:
                print(f"Found {len(tweets.data)} tweets")
                media_map = {m.media_key: m for m in tweets.includes.get("media", [])} if tweets.includes else {}
                
                # Process tweets in parallel for faster execution
                tweets_with_photos = []
                
                for tweet in tweets.data:
                    if str(tweet.id) in processed_ids:
                        print(f"Tweet {tweet.id} already processed, skipping")
                        continue

                    # Only process tweets that have media attachments
                    if hasattr(tweet, "attachments") and tweet.attachments:
                        media_keys = tweet.attachments.get("media_keys", [])
                        
                        # Check if there are any photos in this tweet
                        has_photos = False
                        photo_count = 0
                        
                        for key in media_keys:
                            media = media_map.get(key)
                            if media and media.type == "photo":
                                has_photos = True
                                photo_count += 1
                        
                        if has_photos:
                            tweets_with_photos.append((tweet, media_keys, photo_count))
                        else:
                            print(f"Tweet {tweet.id} has media but no photos - skipping")
                    else:
                        print(f"Tweet {tweet.id} has no media attachments - skipping")
                
                # Process all tweets with photos
                for tweet, media_keys, photo_count in tweets_with_photos:
                    print(f"Tweet {tweet.id} has {photo_count} photo(s) - processing...")
                    
                    # Download all photos from this tweet concurrently
                    import concurrent.futures
                    
                    def download_photo(args):
                        i, key = args
                        media = media_map.get(key)
                        if media and media.type == "photo":
                            print(f"Downloading photo {i+1} from tweet {tweet.id}")
                            return download_and_upload(tweet.id, media.url, i)
                        return False
                    
                    # Use ThreadPoolExecutor for concurrent downloads
                    photo_args = [(i, key) for i, key in enumerate(media_keys) if media_map.get(key) and media_map.get(key).type == "photo"]
                    
                    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                        futures = [executor.submit(download_photo, args) for args in photo_args]
                        results = [future.result() for future in concurrent.futures.as_completed(futures)]
                    
                    # Only save tweet ID after successfully processing photos
                    if any(results):  # If at least one photo was successfully processed
                        save_processed_id(str(tweet.id))
                        print(f"✅ Completed processing tweet {tweet.id}")
                    else:
                        print(f"⚠️ No photos successfully processed for tweet {tweet.id}")
                        
            else:
                print("No tweets found")

        except tweepy.TooManyRequests:
            print("Rate limit exceeded. Waiting 5 minutes before retrying...")
            time.sleep(300)  # Reduced from 900 (15 min) to 300 (5 min)
            continue
        except tweepy.Unauthorized:
            print("Unauthorized access. Please check your Twitter Bearer Token.")
            break
        except (requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout,
                urllib3.exceptions.ProtocolError,
                ConnectionError) as network_error:
            print(f"Network connection error: {network_error}")
            print("This is likely a temporary network issue. Waiting 1 minute before retrying...")
            time.sleep(60)  # Reduced from 300 (5 min) to 60 (1 min)
            continue
        except Exception as e:
            print(f"Error in main loop: {e}")
            print(f"Error type: {type(e).__name__}")
            # Wait a bit longer on other errors to avoid rapid retries
            print("Waiting 2 minutes before retrying...")
            time.sleep(120)  # Reduced from 600 (10 min) to 120 (2 min)
            continue
        
        print("Waiting 1 minute before next check...")
        time.sleep(60)  # Reduced from 300 (5 min) to 60 (1 min)

if __name__ == "__main__":
    run_bot()