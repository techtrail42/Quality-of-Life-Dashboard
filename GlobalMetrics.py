import streamlit as st
import pandas as pd
import plotly.express as px
from utils import custom_navigation

def app():
    # --- 1. Data Loading ---
    df = pd.read_excel("final_data.xlsx")
    df.columns = df.columns.str.strip().str.title()  # Standardize column names

    # Define relevant indicators
    indicators = [
        "Purchasing Power Value", "Safety Value", "Health Care Value", "Climate Value",
        "Cost Of Living Value", "Property Price To Income Value", "Pollution Value",
        "Traffic Commute Time Value", "Quality Of Life Value"
    ]

    # Map indicators to their interpretation
    indicator_polarity = {
        "Quality Of Life Value": "higher_is_better",
        "Purchasing Power Value": "higher_is_better",
        "Cost Of Living Value": "lower_is_better",
        "Property Price To Income Value": "lower_is_better",
        "Safety Value": "higher_is_better",
        "Health Care Value": "higher_is_better",
        "Pollution Value": "lower_is_better",
        "Traffic Commute Time Value": "lower_is_better",
        "Climate Value": "higher_is_better"
    }

    color_scales = {
        "higher_is_better": "RdYlGn",
        "lower_is_better": "RdYlGn_r"
    }

    # Streamlit page configuration
    st.title("Global Metrics Dashboard")
    st.markdown("Explore global statistics and compare quality-of-life metrics across continents.")
    
    with st.expander("ℹ️ How to Navigate This Page", expanded=False):
        st.markdown("""
        <strong><br>🔍 Dashboard Features and How to Use:</strong>
        
        - **Hover over charts** to see detailed values in tooltips for better insights.<br>
        - **Use sidebar filters** to customize the view:
            - Select **one or multiple continents** in Global View.
            - Focus on a **single continent** to analyze country-specific data.<br>
        - **Choose an Indicator** to explore key quality-of-life metrics, such as Safety, Healthcare, and Cost of Living.<br>
        - **Switch between Global and Single Continent View**:
            - **Global View** provides a high-level comparison of continents.
            - **Single Continent View** focuses on detailed country-level insights.<br><br>

        <strong><br>📊 Interactive Visualizations:</strong>
        
        - **Bar Chart**: Compares the average indicator values across continents.<br>
        - **Sunburst Chart**: Visualizes the hierarchical distribution of indicators across continents and countries.<br>
        - **Scatter Plot (Single Continent View)**: Shows country-level variations within a selected continent.<br><br>

        <strong><br>💡 Tips for Effective Analysis:</strong>
        
        - **Select “All Indicators”** to get a comprehensive view of how different regions compare.<br>
        - **Color-coded insights**:
            - 🟢 Green represents better performance.
            - 🔴 Red indicates areas for improvement.<br>
        - **Explore trends** using the various chart types to analyze the distribution and variations across regions.<br><br>
        """, unsafe_allow_html=True)

    # --- 2. Sidebar Filters ---
    with st.sidebar:
        st.sidebar.header("Filters")
        st.sidebar.markdown("""
        <style>
            .sidebar-title {
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        </style>
        <p class="sidebar-title">🔍 Select Indicator</p>
        """, unsafe_allow_html=True)
        
        # Group indicators by category for better organization
        indicator_groups = {
            "Economic": ["Purchasing Power Value", "Cost Of Living Value", "Property Price To Income Value"],
            "Lifestyle": ["Quality Of Life Value", "Safety Value", "Traffic Commute Time Value", "Health Care Value"],
            "Environment": ["Pollution Value", "Climate Value"]
        }
        
        # Select indicator group first
        selected_group = st.radio(
            "Select indicator category:",
            options=list(indicator_groups.keys()),
            horizontal=True
        )
        
        # Then select specific indicator from that group
        group_indicators = indicator_groups[selected_group]
        selected_indicator = st.selectbox("📊 Choose a Quality of Life Indicator", group_indicators)
        
        # Allow user to either select multiple continents or focus on a single one
        continent_mode = st.radio("Display Mode", ["Global View", "Single Continent View"])
        
        if continent_mode == "Global View":
            selected_continents = st.multiselect("Select Continents", df["Continent"].unique(), default=df["Continent"].unique())
            filtered_df = df[df["Continent"].isin(selected_continents)].dropna(subset=[selected_indicator])
            df_continent = filtered_df.groupby("Continent")[selected_indicator].mean().reset_index()
        else:
            selected_continent = st.selectbox("Select a Continent", df["Continent"].unique())
            filtered_df = df[df["Continent"] == selected_continent].dropna(subset=[selected_indicator])
            df_country = filtered_df.groupby(["Continent", "Country"])[selected_indicator].mean().reset_index()

    if filtered_df.empty:
        st.warning("No data available for the selected filters. Please adjust your selections.")
        st.stop()

    # --- 4. Display Statistics ---
    st.subheader(f"Statistics for {selected_indicator}")
    
    # Color scheme info (optional)
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ Indicator Information")
    st.sidebar.info("🎨 **Color Scheme:** Green (better) to Red (worse)")

    
    if continent_mode == "Global View":
        grouped_data = df_continent
        stat_label = "Continent"
    else:
        grouped_data = df_country
        stat_label = "Country"

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(f"Average {stat_label}", f"{grouped_data[selected_indicator].mean():.2f}")
    col2.metric(f"Median {stat_label}", f"{grouped_data[selected_indicator].median():.2f}")
    col3.metric(f"Std Dev {stat_label}", f"{grouped_data[selected_indicator].std():.2f}")
    col4.metric(f"Min {stat_label}", f"{grouped_data[selected_indicator].min():.2f}")
    col5.metric(f"Max {stat_label}", f"{grouped_data[selected_indicator].max():.2f}")
    # Add some space
    st.markdown("<br><br>", unsafe_allow_html=True)
    # --- 5. Bar Graph (Only in Global View) ---
    if continent_mode == "Global View":
        st.subheader(f"{selected_indicator} by Continent")
        fig = px.bar(
            df_continent, x="Continent", y=selected_indicator, color=selected_indicator,
            color_continuous_scale=color_scales[indicator_polarity[selected_indicator]],
            title=f"Average {selected_indicator} Across Continents"
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- 6. Sunburst Chart ---
    

    if continent_mode == "Global View":
        # Sunburst chart only for continents
        st.subheader(f"Sunburst Chart: {selected_indicator} Distribution")
        sunburst_fig = px.sunburst(
            df_continent,
            path=["Continent"],  # Show only continents
            values=selected_indicator,
            color=selected_indicator,
            color_continuous_scale=color_scales[indicator_polarity[selected_indicator]],
            title=f"{selected_indicator} Distribution by Continent"
            
        )
        st.plotly_chart(sunburst_fig, use_container_width=True)
    else:
        # Scatter Plot for a Single Continent
        st.subheader(f"Scatter Chart: {selected_indicator} Distribution")
        scatter_fig = px.scatter(
            filtered_df,
            x="Country",
            y=selected_indicator,
            color=selected_indicator,
            size=selected_indicator,
            hover_name="Country",
            title=f"{selected_indicator} Across {selected_continent}",
            color_continuous_scale=color_scales[indicator_polarity[selected_indicator]]
        )

        # Update layout to increase width and adjust height if necessary
        scatter_fig.update_layout(
            width=1200,  # Increase width of the chart
            height=600,  # Optional: increase height if you want
            title=f"{selected_indicator} Across {selected_continent}",
            xaxis_title="Country",
            yaxis_title=selected_indicator,
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(scatter_fig, use_container_width=True)

        # Sunburst chart for selected continent (continent → country)
        st.subheader(f"Sunburst Chart: {selected_indicator} Distribution")
        sunburst_fig = px.sunburst(
            df_country,
            path=["Continent", "Country"],  # Continent → Country hierarchy
            values=selected_indicator,
            color=selected_indicator,
            color_continuous_scale=color_scales[indicator_polarity[selected_indicator]],
            title=f"{selected_indicator} Distribution in {selected_continent}"
        )

        st.plotly_chart(sunburst_fig, use_container_width=True)

   

 # --- Footer ---
    st.divider()

    st.markdown("""
        <div style="text-align: center; color: #888;">
            <p>Data source: Numbeo Quality of Life Indices | Dashboard created with Streamlit</p>
            <p style="text-align: center; color: #888;">Team Visionaries</p>
        </div>
    """, unsafe_allow_html=True)