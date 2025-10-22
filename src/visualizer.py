# src/visualizer.py
import plotly.express as px

def plot_protocol_distribution(proto_df):
    if proto_df is None or proto_df.empty:
        return None
    fig = px.pie(proto_df, values='total_bytes', names='protocol', title='Protocol Distribution')
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig

def plot_bandwidth_over_time(df):
    if df is None or df.empty:
        return None
    # sum lengths by timestamp for a simple bandwidth/time series
    time_series = df.groupby('timestamp')['length'].sum().reset_index()
    fig = px.line(time_series, x='timestamp', y='length', title='Bytes over Time')
    fig.update_layout(xaxis_title='Time', yaxis_title='Total Bytes', margin=dict(l=10, r=10, t=40, b=10))
    return fig
