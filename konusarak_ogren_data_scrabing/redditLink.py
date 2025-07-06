import requests
import pandas as pd
import time

def get_reddit_posts(subreddit, total_limit=100):
    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = f"https://www.reddit.com/r/{subreddit}/new/.json"

    posts = []
    after = None

    while len(posts) < total_limit:
        params = {
            #spam saymasın diye 25 er kere gönderdim
            "limit": 25,
            "after": after
        }

        response = requests.get(base_url, headers=headers, params=params)
        #hata alırsam kodu patlatmasın döngüyü bitirsin
        if response.status_code != 200:
            print(f"[{subreddit}] Hata kodu: {response.status_code}")
            break
        
        data = response.json()
        children = data["data"]["children"]

        if not children:
            break

        for post in children:
            post_data = post["data"]
            posts.append({
                "title": post_data.get("title", ""),
                "link": "https://www.reddit.com" + post_data.get("permalink", ""),
                "num_comments": post_data.get("num_comments", 0)
            })

            if len(posts) >= total_limit:
                break

        after = data["data"].get("after")
        if not after:
            break

        time.sleep(1)  # Spam önlemek için yazdım.

    return posts

# Subreddit listesiyle döngü
subreddits = ["languagelearning", "EnglishLearning", "duolingo"]

for subreddit in subreddits:
    print(f"Subreddit işleniyor: {subreddit}")
    post_list = get_reddit_posts(subreddit, total_limit=100)
    
    df = pd.DataFrame(post_list)
    df_sorted = df.sort_values("num_comments", ascending=False)

    filename = f"{subreddit}_100posts.csv"
    
    df_sorted.to_csv(filename, index=False, encoding="utf-8")
    print(f"{filename} dosyası oluşturuldu ({len(df)} gönderi).\n")

print("Tüm subreddit verileri kaydedildi.")
