# src/packet_analysis.py
import pandas as pd

def analyze_packets(df: pd.DataFrame):
    """Compute traffic stats and summaries."""
    if df.empty:
        return {}, pd.DataFrame()
    
    summary = {
        'total_packets': len(df),
        'unique_sources': df['src'].nunique(),
        'unique_destinations': df['dst'].nunique(),
        'avg_packet_size': round(df['length'].mean(), 2),
    }

    proto_summary = (
        df.groupby('proto')['length']
        .sum()
        .reset_index()
        .rename(columns={'length': 'total_bytes'})
        .sort_values(by='total_bytes', ascending=False)
    )

    return summary, proto_summary
