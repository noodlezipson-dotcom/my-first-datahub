import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Video Tool Selector 🎬",
    page_icon="🎥",
    layout="wide"
)

st.title("🎬 AI Video Tool Selector")
st.markdown("Find the best AI video tool tailored to your needs 🚀")

# -----------------------------
# Data
# -----------------------------
data = [
    ["Runway Gen-2", "Text-to-Video", "Freemium", 4.6, "Advanced generative video AI", 12, "https://runwayml.com"],
    ["Pika Labs", "Text-to-Video", "Free", 4.4, "Discord-based video generation", 0, "https://pika.art"],
    ["HeyGen", "Avatar Video", "Paid", 4.7, "AI avatars & lip-sync", 29, "https://heygen.com"],
    ["CapCut AI", "Video Editing", "Free", 4.5, "AI editing tools + templates", 0, "https://capcut.com"],
    ["Synthesia", "Avatar Video", "Paid", 4.8, "Corporate AI video presenter", 30, "https://synthesia.io"],
    ["Invideo AI", "Text-to-Video", "Freemium", 4.3, "Script to video automation", 20, "https://invideo.io"],
    ["Lensa AI Video", "Creative Video", "Freemium", 4.1, "AI stylized video effects", 10, "https://lensa-ai.com"],
    ["Kaiber", "Creative Video", "Freemium", 4.2, "Music-driven AI visuals", 15, "https://kaiber.ai"]
]

columns = ["Tool Name", "Best For", "Pricing", "Rating", "Key Feature", "Monthly Price", "Link"]
df = pd.DataFrame(data, columns=columns)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filter Tools")

price_filter = st.sidebar.multiselect(
    "💰 Price Range",
    options=df["Pricing"].unique(),
    default=df["Pricing"].unique()
)

best_for_filter = st.sidebar.multiselect(
    "🎯 Best For",
    options=df["Best For"].unique(),
    default=df["Best For"].unique()
)

rating_filter = st.sidebar.slider(
    "⭐ Minimum Rating",
    min_value=1.0,
    max_value=5.0,
    value=3.5,
    step=0.1
)

search_query = st.sidebar.text_input("🔎 Search by name or feature")

# -----------------------------
# Filtering Logic
# -----------------------------
filtered_df = df[
    (df["Pricing"].isin(price_filter)) &
    (df["Best For"].isin(best_for_filter)) &
    (df["Rating"] >= rating_filter)
]

if search_query:
    filtered_df = filtered_df[
        filtered_df["Tool Name"].str.contains(search_query, case=False) |
        filtered_df["Key Feature"].str.contains(search_query, case=False)
    ]

# -----------------------------
# Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

total_tools = len(filtered_df)
avg_rating = round(filtered_df["Rating"].mean(), 2) if total_tools > 0 else 0

paid_tools = filtered_df[filtered_df["Pricing"] == "Paid"]
cheapest_paid = paid_tools["Monthly Price"].min() if not paid_tools.empty else 0

col1.metric("🧰 Total Tools", total_tools)
col2.metric("⭐ Average Rating", avg_rating)
col3.metric("💵 Cheapest Paid Tool ($)", cheapest_paid)

st.markdown("---")

# -----------------------------
# Table Display
# -----------------------------
st.subheader("📊 AI Video Tools Comparison")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

# -----------------------------
# Charts
# -----------------------------
col1, col2 = st.columns(2)

# Bar Chart: Avg Rating per Pricing
pricing_avg = df.groupby("Pricing")["Rating"].mean().reset_index()

fig_bar = px.bar(
    pricing_avg,
    x="Pricing",
    y="Rating",
    color="Pricing",
    title="⭐ Average Rating by Pricing Type",
    text_auto=True
)

col1.plotly_chart(fig_bar, use_container_width=True)

# Scatter Plot: Price vs Rating
fig_scatter = px.scatter(
    df,
    x="Monthly Price",
    y="Rating",
    color="Pricing",
    size="Rating",
    hover_name="Tool Name",
    title="💸 Price vs ⭐ Rating"
)

col2.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("✨ Built with Streamlit | AI Video Tool Discovery Dashboard")
