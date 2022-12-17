import re
import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# ----------------------------------------------------------------------------
# --- Constants ---
# ----------------------------------------------------------------------------
PCT_HOVERTEMPLATE = '<br>'.join([
    '$%{customdata[0]:.2f} → $%{customdata[1]:.2f}',
    '%{customdata[2]} → %{customdata[3]}',
    '<b>Return: %{y:.2f}%</b>',
])
LOG_HOVERTEMPLATE = '<br>'.join([
    '$%{customdata[0]:.2f} → $%{customdata[1]:.2f}',
    '%{customdata[2]} → %{customdata[3]}',
    '<b>Return: %{y:.4f}</b>',
])

# ----------------------------------------------------------------------------
# --- External Functions ---
# ----------------------------------------------------------------------------
def clean_text_input(text_input: str) -> str:
    '''Remove whitespaces and capitalize text input'''
    cleaned = re.sub(r'\s+', '', text_input)
    cleaned = cleaned.upper()
    return cleaned


@st.cache
def get_data(ticker1: str, ticker2: str) -> pd.DataFrame:
    '''Call yfinance API to get data, given some tickers'''
    data = yf.Tickers(f'{ticker1} {ticker2}').download(
        period='max',
        actions=False,
        auto_adjust=True,
    )
    assert len(yf.shared._ERRORS) == 0, f'yfinance error: {yf.shared._ERRORS}'

    return data


def prep_data(
    data: pd.DataFrame,
    holding_period: float,
    return_metric: str,
    ticker1: str,
    ticker2: str,
) -> pd.DataFrame:
    '''Prepare data with proper columns for plotting'''
    lesser_data_ticker = data['Close'].isna().sum().idxmax()
    lesser_data_startdate = data['Close'].dropna().index[0]
    lesser_data_enddate = data['Close'].dropna().index[-1]
    lesser_data_yeardelta = (lesser_data_enddate - lesser_data_startdate).days / 365
    assert lesser_data_yeardelta > holding_period, (
        f'Ticker "{lesser_data_ticker}" only has {lesser_data_yeardelta :.2f}'
        ' years worth of data. Choose a smaller holding period.'
    )

    df = pd.DataFrame(index = data.index)
    df['startdate'] = data.index
    unmatched_enddates = data.index + np.timedelta64(int(365 * holding_period), 'D')
    df['enddate'] = df.index[df.index.get_indexer(unmatched_enddates, method='nearest')]

    for ticker in [ticker1, ticker2]:
        df[f'{ticker}_startprice'] = data['Close'][ticker]
        df[f'{ticker}_endprice'] = df.loc[df['enddate']][f'{ticker}_startprice'].to_numpy()

        ratio = df[f'{ticker}_endprice'] / df[f'{ticker}_startprice']
        if return_metric == "Cumulative Percent Returns":
            df[f'{ticker}_return'] = 100 * (ratio - 1)
        elif return_metric == "Annualized Percent Returns":
            df[f'{ticker}_return'] = 100 * (ratio ** (1 / holding_period) - 1)
        elif return_metric == "Cumulative Log Returns":
            df[f'{ticker}_return'] = np.log(ratio)
        else:  # return_metric == "Annualized Log Returns"
            df[f'{ticker}_return'] = np.log(ratio) / holding_period

    last_valid_start = df[df['enddate'] == df.index[-1]].index[0]
    df = df.loc[:last_valid_start].dropna()

    return df


def make_plotly(
        prepped_data: pd.DataFrame,
        holding_period: float,
        return_metric: str,
        ticker1: str,
        ticker2: str
) -> go.Figure:
    '''Create a plotly figure from prepped data'''
    hovertemplate = PCT_HOVERTEMPLATE if 'Percent' in return_metric else LOG_HOVERTEMPLATE

    fig = go.Figure()
    for ticker in [ticker1, ticker2]:
        fig.add_trace(go.Scatter(
            name=ticker,
            x=prepped_data['startdate'],
            y=prepped_data[f'{ticker}_return'],
            customdata=np.stack((
                prepped_data[f'{ticker}_startprice'],
                prepped_data[f'{ticker}_endprice'],
                prepped_data['startdate'].dt.strftime('%b %d, %Y'),
                prepped_data['enddate'].dt.strftime('%b %d, %Y'),
            ), axis=-1),
            hovertemplate=hovertemplate,
        ))

    if 'Percent' in return_metric:
        fig.update_yaxes(ticksuffix='%')

    fig.update_layout(
        title=f'{holding_period :.1f} Year Forward Returns ({ticker1} vs. {ticker2})',
        xaxis_title="Start Date",
        yaxis_title=return_metric,
        hovermode="x unified",
        font=dict(size=16),
        width=800, height=600,
    )

    return fig
