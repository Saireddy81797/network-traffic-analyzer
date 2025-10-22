# src/packet_analysis.py
import pandas as pd

def analyze_packets(df: pd.DataFrame):
    if df is None or df.empty:
        summary = {"total_packets": 0, "unique_sources": 0, "unique_destinations": 0, "avg_packet_size": 0}
        proto_summary = pd.DataFrame(columns=["protocol", "total_bytes"])
        return summary, proto_summary

    summary = {
        "total_packets": int(len(df)),
        "unique_sources": int(df['src_ip'].nunique()),
        "unique_destinations": int(df['dst_ip'].nunique()),
        "avg_packet_size": round(float(df['length'].mean()), 2)
    }

    proto_summary = (
        df.groupby('protocol')['length']
          .sum()
          .reset_index()
          .rename(columns={'length': 'total_bytes'})
          .sort_values(by='total_bytes', ascending=False)
    )

    return summary, proto_summary
