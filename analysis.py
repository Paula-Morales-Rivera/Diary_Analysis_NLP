from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st
import pandas as pd
import plotly.express as px
import glob
from datetime import datetime


# Retrieves entries using wildcard '*' pattern
def load_diary():
    entries = []
    for name in glob.glob('diary\*.txt'):
        entries.append(name)
    return sorted(entries)

diary = load_diary()

# Sets up sentiment analysis tool and lists
analyzer = SentimentIntensityAnalyzer()
positive_values = []
negative_values = []
compound_values = []
dates= []

overall = { 'date': dates,
    'positive': positive_values,
    'negative': negative_values,
    'compound': compound_values}
date_format = "%Y-%m-%d"

# Reads and analyzes the diary entry
for diary_path in diary:
    # Converts string to datetime obj
    file_date = diary_path.strip(r"diary\"").strip(".txt")
    date_obj = datetime.strptime(file_date, "%Y-%m-%d")

    # Formats date to format: 'Jan 01, 2003'
    dt = date_obj.strftime("%b %d, %Y")
    with open(diary_path) as file:
        entry = file.read()
        score = analyzer.polarity_scores(entry)
        positive_values.append(score["pos"])
        negative_values.append(score["neg"])
        compound_values.append(score["compound"])
        dates.append(dt)


st.header("Moods for Diary", divider=True)

st.subheader("Comparison of Sentiment Scores")
# Creates area plot using dictionary
fig = px.area(overall,  x='date',  # The x-axis is 'date'
    y=['positive', 'negative', 'compound'],  # Values to plot in the area chart
    labels={'date': 'DATE', 'value': 'SENTIMENT SCORE'},
    color_discrete_map={
        'positive': '#097969',
        'negative': '#800080',
        'compound': '#87CEEB'
    })


# Displays area chart and file names
col1, col2 = st.columns([3, 1])
with col1:
    st.plotly_chart(fig)
with col2:
    st.markdown("""
            <style>
                .stDataFrame tbody td {
                    font-size: 50px;
                }
            </style>
        """, unsafe_allow_html=True)

    df = pd.DataFrame({"diary entries": diary})
    st.markdown(df.to_html(classes='table table-bordered table-hover', index=False), unsafe_allow_html=True)


# Creates line plots and modifies color
st.subheader("Overall Days")
fig1 = px.line(x=dates, y=compound_values, labels={"x": "DATE", "y": "COMPOUND"}, range_y=[-1,1])
fig1.update_traces(line_color='#87CEEB', line_width=5)
st.plotly_chart(fig1)

st.subheader("Positive Days")
fig2 = px.line(x=dates, y=positive_values, labels={"x": "DATE", "y": "POSITIVE"}, range_y=[-1,1])
fig2.update_traces(line_color='#097969', line_width=5)
st.plotly_chart(fig2)

st.subheader("Negative Days")
fig3 = px.line(x=dates, y=negative_values, labels={"x": "DATE", "y": "NEGATIVE"}, range_y=[-1,1])
fig3.update_traces(line_color='#800080', line_width=5)
st.plotly_chart(fig3)

