# Streamlit-Dashboard-Ticker_Technical_Analysis
Streamlit Dashbaord returning technical indicators for a given ticker (yfinance/ta)

##### Running: `streamlit run https://raw.githubusercontent.com/poltys/Streamlit-Dashboard-Ticker_Technical_Analysis/master/app.py`
![](https://github.com/poltys/Streamlit-Dashboard-Ticker_Technical_Analysis/blob/master/extra/streamlit-app-2020-08-30-12-08-43.gif)

#### To Do
- [ ] Add user inputs
  - [X] Buying Price & Plotly Shape
    - [ ] Fix number_input 
  - [X] Create button to upload portfio detail and calcul global buying price / weighted av.
    - [X] Add logic to calculate values
    - [ ] Create a templated csv to download [work-around](https://discuss.streamlit.io/t/file-download-workaround-added-to-awesome-streamlit-org/1244)
  - [X] Portfolio Size
  - [X] T Price
  - [X] Add Dynamic Indicator
- [ ] Add means
- [ ] Dynamically generate annotations
- [ ] Add technical indicators
- [ ] Identify how to create pages with streamlit 
- [ ] Improve layout integration between streamlit and plotly
- [ ] Add trained ML predictive model 
- [ ] Deploy on Heroku
