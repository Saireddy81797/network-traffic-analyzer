# src/visualizer.py
import plotly.express as px

def plot_protocol_distribution(proto_df):
    if proto_df.empty:
        return None
    fig = px.pie(proto_df, values='total_bytes', names='proto', title='Protocol Distribution')
    fig.update_traces(textinfo='percent+label')
    return fig
