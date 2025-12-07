import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def line_chart(df, x, y, color=None, title=None):
    fig = px.line(df, x=x, y=y, color=color, title=title)
    fig.update_layout(template="plotly_white")
    return fig

def bar_chart(df, x, y, color=None, title=None, orientation="v"):
    fig = px.bar(df, x=x, y=y, color=color, title=title, orientation=orientation)
    fig.update_layout(template="plotly_white")
    return fig

def candlestick_chart(df, datetime_col='date', open_col='open', high_col='high', low_col='low', close_col='close', title=None):
    df = df.sort_values(datetime_col)
    fig = go.Figure(data=[go.Candlestick(
        x=df[datetime_col],
        open=df[open_col],
        high=df[high_col],
        low=df[low_col],
        close=df[close_col],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    fig.update_layout(title=title or "Candlestick", xaxis_title=datetime_col, template="plotly_white")
    return fig

def histogram(df, column, nbins=50, title=None):
    fig = px.histogram(df, x=column, nbins=nbins, title=title)
    fig.update_layout(template="plotly_white")
    return fig

def pie_chart(df, names, values, title=None):
    fig = px.pie(df, names=names, values=values, title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template="plotly_white")
    return fig

def correlation_heatmap(df, numeric_only=True, title=None):
    if numeric_only:
        data = df.select_dtypes(include=[np.number])
    else:
        data = df.copy()
    corr = data.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu', title=title)
    fig.update_layout(template="plotly_white")
    return fig