import streamlit as st
import pandas as pd
import plotly.express as px
from utils import custom_navigation


def app():

    # --- Page Configuration ---

    # --- Load Data ---
    df = pd.read_excel("final_data.xlsx")

    # --- Clean Column Names ---
    df.columns = df.columns.str.strip().str.lower()  # Normalize column names

    # Create a proper sidebar with sections for better organization
    with st.sidebar:
        st.header('Filters')
        
        # Create visual selector for indicators with icons
        st.subheader("🔍 Select Indicator")
        
        # Group indicators by category for better organization
        indicator_groups = {
            "Economic": ["Purchasing Power Value", "Cost of Living Value", "Property Price to Income Value"],
            "Lifestyle": ["Quality of Life Value", "Safety Value", "Traffic Commute Time Value", "Health Care Value"],
            "Environment": ["Pollution Value", "Climate Value"]
        }
        
        # Select indicator group first
        selected_group = st.radio(
            "Select indicator category:",
            options=list(indicator_groups.keys()),
            horizontal=True
        )
        
        # Then select specific indicator from that group
        selected_indicator = st.selectbox(
            'Select Indicator', 
            indicator_groups[selected_group]
        )


    # Convert selected_indicator to lowercase for consistency
    selected_indicator = selected_indicator.lower()

    view_type = st.sidebar.radio("📈 Choose Analysis Type", ["Top/Bottom Countries", "Top vs Bottom Comparison"])

    if view_type == "Top/Bottom Countries" or view_type == "Top vs Bottom Comparison":
        num_countries = st.sidebar.slider("📌 Select Number of Countries", min_value=3, max_value=10, value=5)
        rank_type = st.sidebar.radio("📊 Select Ranking Type", ["Top Countries", "Bottom Countries"])

    # --- Continent Filter Option ---
    filter_continent = st.sidebar.checkbox("🌍 Geographic Filters")
    selected_continent = None
    if filter_continent:
        continents = df["continent"].unique()
        selected_continent = st.sidebar.selectbox("🌍 Select a Continent", continents)
        df = df[df["continent"] == selected_continent]

    # --- Sidebar Filters for Min/Max Values (Styled like screenshot) ---
    if view_type == "Top/Bottom Countries":
        st.sidebar.subheader("📉 Indicator Filters")
        
        if not df.empty:
            min_val = float(df[selected_indicator].min())
            max_val = float(df[selected_indicator].max())
            
            selected_min, selected_max = st.sidebar.slider(
                "Filter by Indicator Value",
                min_value=round(min_val, 2),
                max_value=round(max_val, 2),
                value=(round(min_val, 2), round(max_val, 2))
            )

            st.sidebar.markdown(
                f"<div style='color: gray; font-size: 14px;'>"
                f"Selected Range: <strong>{selected_min}</strong> to <strong>{selected_max}</strong>"
                f"</div>", unsafe_allow_html=True
            )

            df = df[(df[selected_indicator] >= selected_min) & (df[selected_indicator] <= selected_max)]

            # Color scheme info (optional)
            st.sidebar.markdown("---")
            st.sidebar.subheader("ℹ️ Indicator Information")
            st.sidebar.info("🎨 **Color Scheme:** Green (better) to Red (worse)")
        else:
            st.sidebar.warning("⚠️ No data available for selected filters.")


    # --- Top/Bottom Countries View ---
    if view_type == "Top/Bottom Countries":
        if rank_type == "Top Countries":
            sorted_df = df.nlargest(num_countries, selected_indicator)
            color_scale = "RdYlGn"  # Green for high values, Red for low values
        else:
            sorted_df = df.nsmallest(num_countries, selected_indicator)
            color_scale = "RdYlGn"  # Green for high values, Red for low values
            
        # --- Update Title with Continent (if selected) ---
        title_continent = f" in {selected_continent}" if selected_continent else ""

        # --- Scatter Plot ---
        st.subheader(f"📌 {rank_type} - {selected_indicator.replace('_', ' ').title()}{title_continent}")
        st.markdown(
            f"This visualization ranks the **{rank_type.lower()}** performers in **{selected_indicator.replace('_', ' ').title()}**, "
            "providing insight into which countries excel or struggle in this aspect of quality of life."
        )

        # --- Add Explanation Expander ---
        with st.expander("ℹ️ How to Navigate This Page", expanded=False):
            st.markdown("""
            <strong><br>🔍 Dashboard Features and How to Use:</strong>
            
            - **Select an Indicator** from the sidebar to explore key quality of life metrics like Purchasing Power, Safety, Health Care, and more.<br>
            - **Choose Analysis Type**: You can view **Top/Bottom Countries** to see the highest and lowest rankings, or use **Top vs Bottom Comparison** to compare the best and worst performers side-by-side.<br>
            - **Apply Filters** to refine your results:
                - Use the **Geographic Filter** to narrow the data to a specific Continents.
                - Adjust the **Range Sliders** to focus on specific values within the chosen indicator.<br>
            
            <strong><br>📊 Interactive Visualizations:</strong>
        
            - **Scatter Plot**: Visualize the distribution of countries by the selected indicator. Hover over data points to see more details.<br>
            - **Bar Chart**: Compare the performance of top vs bottom countries for the selected indicator.<br><br>

            <strong><br>💡 Tips for Effective Analysis:</strong>
            
            - **Select individual indicators** to analyze specific metrics like cost of living, safety, or healthcare for deeper insights.<br>
            - **Color-coded insights**:
            - 🟢 Green represents better performance.
            - 🔴 Red indicates areas for improvement.<br>
            <strong>
            """, unsafe_allow_html=True)


        # Define color scale dynamically based on indicator type
        if selected_indicator in ["purchasing power value", "safety value", "health care value", 
                                "climate value", "quality of life value"]:
            color_scale = "RdYlGn"  # Green for high (better), Red for low (worse)
        else:
            color_scale = "RdYlGn_r"  # Green for low (better), Red for high (worse)

        # --- Scatter Plot ---
        fig_scatter = px.scatter(
            sorted_df, 
            x="country", 
            y=selected_indicator, 
            size=selected_indicator, 
            color=selected_indicator,
            color_continuous_scale=color_scale,  # Apply appropriate color scale dynamically
            hover_name="country",
            title=f"📊 {rank_type} - {selected_indicator.replace('_', ' ').title()} {title_continent}",
        )
        fig_scatter.update_layout(
            xaxis_title="Country",
            yaxis_title=selected_indicator.replace('_', ' ').title(),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)



    # --- Top vs Bottom Comparison ---
    elif view_type == "Top vs Bottom Comparison":
        top_countries = df.nlargest(num_countries, selected_indicator)
        bottom_countries = df.nsmallest(num_countries, selected_indicator)
        comparison_df = pd.concat([top_countries, bottom_countries])

        st.subheader(f"📌 Top vs Bottom Countries for {selected_indicator.replace('_', ' ').title()}")
        st.markdown(
            "This comparative analysis highlights the stark differences between the **best-performing** and **worst-performing** "
            f"countries in **{selected_indicator.replace('_', ' ').title()}**. This allows us to understand economic, environmental, and policy-driven "
            "factors that differentiate these groups."
        )

        # --- Bar Chart Comparison ---
        fig_compare = px.bar(
            comparison_df,
            x="country",
            y=selected_indicator,
            text=selected_indicator,
            color="country",
            title=f"📊 Comparative Analysis: Top vs Bottom Countries in {selected_indicator.replace('_', ' ').title()}",
            labels={"Value": selected_indicator},
        )
        fig_compare.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_compare.update_layout(
            xaxis_title="Country",
            yaxis_title=selected_indicator.replace('_', ' ').title(),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig_compare, use_container_width=True)
        
        # --- Enhanced Insights Section ---
        st.subheader("🔍 Key Insights from the Comparison")
    insights = {
        "purchasing power value": "### 🟢 High-Ranking Countries\n"
            "- **Higher salaries relative to the cost of living**, allow citizens to afford more goods and services.\n"
            "- **Strong economic growth and low inflation**, ensure stable financial conditions.\n\n"
            "### 🔴 Low-Ranking Countries\n"
            "- **High inflation**, reduces the actual value of wages and savings.\n"
            "- **Weak currency value**, making imports expensive and lowering affordability.\n\n"
            "### 🌍 How This Affects Quality of Life\n"
            "- **High purchasing power** leads to **better financial security, higher living standards, and economic opportunities**.\n"
            "- **Low purchasing power** results in **poverty, economic uncertainty, and reduced social mobility**.",

        "health care value": "### 🟢 High-Ranking Countries\n"
            "- **Well-funded hospitals** equipped with modern medical technology.\n"
            "- **Universal healthcare**, ensuring accessibility for all citizens.\n\n"
            "### 🔴 Low-Ranking Countries\n"
            "- **Underfunded public hospitals**, leading to long wait times and inadequate facilities.\n"
            "- **Limited access to medicines** due to high costs or shortages.\n\n"
            "### 🌍 How This Affects Quality of Life\n"
            "- Countries investing in healthcare see **higher life expectancy and stronger economies**.\n"
            "- Poor healthcare leads to **public health crises and financial strain**.",

        "cost of living value": "### 🟢 Low-Ranking Countries\n"
            "- **Basic needs like food, rent, and transportation are more affordable**, allowing residents to maintain a decent standard of living.\n"
            "- **Lower daily expenses** increase the capacity to save or invest income.\n\n"
            "### 🔴 High-Ranking Countries\n"
            "- **High consumer prices** make everyday expenses significantly burdensome.\n"
            "- **Costly urban centers** may reduce disposable income despite high salaries.\n\n"
            "### 🌍 How This Affects Quality of Life\n"
            "- A **lower cost of living improves affordability and reduces economic stress**.\n"
            "- High living costs can **undermine quality of life even in wealthy nations**.",

        "property price to income value": "### 🟢 Low-Ranking Countries\n"
            "- **Affordable housing relative to income** makes homeownership realistic for many.\n"
            "- **Lower rent and mortgage ratios** lead to improved financial stability.\n\n"
            "### 🔴 High-Ranking Countries\n"
            "- **Housing prices are disproportionately high**, making it difficult for average earners to afford homes.\n"
            "- **Urban areas experience severe affordability crises**, especially for younger populations.\n\n"
            "### 🌍 How This Affects Quality of Life\n"
            "- Affordable property prices support **social mobility and long-term wealth**.\n"
            "- High ratios reflect **housing inequality and urban affordability challenges**.",

        "safety value": "### 🟢 High-Ranking Countries\n"
            "- **Low crime rates and effective policing** ensure a sense of security.\n"
            "- **Public spaces feel safe**, enabling freer movement and community engagement.\n\n"
            "### 🔴 Low-Ranking Countries\n"
            "- **High levels of crime and social unrest** create fear and instability.\n"
            "- **Poor enforcement or systemic corruption** undermines public trust.\n\n"
            "### 🌍 How This Affects Quality of Life\n"
            "- Personal safety enhances **mental well-being, freedom, and investment appeal**.\n"
            "- Unsafe environments can **discourage tourism, investment, and social cohesion**.",

        "pollution value": "### 🟢 Low-Ranking Countries\n"
            "- **Clean air, water, and surroundings** promote better public health.\n"
            "- **Effective environmental regulations** lead to sustainable urban living.\n\n"
            "### 🔴 High-Ranking Countries\n"
            "- **Air and water contamination**, often from industrial or traffic sources, pose major health risks.\n"
            "- **Poor waste management** contributes to environmental degradation.\n\n"
            "### 🌍 How This Affects Quality of Life\n"
            "- Pollution has direct links to **respiratory diseases, reduced productivity, and premature death**.\n"
            "- Cleaner environments support **long-term national health and development goals**.",

        "traffic commute time value": "### 🟢 Low-Ranking Countries\n"
            "- **Efficient transportation systems** reduce commuting stress and save time.\n"
            "- **Shorter commute times** support better work-life balance and overall satisfaction.\n\n"
            "### 🔴 High-Ranking Countries\n"
            "- **Long traffic delays** decrease productivity and increase fatigue.\n"
            "- **Poor infrastructure** leads to lost time and frustration for workers.\n\n"
            "### 🌍 How This Affects Quality of Life\n"
            "- Daily commuting time **influences well-being, stress levels, and time with family**.\n"
            "- High commute burdens **impact both mental health and national productivity**.",

        "climate value": "### 🟢 High-Ranking Countries\n"
            "- **Mild, pleasant weather conditions** improve comfort and health.\n"
            "- **Low climate volatility** reduces exposure to extreme weather events.\n\n"
            "### 🔴 Low-Ranking Countries\n"
            "- **Extreme temperatures or unpredictable weather** can disrupt daily life.\n"
            "- **Frequent natural disasters** such as floods or droughts lower resilience.\n\n"
            "### 🌍 How This Affects Quality of Life\n"
            "- Favorable climates support **agriculture, tourism, and lifestyle comfort**.\n"
            "- Harsh climates can **strain infrastructure and increase health risks**.",

        "quality of life value": "### 🟢 High-Ranking Countries\n"
            "- **Strong overall performance across safety, health, economy, and environment**.\n"
            "- **High life satisfaction and access to essential services**.\n\n"
            "### 🔴 Low-Ranking Countries\n"
            "- **Multiple challenges across pollution, income, healthcare, or safety**.\n"
            "- **Lower public trust and quality in institutions and infrastructure**.\n\n"
            "### 🌍 How This Affects Quality of Life\n"
            "- This index captures a **holistic view of well-being and happiness**.\n"
            "- It reflects how **balanced national development directly shapes lives**."
    }
    insight_text = insights.get(selected_indicator, "This analysis highlights key economic, social, and policy-driven differences between top and bottom-ranking countries.")
    st.markdown(insight_text)

     # --- Footer ---
    st.divider()

    st.markdown("""
        <div style="text-align: center; color: #888;">
            <p>Data source: Numbeo Quality of Life Indices | Dashboard created with Streamlit</p>
            <p style="text-align: center; color: #888;">Team Visionaries</p>
        </div>
    """, unsafe_allow_html=True)
