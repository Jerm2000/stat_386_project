import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from analysis import (
    load_combined,
    prepare_data,
    longest_vs_avg_distance,
    correlation_table,
    barrel_power_table,
    workload_vs_distance,
    find_outliers,
    plot_max_vs_avg_distance,
    plot_launch_speed_vs_distance,
    plot_barrel_percent_vs_distance,
    plot_hr_count_vs_distance
)

st.set_page_config(page_title="MLB Statcast Hitter Leaders")

st.title("MLB Statcast Hitter Leaders - Data Explorer")


# load and prepare dataset
st.header("Dataset Preview")

raw = load_combined()
st.write("Raw Dataset:", raw.head())

min_hr = st.slider("Minimum HR to include", 0, 50, 5)

df = prepare_data(raw, min_hr=min_hr)

st.write(f"Filtered dataset (HR >= {min_hr}):", df)


# longest vs average distance
st.header("Longest Home Runs vs Average Home Run Distance")

top_n = st.slider("Top N players by max Home Run distance", 5, 50, 20)

st.dataframe(longest_vs_avg_distance(df, n=top_n))

fig1 = plot_max_vs_avg_distance(df)
st.pyplot(fig1)


# correlation table
st.header("Correlation Between Metrics")

st.dataframe(correlation_table(df))


# barrel power table
st.header("Barrel Percentage and Power Indicators")

top_barrel_n = st.slider("Top N players by Barrel %", 5, 50, 20)

st.dataframe(barrel_power_table(df, n=top_barrel_n))

fig2 = plot_barrel_percent_vs_distance(df)
st.pyplot(fig2)


# exit velocity vs distance
st.header("Exit velocity vs Home Run Distance")

fig3 = plot_launch_speed_vs_distance(df)
st.pyplot(fig3)

# HR count vs average distance
st.header("Workload vs Average Home Run Distance")

fig4 = plot_hr_count_vs_distance(df)
st.pyplot(fig4)

# outliers
st.header("Outlier Detection")

outliers = find_outliers(df)
st.write("Detected Outliers (Z-score):")
st.dataframe(outliers)
