import pickle
import streamlit as st
from utils import clean_text_input, get_data, prep_data, make_plotly

# ----------------------------------------------------------------------------
# --- Sidebar Content ---
# ----------------------------------------------------------------------------
st.set_page_config(layout="wide")
with st.sidebar:
    with st.form(key='my_form'):
        ticker1 = st.text_input(label='Ticker 1', value='SOXL')
        ticker2 = st.text_input(label='Ticker 2', value='SOXX')
        st.caption("Use tickers compatible with Yahoo Finance")
        # st.markdown("""---""")
        holding_period = st.number_input(
            label='Holding Period (Years)',
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.5,
        )
        return_metric = st.radio(
            label='Return Metric (Y-axis)',
            options=[
                "Cumulative Percent Returns",
                "Annualized Percent Returns",
                "Cumulative Log Returns",
                "Annualized Log Returns",
            ],
            index=0,
        )
        plot_update = st.form_submit_button(label='Update Plot 📈')

# ----------------------------------------------------------------------------
# --- Data Preparation ---
# ----------------------------------------------------------------------------
# with open('toy_data.pkl', 'rb') as file:
#     data = pickle.load(file)
# ticker1 = 'SOXX'
# ticker2 = 'SOXL'
ticker1 = clean_text_input(ticker1)
ticker2 = clean_text_input(ticker2)
data = get_data(ticker1, ticker2)

prepped_data = prep_data(data, holding_period, return_metric, ticker1, ticker2)
fig = make_plotly(prepped_data, holding_period, return_metric, ticker1, ticker2)

win_rate = (prepped_data[f'{ticker1}_return'] > prepped_data[f'{ticker2}_return']).mean()
avg_ret1 = prepped_data[f'{ticker1}_return'].mean()
avg_ret2 = prepped_data[f'{ticker2}_return'].mean()

# ----------------------------------------------------------------------------
# --- Main Content ---
# ----------------------------------------------------------------------------
st.plotly_chart(fig)
st.markdown(f'{ticker1} beats {ticker2} in {100 * win_rate :.1f}% of {prepped_data.shape[0]} possible historical purchase dates, if these assets are held for {holding_period :.1f} years.')
if 'Percent' in return_metric:
    st.markdown(
        f"**Average Historical {return_metric}**"  + "  \n" +
        f"{ticker1}: {avg_ret1 :.1f}%" + "  \n" +
        f"{ticker2}: {avg_ret2 :.1f}%"
    )
else:
    st.markdown(
        f"**Average Historical {return_metric}**"  + "  \n" +
        f"{ticker1}: {avg_ret1 :.3f}" + "  \n" +
        f"{ticker2}: {avg_ret2 :.3f}"
    )
