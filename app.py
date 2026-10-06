import json
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Web Scraping ETL Assignment",
    page_icon="📚",
    layout="wide",
)

st.title("Web Scraping ETL Assignment")
st.write(
    "Python web scraping and data-processing pipeline using "
    "Books to Scrape and Quotes to Scrape."
)

summary_path = Path("output/summary_report.json")
csv_path = Path("output/final_dataset.csv")

if summary_path.exists() and csv_path.exists():
    with open(summary_path, "r", encoding="utf-8") as file:
        summary = json.load(file)

    df = pd.read_csv(csv_path)

    st.subheader("Scraping Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Books", summary["sources"]["Books to Scrape"]["final_records"])
    col2.metric("Quotes", summary["sources"]["Quotes to Scrape"]["final_records"])
    col3.metric("Total Records", len(df))

    st.subheader("Final Dataset")

    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Final Dataset",
        data=csv_data,
        file_name="final_dataset.csv",
        mime="text/csv",
    )

    st.subheader("Pipeline")

    st.write(
        "Scraping → Cleaning → Validation → Deduplication → Consolidation → Output"
    )

else:
    st.error(
        "Output files were not found. Please run the scraping pipeline first."
    )