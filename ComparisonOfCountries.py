import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from utils import custom_navigation


def app():
    # Load Data
    df = pd.read_excel("final_data.xlsx")

    # Standardize column names
    df.columns = df.columns.str.strip().str.title()

    # Identify numeric columns for aggregation
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

    # Compute mean values for each continent (without modifying country-level data)
    df_continent = df.groupby("Continent")[numeric_columns].mean().reset_index()

    with st.container():
        col1, col2 = st.columns([5, 1])
        with col1:
            st.title('Quality of Life Indicator Comparison')
            st.markdown('Compare quality of life metrics between countries or continents.')
    
    # Add help expander here
    with st.expander("ℹ️ How to Navigate This Page", expanded=False):
        st.markdown("""
            <strong><br>🔍 Dashboard Features and How to Use:</strong>
                    
            - **Hover over the charts** to view detailed values in interactive tooltips.<br>
            - **Zoom in/out on the radar chart** by selecting the region to zoom in on, and double-click to zoom out.<br>
            - **Change filters** in the sidebar to compare data for different countries, continents, or indicators.<br>
            - **Explore diverse indicators** such as safety, healthcare, purchasing power, and cost of living by selecting from the dropdown menus.<br>
            - **Compare countries or continents** by selecting them in the sidebar to visualize the key differences in quality of life indicators.<br>
            
            <strong><br>📊 Interactive Visualizations:</strong>
                    
            - **Bar charts** provide a side-by-side comparison of the selected indicator values for the chosen entities.<br>
            - **Bubble chart** illustrates the relative sizes of indicators across entities, with the bubble size representing magnitude.<br>
            - **Radar chart** visualizes the strengths and weaknesses of different entities, comparing them across various dimensions in a circular format.<br><br>
            
            <strong><br>💡 Tips for Effective Analysis:</strong>
            - **Select "All Indicators"** to get an overview of how countries or continents compare across multiple dimensions.<br>
            - **Select individual indicators** to zoom in on specific metrics like cost of living, safety, or health care for a deeper comparison.<br>
            - **Color-coded insights**:
            - 🟢 Green represents better performance.
            - 🔴 Red indicates areas for improvement.<br>
            - **Use the radar chart for holistic comparison**, where you can see the performance across multiple indicators in one view.<br><br>
            <strong>""", unsafe_allow_html=True)

    with st.sidebar:
        st.header('Filters')
        
        st.subheader("🔍 Select Analysis Criteria")
        compare_type = st.radio(
            "Compare By:",
            ["Countries", "Continents"],
            index=0,
            help="Choose whether to compare two countries or two continents."
        )

        # Define indicator groups the same way as in the world map page
        indicator_groups = {
            "Economic": ["Purchasing Power", "Cost Of Living", "Property Price To Income"],
            "Lifestyle": ["Quality Of Life", "Safety", "Traffic Commute Time", "Health Care"],
            "Environment": ["Pollution", "Climate"]
        }
        
        st.divider()
        st.subheader("🔍 Select Indicator")
        
        # Option to view all indicators or filter by category
        show_all = st.checkbox("Show All Indicators", value=True)
        
        if not show_all:
            # Select indicator group using horizontal radio buttons
            selected_group = st.radio(
                "Select indicator category:",
                options=list(indicator_groups.keys()),
                horizontal=True
            )
            
            # Filter numeric columns based on selected group
            group_indicators = [col for col in numeric_columns if any(col.startswith(ind) for ind in indicator_groups[selected_group])]
            
            # Select from filtered indicators
            if group_indicators:
                selected_indicator = st.selectbox("Choose an indicator to compare:", group_indicators, index=0)
            else:
                selected_indicator = "No indicators available for this category"
        else:
            # Show all indicators
            selected_indicator = st.selectbox("Choose an indicator to compare:", ["All Indicators"] + numeric_columns, index=0)
        
        st.divider()

    with st.sidebar:
        if compare_type == "Countries":
            st.subheader("🌍 Select Countries")
            countries = df["Country"].unique()
            entity1 = st.selectbox("Select Country 1", countries, index=0)
            entity2 = st.selectbox("Select Country 2", countries, index=1)
            # Filter data for selected countries
            df1 = df[df["Country"] == entity1].melt(id_vars=["Country"], value_vars=numeric_columns, var_name="Indicator", value_name="Value")
            df2 = df[df["Country"] == entity2].melt(id_vars=["Country"], value_vars=numeric_columns, var_name="Indicator", value_name="Value")
        else:
            st.subheader("🌎 Select Continents")
            continents = df["Continent"].dropna().unique()
            entity1 = st.selectbox("Select Continent 1", continents, index=1)
            entity2 = st.selectbox("Select Continent 2", continents, index=2)
            # Compute average values per continent
            df1 = df[df["Continent"] == entity1].groupby("Continent")[numeric_columns].mean().reset_index()
            df1 = df1.melt(id_vars=["Continent"], value_vars=numeric_columns, var_name="Indicator", value_name="Value")
            df2 = df[df["Continent"] == entity2].groupby("Continent")[numeric_columns].mean().reset_index()
            df2 = df2.melt(id_vars=["Continent"], value_vars=numeric_columns, var_name="Indicator", value_name="Value")

    # Filter data based on selected indicator
    if not show_all and selected_indicator != "All Indicators" and selected_indicator != "No indicators available for this category":
        df1 = df1[df1["Indicator"] == selected_indicator]
        df2 = df2[df2["Indicator"] == selected_indicator]
    elif show_all and selected_indicator != "All Indicators":
        df1 = df1[df1["Indicator"] == selected_indicator]
        df2 = df2[df2["Indicator"] == selected_indicator]
    elif not show_all:
        # If filtering by category, only show indicators from that category
        group_indicators = [col for col in numeric_columns if any(col.startswith(ind) for ind in indicator_groups[selected_group])]
        df1 = df1[df1["Indicator"].isin(group_indicators)]
        df2 = df2[df2["Indicator"].isin(group_indicators)]

    # Define consistent colors for charts (matching the world map theme)
    color_1 = "#4682B4"  # Steel Blue (matches the lake color from world map)
    color_2 = "#228B22"  # Forest Green (matches the tree color from world map)

    # Interactive Bar Chart 1
    bar_chart1 = alt.Chart(df1).mark_bar().encode(
        x=alt.X("Indicator", sort=None, title="Indicator", axis=alt.Axis(labelAngle=45, labelLimit=400, labelOverlap=False)),
        y=alt.Y("Value", title="Indicator Value"),
        color=alt.value(color_1),  # Blue
        tooltip=["Indicator", "Value"]
    ).properties(
        width=1200, height=700, 
        title=alt.TitleParams(f"Indicator Values for {entity1}", anchor="middle")
    )

    # Interactive Bar Chart 2
    bar_chart2 = alt.Chart(df2).mark_bar().encode(
        x=alt.X("Indicator", sort=None, title="Indicator", axis=alt.Axis(labelAngle=45, labelLimit=400, labelOverlap=False)),
        y=alt.Y("Value", title="Indicator Value"),
        color=alt.value(color_2),  # Green
        tooltip=["Indicator", "Value"]
    ).properties(
        width=1200, height=700, 
        title=alt.TitleParams(f"Indicator Values for {entity2}", anchor="middle")
    )

    # Interactive Bar Chart 3 (for single indicator comparison)
    show_single_indicator = selected_indicator != "All Indicators" and selected_indicator != "No indicators available for this category"
    if show_single_indicator:
        if df1.empty or df2.empty:
            st.warning("No data available for the selected indicator and entities.")
        else:
            df_compare = pd.DataFrame({
                "Entity": [entity1, entity2],
                "Value": [df1["Value"].values[0], df2["Value"].values[0]],
            })
            
            bar_chart3 = alt.Chart(df_compare).mark_bar().encode(
                x=alt.X("Entity", title="Entity", axis=alt.Axis(labelAngle=0, labelLimit=400, labelOverlap=False)),
                y=alt.Y("Value", title=selected_indicator),
                color=alt.Color("Entity", scale=alt.Scale(domain=[entity1, entity2], range=[color_1, color_2])),
                tooltip=["Entity", "Value"]
            ).properties(
                width=600, height=400, 
                title=alt.TitleParams(f"Comparison between {entity1} and {entity2}", anchor="middle")
            )

    # Combine data for other visualizations
    df_area = pd.concat([df1.assign(Entity=entity1), df2.assign(Entity=entity2)])

    # Bubble Chart
    tooltip_fields = ["Indicator", "Value", "Entity"]
    
    if not df1.empty and not df2.empty:
        bubble_chart = alt.Chart(df_area).mark_circle().encode(
            x=alt.X("Indicator", sort=None, title="Indicator", axis=alt.Axis(labelAngle=45, labelLimit=400, labelOverlap=False)),
            y=alt.Y("Value", title="Indicator Value"),
            size=alt.Size("Value", title="Magnitude"),
            color=alt.Color("Entity", scale=alt.Scale(domain=[entity1, entity2], range=[color_1, color_2])),
            tooltip=tooltip_fields
        ).properties(
            width=800, height=500, 
            title=alt.TitleParams(f"Bubble Chart Comparison Between {entity1} and {entity2}", anchor="middle")
        ).configure_axis(
            labelColor='white', titleColor='white'
        )

        # Radar Chart
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=df1["Value"], theta=df1["Indicator"], fill='toself', name=entity1, line=dict(color=color_1)))
        fig.add_trace(go.Scatterpolar(r=df2["Value"], theta=df2["Indicator"], fill='toself', name=entity2, line=dict(color=color_2)))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    tickfont=dict(color="white"),
                    gridcolor="rgba(255, 255, 255, 0.3)"
                ),
                angularaxis=dict(
                    tickfont=dict(size=10, color="white")
                )
            ),
            showlegend=True,
            title=dict(
                text="Radar Chart Comparison",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font=dict(size=16, color="white")
            ),
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font_color='white',
            width=1000,
            height=600
        )

        # Conditionally create tabs based on selected indicator
        if selected_indicator == "All Indicators":
            # If comparing all indicators, show all three chart types
            tab1, tab2, tab3 = st.tabs(["📊 Bar Charts", "💭 Bubble Chart", "📡 Radar Chart"])
            
            with tab1:
                col1, col2 = st.columns(2)
                col1.altair_chart(bar_chart1, use_container_width=True)
                col2.altair_chart(bar_chart2, use_container_width=True)
                    
            with tab2:
                st.altair_chart(bubble_chart, use_container_width=True)
                
            with tab3:
                st.plotly_chart(fig, use_container_width=True)
        else:
            # If comparing a single indicator, show only bar chart
            tab1 = st.tabs(["📊 Bar Chart"])
            
            with tab1[0]:
                st.altair_chart(bar_chart3, use_container_width=True)
                
                # Display comparison metrics for single indicator
                value1 = df1["Value"].values[0]
                value2 = df2["Value"].values[0]
                difference = abs(value1 - value2)
                # Create a metrics display row
                metric_cols = st.columns(3)
                metric_cols[0].metric(entity1, f"{value1:.2f}")
                metric_cols[1].metric(entity2, f"{value2:.2f}")
                metric_cols[2].metric("Difference", f"{difference:.2f}")
                
                # Display comparison message
                if value1 > value2:
                    st.success(
                        f"📌 {entity1} scores *{difference:.2f} points higher* than {entity2} in {selected_indicator}."
                    )
                elif value1 < value2:
                    st.warning(
                        f"📌 {entity2} scores *{difference:.2f} points higher* than {entity1} in {selected_indicator}."
                    )
                else:
                    st.info(f"🤝 {entity1} and {entity2} have *equal* scores for {selected_indicator}.")
    else:
        st.warning("No data available for the selected filters.")
    
    # --- Footer ---
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #888;">
        <p>Data source: Numbeo Quality of Life Indices | Dashboard created with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)