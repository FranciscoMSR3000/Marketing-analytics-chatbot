import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

def ingest_data(csv_path: str):
    df = pd.read_csv(csv_path)
    
    client = chromadb.PersistentClient(path="./chroma_db")
    
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    collection = client.get_or_create_collection(
        name="campaigns",
        embedding_function=ef
    )
    
    documents = []
    ids = []
    metadatas = []
    
    for _, row in df.iterrows():
        doc = f"""
        Campaign: {row['campaign_name']}
        Channel: {row['channel']}
        Type: {row['campaign_type']}
        Region: {row['region']}
        Objective: {row['objective']}
        Quarter: {row['quarter']}
        Impressions: {row['impressions']:,}
        Clicks: {row['clicks']:,}
        CTR: {row['ctr']}%
        Conversions: {row['conversions']:,}
        Conversion Rate: {row['conversion_rate']}%
        Spend: ${row['spend']:,.2f}
        Revenue: ${row['revenue']:,.2f}
        ROAS: {row['roas']}x
        Cost per conversion: ${row['cost_per_conversion']:,.2f}
        CPC: ${row['cpc']:,.2f}
        Engagement Rate: {row['engagement_rate']}%
        Likes: {row['likes']:,}
        Shares: {row['shares']:,}
        Comments: {row['comments']:,}
        Video Views: {row['video_views']:,}
        Bounce Rate: {row['bounce_rate']}%
        """
        documents.append(doc)
        ids.append(str(row['campaign_name']))
        metadatas.append({
            "channel": row['channel'],
            "quarter": row['quarter'],
            "region": row['region'],
            "campaign_type": row['campaign_type']
        })
    
    collection.upsert(documents=documents, ids=ids, metadatas=metadatas)
    print(f"✓ {len(documents)} campañas indexadas con métricas completas en ChromaDB")

if __name__ == "__main__":
    ingest_data("data/campaigns.csv")