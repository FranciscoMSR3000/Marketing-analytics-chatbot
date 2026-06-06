import pandas as pd
import numpy as np

np.random.seed(42)
n = 200

channels = [
    "Instagram", "Google Ads", "Email", "TikTok", "LinkedIn",
    "YouTube", "Pinterest", "X (Twitter)", "Facebook", "Snapchat"
]

campaign_types = ["Brand Awareness", "Retargeting", "Lead Gen", "Conversion", "Engagement"]
regions = ["LATAM", "North America", "Europe", "APAC"]
objectives = ["Traffic", "Sales", "Awareness", "Leads", "Retention"]

df = pd.DataFrame({
    "campaign_name": [f"Campaign_{i:03d}" for i in range(n)],
    "channel": np.random.choice(channels, n),
    "campaign_type": np.random.choice(campaign_types, n),
    "region": np.random.choice(regions, n),
    "objective": np.random.choice(objectives, n),
    "quarter": np.random.choice(["Q1_2024", "Q2_2024", "Q3_2024", "Q4_2024"], n),
    "impressions": np.random.randint(10000, 1000000, n),
    "clicks": np.random.randint(500, 50000, n),
    "conversions": np.random.randint(50, 5000, n),
    "spend": np.random.uniform(1000, 100000, n).round(2),
    "revenue": np.random.uniform(5000, 500000, n).round(2),
    "likes": np.random.randint(100, 50000, n),
    "shares": np.random.randint(10, 10000, n),
    "comments": np.random.randint(5, 5000, n),
    "video_views": np.random.randint(0, 200000, n),
    "bounce_rate": np.random.uniform(20, 80, n).round(2),
})

df["ctr"] = (df["clicks"] / df["impressions"] * 100).round(2)
df["cpc"] = (df["spend"] / df["clicks"]).round(2)
df["cost_per_conversion"] = (df["spend"] / df["conversions"]).round(2)
df["roas"] = (df["revenue"] / df["spend"]).round(2)
df["engagement_rate"] = ((df["likes"] + df["shares"] + df["comments"]) / df["impressions"] * 100).round(2)
df["conversion_rate"] = (df["conversions"] / df["clicks"] * 100).round(2)

df.to_csv("data/campaigns.csv", index=False)
print(f"✓ {n} campañas generadas con {len(df.columns)} métricas en data/campaigns.csv")