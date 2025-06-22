from apify_client import ApifyClientAsync
from dotenv import load_dotenv
import os
from typing import List
import json
load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

async def get_hashtag_views(hashtags: List[str]):
    client = ApifyClientAsync(token=APIFY_TOKEN)
    run_input = {
        "hashtags": hashtags,
        "excludePinnedPosts": False,
        "proxyCountryCode": "None",
        "resultsPerPage": 5,
        "shouldDownloadAvatars": False,
        "shouldDownloadCovers": False,
        "shouldDownloadMusicCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadVideos": False
    }

    try:
        print(f"Starting scrape for hashtags: {hashtags}")
        run = await client.actor("f1ZeP0K58iwlqG2pY").call(run_input=run_input)
        print(f"Run completed with status: {run.get('status', 'unknown')}")
        
        dataset = client.dataset(run["defaultDatasetId"])
        items = await dataset.list_items()
        
        print(f"Found {len(items.items)} items")
        with open("tiktok_hashtag_data.json", "w") as f:
            json.dump(items.items, f, indent=2)
        hashtag_data = {}
        for item in items.items:
            search_hashtag = item.get("searchHashtag")
            
            # Add null check for searchHashtag
            if search_hashtag and isinstance(search_hashtag, dict):
                search_hashtag_name = search_hashtag.get("name")
                search_hashtag_views = search_hashtag.get("views")
                
                if search_hashtag_name and search_hashtag_name not in hashtag_data:
                    hashtag_data[search_hashtag_name] = {
                        "views": search_hashtag_views,
                    }
            else:
                print(f"Warning: Item missing searchHashtag data: {item}")
        
        print(f"Processed hashtag data: {hashtag_data}")
        return hashtag_data
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        return {}
