import praw
import pandas as pd

# Reddit API bağlantısı
reddit = praw.Reddit(
    client_id="mHCy7dZiQYfcwlnQJCgggA",
    client_secret="e_oGkJjAt1FCanWYRlnvXVYh2gvVaQ",
    user_agent="script:konusarak-ogren:v1.0 (by /u/authomate-with-python)"
)

# İşlenecek subreddit listesi (csv dosya adlarıyla aynı)
subreddits = ["EnglishLearning", "duolingo", "languagelearning"]

for subreddit in subreddits:
    csv_file = f"{subreddit}_100posts.csv"
    print(f"🔍 İşleniyor: {csv_file}")

    try:
        # CSV'den 10–30. satırlar arası linkleri al
        df_links = pd.read_csv(csv_file).iloc[10:30]
        post_data = []

        for idx, row in df_links.iterrows():
            url = row[1]  # 2. sütundaki Reddit linki

            try:
                submission = reddit.submission(url=url)
                submission.comments.replace_more(limit=None)
                all_comments = submission.comments.list()

                comment_bodies = [comment.body.strip() for comment in all_comments[:100]]
                joined_comments = "\n---\n".join(comment_bodies)

                post_data.append({
                    "original_link": url,
                    "praw_title": submission.title,
                    "num_comments": len(all_comments),
                    "selftext": submission.selftext.strip(),
                    "all_comments": joined_comments
                })

            except Exception as e:
                print(f"Hata oluştu: {url} -> {e}")
                continue

        # Excel dosyasına yaz
        df_output = pd.DataFrame(post_data)
        output_filename = f"{subreddit}_details.xlsx"
        df_output.to_excel(output_filename, index=False, engine='openpyxl')
        print(f"✅ Kaydedildi: {output_filename}\n")

    except Exception as e:
        print(f"{csv_file} dosyasında sorun var: {e}")
