# src/utils.py
import pandas as pd

def filter_by_protocol(df: pd.DataFrame, protocol: str):
    if df.empty:
        return df
    if protocol == "All":
        return df
    return df[df["protocol"] == protocol]

def filter_by_ip(df: pd.DataFrame, ip_address: str):
    if df.empty or not ip_address:
        return df
    return df[(df["src_ip"] == ip_address) | (df["dst_ip"] == ip_address)]
