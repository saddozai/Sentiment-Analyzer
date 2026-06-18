import streamlit as st
from textblob import TextBlob
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Sentiment Analyzer")
st.title("Sentiment Analyzer")
st.markdown("Upload your CSV file and analyze sentiments instantly.")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"File uploaded successfully! {len(df)} rows found.")
    st.markdown("---")

    columns = df.columns.tolist()
    selected_column = st.selectbox("Which column contains the review text?", columns)

    if selected_column:
        st.markdown("---")
        st.subheader("Preview of your data")
        st.dataframe(df[[selected_column]].head(10))

        st.markdown("---")
        st.subheader("Analyzing... please wait")

        def get_label(score):
            if score > 0.1:
                return "Positive"
            elif score < -0.1:
                return "Negative"
            else:
                return "Neutral"

        df['polarity'] = df[selected_column].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity
        )

        df['sentiment'] = df['polarity'].apply(get_label)

        st.success("Done! Analysis complete ✅")
        st.markdown("---")
        st.subheader("Results")

        total = len(df)
        positive = len(df[df['sentiment'] == 'Positive'])
        negative = len(df[df['sentiment'] == 'Negative'])
        neutral = len(df[df['sentiment'] == 'Neutral'])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Positive 😊", positive)
        with col2:
            st.metric("Negative 😞", negative)
        with col3:
            st.metric("Neutral 😐", neutral)
        st.markdown("---")
        st.subheader("Sentiment Breakdown")

        fig = go.Figure(data=[go.Pie(
            labels=['Positive', 'Negative', 'Neutral'],
            values=[positive, negative, neutral],
            hole=0.4,
            marker_colors=['#1D9E75', '#D85A30', '#888780']
        )])

        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")
        st.subheader("Most Positive Tweet 😊")
        most_positive = df.loc[df['polarity'].idxmax(), selected_column]
        st.success(most_positive)

        st.markdown("---")
        st.subheader("Most Negative Tweet 😞")
        most_negative = df.loc[df['polarity'].idxmin(), selected_column]
        st.error(most_negative)
