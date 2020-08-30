import pandas as pd
import yfinance as yf
import ta
from ta import add_all_ta_features
from ta.utils import dropna
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
from datetime import date
import datetime
import io
yf.pdr_override()

st.set_option('deprecation.showfileUploaderEncoding', False)

st.write("""
# Technical Analysis Dashboard for any stock using **yfinance** and **ta**
""")

st.sidebar.header('User Input Parameters')

time = pd.to_datetime('now')
today = datetime.date.today()
def user_input_features():
    ticker = st.sidebar.text_input("Ticker", 'XRP-EUR')
    start_date = st.sidebar.text_input("Start Date", '2019-01-01')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    buying_price = st.sidebar.number_input("Buying Price", value=0.2000, step=0.0001)
    balance = st.sidebar.number_input("Balance", value=0.0, step=0.0001)
    file_buffer = st.sidebar.file_uploader("Choose a CSV file\n 2 columns are expected 'rate' and 'price'", type='csv')
    return ticker, start_date, end_date, buying_price, balance, file_buffer

symbol, start, end, buying_price, balance, file_buffer = user_input_features()

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# Read data
data = yf.download(symbol,start,end)
data.columns = map(str.lower, data.columns)
df = data.copy()
df = ta.add_all_ta_features(df, "open", "high", "low", "close", "volume", fillna=True)
df_trends = df[['close','trend_sma_fast','trend_sma_slow','trend_ema_fast','trend_ema_slow',]]
df_momentum = df[['momentum_rsi', 'momentum_roc', 'momentum_tsi', 'momentum_uo', 'momentum_stoch', 'momentum_stoch_signal', 'momentum_wr', 'momentum_ao', 'momentum_kama']]

# Price
daily_price = data.close.iloc[-1]
portfolio = daily_price * balance


st.title(f"Streamlit and {symbol} :euro:")

st.header("DF last rows")
st.dataframe(data.tail())
st.header("DF today's value")
st.markdown(f'Daily {symbol} price: {daily_price}')
st.markdown(f'{symbol} price per quantity: {portfolio}')
st.dataframe(data.tail(1))
st.code("""
time = pd.to_datetime('now')
today = datetime.date.today()
def user_input_features():
    ticker = st.sidebar.text_input("Ticker", 'XRP-EUR')
    start_date = st.sidebar.text_input("Start Date", '2019-01-01')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    return ticker, start_date, end_date

symbol, start, end = user_input_features()
# Read data
data = yf.download(symbol,start,end)
""", language="python")

# Uploaded file
if file_buffer is not None:
     file = pd.read_csv(file_buffer)
     st.write(file)


st.header(f"Candlestick for {symbol}")
# Initialize figure
fig = go.Figure()
# Candlestick
fig.add_trace(go.Candlestick(x=df.index,
                             open=df.open,
                             high=df.high,
                             low=df.low,
                             close=df.close,
                             visible=True,
                             name='Candlestick',))

fig.add_shape(
     # Line Horizontal
         type="line",
         x0=start,
         y0=buying_price,
         x1=end,
         y1=buying_price,
         line=dict(
             color="black",
             width=1.5,
             dash="dash",
         ),
         visible = True,
)

for column in df_trends.columns.to_list():
    fig.add_trace(
    go.Scatter(x = df_trends.index,y = df_trends[column],name = column,))
fig.update_layout(height=800,width=1000, xaxis_rangeslider_visible=False)
st.plotly_chart(fig)


st.header(f"Trends for {symbol}")
fig = go.Figure()
for column in df_trends.columns.to_list():
    fig.add_trace(
    go.Scatter(x = df_trends.index,y = df_trends[column],name = column,))
# Adapt buttons start
button_all = dict(label = 'All',method = 'update',args = [{'visible': df_trends.columns.isin(df_trends.columns),'title': 'All','showlegend':True,}])
def create_layout_button(column):
    return dict(label = column,
                method = 'update',
                args = [{'visible': df_trends.columns.isin([column]),
                        'title': column,
                        'showlegend': True,
                        }])
fig.update_layout(updatemenus=[go.layout.Updatemenu(active = 0, buttons = ([button_all]) + list(df_trends.columns.map(lambda column: create_layout_button(column))))],)
# Adapt buttons end
# add slider
fig.update_layout(
    xaxis=dict(
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ))
fig.update_layout(height=800,width=1000,updatemenus=[dict(direction="down",pad={"r": 10, "t": 10},showactive=True,x=0,xanchor="left",y=1.15,yanchor="top",)],)
# Candlestick
st.plotly_chart(fig)


# momentum indicators
st.header(f"Momentum Indicators for {symbol}")
trace=[]
Headers = df_momentum.columns.values.tolist()
for i in range(9):
    trace.append(go.Scatter(x=df_momentum.index, name=Headers[i], y=df_momentum[Headers[i]]))
fig = make_subplots(rows=9, cols=1)
for i in range(9):
     fig.append_trace(trace[i],i+1,1)
fig.update_layout(height=2200, width=1000)
st.plotly_chart(fig)
