import streamlit as st
import pandas as pd
import plotly.express as px
import importlib
from utils import custom_navigation



# Page configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="Quality of Life Analysis",
    page_icon="🌍",
    layout="wide"
)


def main():
    # Get the current page from URL parameter
    query_params = st.query_params
    page = query_params.get("page", "main")

    # Custom navigation
    custom_navigation()

    # Render the appropriate page based on the query parameter
    if page == "main":
        # Custom CSS to enhance the visual appeal
        st.markdown("""
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #1E3A8A;
                margin-bottom: 1rem;
            }
            .section-header {
                font-size: 1.5rem;
                font-weight: bold;
                color: #FFFFFF;
                margin-top: 1rem;
                margin-bottom: 0.5rem;
            }
            .sub-header {
                font-size: 1.5rem;
                font-weight: bold;
                color: #3B82F6;
                margin-top: 1rem;
            }
            .card {
                padding: 1.0rem;
                border-radius: 0.5rem;
                background-color: #F8FAFC;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                color: #1F2937;  /* Very dark gray text for strong contrast;
                margin-bottom: 1rem;
            }
            .highlight {
                background-color: #DBEAFE;
                padding: 0.5rem;
                border-radius: 0.25rem;
            }
            .emoji-icon {
                font-size: 2rem;
                margin-right: 0.5rem;
            }
            .container {
                display: flex;
                align-items: center;
            }
        </style>
        """, unsafe_allow_html=True)

        # Header
        st.markdown(
        '<h3 class="main-header" style="color: white;">🌍 Global Quality of Life Analysis</h3>', 
        unsafe_allow_html=True)
            

        st.markdown("This interactive dashboard allows users to explore, compare, and analyze quality-of-life indicators across different countries and regions.")

        # Interactive tabs for main sections
        tab1, tab2, tab3 = st.tabs(["📋 Overview", "🔍 Data Insights", "🧪 Hypothesis"])

        with tab1:
            st.markdown(
        '<h4 class="main-header" style="color: white;">🌍 Introduction & Problem Definition</h4>', 
        unsafe_allow_html=True)
            # Expandable introduction

            st.markdown('<div class="container"><strong>Problem Definition</strong></div>', unsafe_allow_html=True)
            st.markdown("""
                Quality of life varies significantly across regions due to economic stability, 
                        healthcare access, environmental conditions, safety, and infrastructure differences. 
                        While data on these factors exists, it is often fragmented, making it difficult to analyze trends,
                        compare regions, and identify areas for improvement. A structured, accessible, visually engaging tool is needed to address this gap.
                """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                with st.expander("💡 Central Message"):
                 st.markdown("""
                        Quality of life is shaped by interconnected factors that vary significantly across countries and regions, 
                requiring systematic analysis to understand global disparities and inform policy decisions.
                """)
                

                with st.expander("🎯 Goal"):
                 st.markdown("""
                        To develop an interactive dashboard consolidating global quality-of-life indicators, enabling users to explore, compare, and analyze different regions. 
                        This tool will provide structured insights for informed decision-making and policy development.
                 """)
                 
            
            with col2:
                with st.expander("📖 Narrative"):
                 st.markdown("""
                            Quality of life is shaped by multiple interconnected factors, yet the lack of a unified framework makes it challenging to assess and compare conditions across countries. 
                            This project aims to bridge that gap by transforming raw data into a user-friendly visualization tool. 
                            By integrating economic, healthcare, and environmental indicators, the dashboard will help users identify patterns, assess disparities, 
                            and support data-driven improvements in living conditions worldwide.
                  """)
                

                with st.expander("👥 Target Audience"):
                 st.write("- *Policymakers* - To evaluate national and regional performance and implement improvement strategies.\n"
                          "- *Researchers* - To analyze economic, healthcare, and environmental trends.\n"
                          "- *Healthcare Professionals* - To understand public health impacts and shape policies.\n"
                          "- *Urban Planners* - To design more sustainable cities using insights on infrastructure and pollution.\n"
                          "- *Individuals & Expats* - To make informed relocation and investment decisions.\n"
                          "- *Investors* - To assess economic stability and cost of living across countries.",
                          unsafe_allow_html=True)  

        with tab2:
            st.markdown('<div class="section-header">Dataset Overview</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="container"><span class="emoji-icon">📊</span><strong>Dataset Composition</strong></div>', unsafe_allow_html=True)
            st.markdown("""
                The analysis uses two integrated datasets:
                - **Quality of Life for Each Country**: Analyzes socio-economic and environmental factors from Numbeo.
                - **Country-Continent Classification**: Added to enable regional comparisons.
                """)
            
            st.markdown('<div class="section-header">Dataset at a Glance</div>', unsafe_allow_html=True)
            
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">114</div>
                    <div class="metric-label">Countries</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[1]:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">15+</div>
                    <div class="metric-label">Quality Indicators</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[2]:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">5</div>
                    <div class="metric-label">Continents</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[3]:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">Crowd-sourced</div>
                    <div class="metric-label">Data Collection\n</div>
                </div>
                """, unsafe_allow_html=True)
                
            
            st.write("")
            st.write("")

            st.markdown('<div class="section-header">Key Findings</div>', unsafe_allow_html=True)
             # Use columns for key findings
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="card"><b>Property Affordability vs. Income</b><br>The Property Price to Income Ratio varies dramatically, with values ranging from as low as 2.81 to as high as 1075.92. This disparity highlights severe challenges in housing affordability in many regions.</div>', unsafe_allow_html=True)
                
            
            with col2:
                st.markdown('<div class="card"><b>Pollution vs. Climate</b><br>Despite generally favorable climate scores (with an average nearly 77.83), many countries struggle with high pollution levels (averaging 56.15), indicating that pleasant weather does not necessarily ensure a clean environment.</div>', unsafe_allow_html=True)
            
            st.write("")
            st.write("")
            
            fig = px.pie(values=[13.16, 15.79, 34.21, 34.21, 2.63 ], names=['Africa', 'Americas', 'Asia', 'Europe', 'Oceania'], 
                    title='Distribution by Continents', height=250)
            fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)



        with tab3:
            st.markdown('<p class="sub-header">Hypothesis Testing</p>', unsafe_allow_html=True)
            
            # Interactive hypothesis selection
            hypothesis = st.selectbox(
                "Select hypothesis to explore:",
                ["H1: Countries with higher Purchasing Power exhibit higher Cost of Living",
                 "H2: Countries with higher Purchasing Power tend to have lower Pollution"]
            )
            
            if hypothesis == "H1: Countries with higher Purchasing Power exhibit higher Cost of Living":
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.markdown('<div class="container"><span class="emoji-icon">💲</span></div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    **Findings**: Data broadly supports this hypothesis, with a positive correlation (r ~ 0.71) between purchasing power and cost of living.
                    
                    **Key Insights**:
                    - Wealthier nations generally have higher price levels for goods, services, and housing
                    - Some exceptions exist, like Saudi Arabia, which maintains high purchasing power with moderate living costs
                    - Local policies, natural resources, and economic priorities play significant roles in determining affordability
                    """)
                
                st.markdown('<div class="highlight">', unsafe_allow_html=True)
                st.markdown("""
                **Implications**: While wealth and expense often go hand-in-hand, examples like Saudi Arabia show that prudent policies—such as
                subsidizing essentials or investing in public infrastructure—can help balance affordability with prosperity.
                """)
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.markdown('<div class="container"><span class="emoji-icon">🏭</span></div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    **Findings**: Analysis supports this hypothesis, with a negative correlation (r ~ -0.63) between purchasing power and pollution.
                    
                    **Key Insights**:
                    - European countries generally show higher purchasing power and lower pollution values
                    - Countries with lower economic resources often correlate with higher pollution
                    - Limited investment in eco-friendly technologies contributes to higher pollution in less wealthy nations
                    """)
                
                st.markdown('<div class="highlight">', unsafe_allow_html=True)
                st.markdown("""
                **Notable Exceptions**: 
                - Middle Eastern oil-rich countries (Bahrain, Saudi Arabia, Kuwait, Qatar) show high purchasing power but also high pollution
                - Rwanda demonstrates low pollution despite limited economic resources due to strong environmental policies
                """)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Footer ---
        st.divider()

        st.markdown("""
            <div style="text-align: center; color: #888;">
                <p>Data source: Numbeo Quality of Life Indices | Dashboard created with Streamlit</p>
                <p style="text-align: center; color: #888;">Team Visionaries</p>
            </div>
        """, unsafe_allow_html=True)

    elif page == "WorldMap":
        # Import and run WorldMap page content
        world_map = importlib.import_module("WorldMap")
        world_map.app()


    elif page == "ComparisonOfCountries":
        # Import and run Comparison page content
        comparison = importlib.import_module("ComparisonOfCountries")
        comparison.app()

    elif page == "TopvBottom":
        # Import and run Top vs Bottom page content
        top_bottom = importlib.import_module("TopvBottom")
        top_bottom.app()
    
    elif page == "GlobalMetrics":
        # Import and run Top vs Bottom page content
        GlobalMetrics = importlib.import_module("GlobalMetrics")
        GlobalMetrics.app()

    


if __name__ == "__main__":
    main()