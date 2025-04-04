import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

from utils import custom_navigation

def app():


        # --- Data Loading and Preprocessing ---
    df = pd.read_excel('final_data.xlsx')

    # Define indicators (all columns except 'country' and 'continent')
    indicators = [col for col in df.columns if col not in ['country', 'continent']]

    # Separate numerical and categorical indicators
    numerical_indicators = [col for col in indicators if not col.endswith('Category')]
    categorical_indicators = [col for col in indicators if col.endswith('Category')]

    # Coerce only numerical indicators to numeric
    for col in numerical_indicators:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # --- Configuration ---

    # Define consistent color maps for standard categories
    standard_category_colors = {
        'higher_is_better': {
            'Very Low': '#d73027',    # Dark red
            'Low': '#f46d43',         # Red-orange
            'Moderate': '#ffffbf',    # Yellow
            'High': '#a6d96a',        # Light green
            'Very High': '#1a9850'    # Dark green
        },
        'lower_is_better': {
            'Very Low': '#1a9850',    # Dark green
            'Low': '#a6d96a',         # Light green
            'Moderate': '#ffffbf',    # Yellow
            'High': '#f46d43',        # Red-orange
            'Very High': '#d73027'    # Dark red
        }
    }

    # Define indicator polarity (whether higher is better or worse)
    indicator_polarity = {
        'Pollution': 'lower_is_better',
        'Climate': 'higher_is_better',
        'Purchasing Power': 'higher_is_better',
        'Cost of Living': 'lower_is_better',
        'Property Price to Income': 'lower_is_better',
        'Safety': 'higher_is_better',
        'Health Care': 'higher_is_better',
        'Quality of Life': 'higher_is_better',
        'Traffic Commute Time': 'lower_is_better'
    }

    # Define red-to-green color scales based on polarity
    color_scales = {
        'higher_is_better': 'RdYlGn',     # Red to Green (higher is better)
        'lower_is_better': 'RdYlGn_r'     # Green to Red (lower is better)
    }

    # Dictionary of indicator descriptions
    descriptions = {
        'Quality of Life': """
    **Quality of Life Index**  
    The Quality of Life Index is an empirical measure that evaluates how various factors—economic stability, healthcare access, safety, environmental conditions, and infrastructure quality—shape daily life, health, and well-being. It ranges from **0.00 to 224.31** (mean: **131.39**), showing significant global variation. Notably, **33 countries** rank in the "Very High" category, meaning about a quarter of nations offer exceptional living conditions. This index highlights disparities and provides a quantitative basis for assessing global living standards.  
    **Calculation Method:**  
    `index.main = Math.max(0, 100 + purchasingPowerInclRentIndex / 2.5 - (housePriceToIncomeRatio * 1.0) - costOfLivingIndex / 10 + safetyIndex / 2.0 + healthIndex / 2.5 - trafficTimeIndex / 2.0 - pollutionIndex * 2.0 / 3.0 + climateIndex / 3.0);` (Source: Numbeo)
    """,
        'Purchasing Power': """
    **Purchasing Power Index**  
    This index measures residents' buying capacity, with higher values indicating greater purchasing power. It spans **10.33 (Uganda)** to **195.55 (Luxembourg)**, with a global mean of **72.67**, underscoring economic disparities. **33 countries** fall into the "Low" category, where limited income restricts access to necessities. Top performers include Luxembourg, Qatar, and Kuwait, while Uganda and Nigeria rank lowest.  
    **Calculation Method:** Not specified.
    """,
        'Cost of Living': """
    **Cost of Living Index**  
    The Cost of Living Index gauges the expense of essentials like food, rent, and transportation. It ranges from **17.90 to 101.18** (mean: **41.41**), with **61 countries** in the "Very Low" category, indicating lower costs in most regions compared to high-cost nations like Switzerland (**101.18**). However, low costs don't always equate to high quality of life due to income-expense gaps.  
    **Calculation Method:** Benchmarked against New York City (NYC = 100). A score of 120 means 20% more expensive than NYC; 75 means 25% cheaper.
    """,
        'Property Price to Income': """
    **Property Price to Income Value**  
    This ratio shows housing affordability relative to income, with lower values indicating more accessible markets. It ranges from **2.81 to 1075.92** (standard deviation: **145.98**), revealing vast disparities. **36 countries** are in the "Very High" category, where housing is often unaffordable, impacting stability and wealth-building.  
    **Calculation Method:** Not explicitly described.
    """,
        'Safety': """
    **Safety Index**  
    The Safety Index assesses crime rates, public safety, and law enforcement efficiency. It ranges from **25.36 to 84.43** (mean: **57.91**, standard deviation: **13.60**), with **53 countries** in the "Moderate" category, indicating reasonable but not exceptional safety. It correlates with other quality of life factors.  
    **Calculation Method:** Based on public reports and Numbeo user surveys; exact method unspecified.
    """,
        'Health Care': """
    **Health Care Index**  
    This index evaluates medical infrastructure, accessibility, and efficiency. It ranges from **41.05 to 86.50** (mean: **62.60**), with **64 countries** in the "High" category, suggesting strong healthcare in over half the nations studied. It's vital for well-being and life expectancy.  
    **Calculation Method:** Derived from public health reports and Numbeo surveys; formula not provided.
    """,
        'Pollution': """
    **Pollution Index**  
    The Pollution Index measures air and environmental pollution, with higher values signaling worse conditions. It ranges from **11.83 (Finland)** to **89.41 (Lebanon)** (mean: **56.15**), with **48 countries** in the "High" category. Poor air quality links to health issues like respiratory diseases, affecting life expectancy.  
    **Calculation Method:** Not specified.
    """,
        'Traffic Commute Time': """
    **Traffic Commute Time Index**  
    This index tracks average commute times, impacting work-life balance. It ranges from **15.67 to 65.31** (mean: **35.43**), with **38 countries** in the "Low" category, showing achievable commute times in many places. It ties to infrastructure and urban planning.  
    **Calculation Method:** Not specified.
    """,
        'Climate': """
    **Climate Index**  
    The Climate Index evaluates weather conditions (temperature, humidity, variability) for livability. It spans **-3.54 (Mongolia)** to **99.89 (Guatemala)** (mean: **77.83**), with **58 countries** in the "Very High" category. Favorable climates don't always mean healthy environments, as pollution can offset benefits.  
    **Calculation Method:** Not specified.
    """
    }

    note_dict = {
        'Purchasing Power': 'Higher is better: A higher value means residents can buy more with their income.',
        'Cost of Living': 'Lower is better: Lower scores mean more affordable living expenses.',
        'Property Price to Income': 'Lower is better: Indicates more affordable housing relative to income.',
        'Safety': 'Higher is better: Indicates lower crime rates and more efficient law enforcement.',
        'Health Care': 'Higher is better: Reflects better medical infrastructure, accessibility, and efficiency.',
        'Pollution': 'Lower is better: Indicates cleaner air and better environmental conditions.',
        'Traffic Commute Time': 'Lower is better: Means shorter daily commute times and better work-life balance.',
        'Climate': 'Higher is better: Suggests more favorable weather conditions.',
        'Quality of Life': 'Higher is better: Indicates better overall living conditions.'
    }

    # --- Streamlit Dashboard Setup ---

    # Main title and description in a container for better styling
    with st.container():
        col1, col2 = st.columns([5, 1])
        with col1:
            st.title('World Map of Quality of Life Indicators')
            st.markdown('Explore global quality of life metrics across countries.')
            
    with st.expander("ℹ️ How to Navigate This Page", expanded=False):
        st.markdown("""
        <strong><br>🔍 Dashboard Features and How to Use:</strong>

         - **Select an Indicator** from the sidebar to analyze various quality of life metrics such as Purchasing Power, Safety, Health Care, and more.<br>
        - **Filter by Continents**: Use the Geographic Filter to narrow down the map and data to specific Continents.<br>  
        - **Log Scale Option**:  Toggle the **log scale** for better visualization of skewed data.<br>  
        - **Viewing the Map**:  
            - The map highlights countries based on the selected indicator, allowing easy comparison.  
            - You can **zoom in and pan** across the world map for a closer look at specific countries.<br>  

        <strong><br>📊 Interactive Visualizations:</strong>  

        - **World Map**: Countries are color-coded based on the selected indicator. Hover over them to see values.<br>
        - **Category Distribution**: If the indicator has categories (e.g., "Very Low", "Low"), a bar chart will display the distribution of countries in these categories.<br>  

        <strong><br>💡 Tips for Effective Analysis:</strong>  

        - **Select individual indicators** to analyze specific metrics like cost of living, safety, or healthcare for deeper insights.  
        - **Color-coded insights**:
            - 🟢 Green represents better performance.  
            - 🔴 Red indicates areas for improvement.  
        - **Use log scale** for better visualization when working with indicators with large numerical ranges.  
        - **Compare different continents** to understand regional differences in quality of life and other factors.  
        """, unsafe_allow_html=True)

    # Create a proper sidebar with sections for better organization
    with st.sidebar:
        st.header('Filters')
        
        # Create visual selector for indicators with icons
        st.subheader("🔍 Select Indicator")
        
        # Group indicators by category for better organization
        indicator_groups = {
            "Economic": ["Purchasing Power", "Cost of Living", "Property Price to Income"],
            "Lifestyle": ["Quality of Life", "Safety", "Traffic Commute Time", "Health Care"],
            "Environment": ["Pollution", "Climate"]
        }
        
        # Flatten the dictionary for selection
        indicator_map = {}
        for group, inds in indicator_groups.items():
            for ind in inds:
                # Find all matching indicators (value and category)
                matches = [i for i in indicators if i.startswith(ind)]
                for match in matches:
                    indicator_map[match] = group
        
        # Select indicator group first
        selected_group = st.radio(
            "Select indicator category:",
            options=list(indicator_groups.keys()),
            horizontal=True
        )
        
        # Then select specific indicator from that group
        # Replace the code starting around line 89 (after selected_group = st.radio(...))

        # Then select specific indicator from that group
        base_group_indicators = []
        for ind_name in indicators:
            for base_ind in indicator_groups[selected_group]:
                if ind_name.startswith(base_ind):
                    base_group_indicators.append(base_ind)
                    break

        base_group_indicators = list(set(base_group_indicators))  # Remove duplicates
        selected_base_indicator = st.selectbox('Select Indicator', base_group_indicators)

        # Always use the value version for the main map display
        if f"{selected_base_indicator} Value" in indicators:
            selected_indicator = f"{selected_base_indicator} Value"
        else:
            selected_indicator = selected_base_indicator
            
        # Also keep track of the category version for the bar chart
        category_indicator = f"{selected_base_indicator} Category" if f"{selected_base_indicator} Category" in indicators else None



        # Add quick info about the selected indicator
        # Extract base indicator name properly (handling multi-word indicators)
        if ' Value' in selected_indicator:
            base_name = selected_indicator.replace(' Value', '')
        elif ' Category' in selected_indicator:
            base_name = selected_indicator.replace(' Category', '')
        else:
            base_name = selected_indicator
        polarity = indicator_polarity.get(base_name, 'higher_is_better')
        note = note_dict.get(base_name, 'No note available.')
        
        # Show quick info in a colorful box
        if polarity == 'higher_is_better':
            st.success(f"**{note}**")
        else:
            st.error(f"**{note}**")

        # Determine if the selected indicator is categorical
        is_categorical = False
        
        st.divider()
        st.subheader("🌍 Geographic Filters")
        
        # Add an option to select all continents easily
        continents = sorted(df['continent'].unique())
        select_all_continents = st.checkbox("Select All Continents", True)
        
        if select_all_continents:
            selected_continents = continents
        else:
            selected_continents = st.multiselect('Select Continents', continents, default=[])
        
        # Ensure at least one continent is selected
        if not selected_continents:
            st.warning("Please select at least one continent.")
        #   selected_continents = [continents[0]]  # Default to first continent if none selected
        
        st.divider()
        st.subheader("📊 Indicator Filters")

        if is_categorical:
            unique_categories = sorted(df[selected_indicator].dropna().unique())
            
            # Fix the category ordering for standard categories
            standard_categories = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
            if all(cat in standard_categories for cat in unique_categories):
                # Sort according to standard order
                unique_categories = [cat for cat in standard_categories if cat in unique_categories]
                
            select_all_categories = st.checkbox("Select All Categories", True)
            if select_all_categories:
                selected_categories = unique_categories
            else:
                selected_categories = st.multiselect('Select Categories', unique_categories, default=[])
                
            if not selected_categories:
                st.warning("Please select at least one category.")
                selected_categories = [unique_categories[0]]  # Default to first category if none selected
            
            # Determine color scheme info based on polarity
            if polarity == 'higher_is_better':
                color_info = "Red (worse) to Green (better)"
            else:
                color_info = "Green (better) to Red (worse)"
        else:
            # Determine if log scaling is appropriate
            min_val = float(df[selected_indicator].min())
            max_val = float(df[selected_indicator].max())
            
            # Add a switch for log scaling with better explanation
            use_log_scale = False
            if min_val > 0 and max_val / min_val > 10:
                use_log_scale = st.checkbox("Use logarithmic scale", value=True, 
                                        help="Recommended for data with wide ranges")
            
            # Filter range based on scaling choice
            if use_log_scale and min_val > 0:
                log_min = np.log(min_val)
                log_max = np.log(max_val)
                log_filter_range = st.slider(
                    'Filter by Indicator Value (log scale)', 
                    float(log_min), 
                    float(log_max), 
                    (float(log_min), float(log_max)), 
                    step=(log_max - log_min) / 100
                )
                filter_range = (np.exp(log_filter_range[0]), np.exp(log_filter_range[1]))
                st.write(f"Selected Range: {filter_range[0]:.2f} to {filter_range[1]:.2f}")
            else:
                filter_range = st.slider(
                    'Filter by Indicator Value', 
                    float(min_val), float(max_val), 
                    (float(min_val), float(max_val)), 
                    step=(max_val - min_val) / 100
                )
            
            # Explain the color scheme
            if polarity == 'higher_is_better':
                color_info = "Red (worse) to Green (better)"
            else:
                color_info = "Green (better) to Red (worse)"

        # Show indicator information in a dedicated section
        st.divider()
        st.subheader("ℹ️ Indicator Information")
        st.info(f"📊 **Color Scheme**: {color_info}")
        

    # --- Data Filtering ---
    if is_categorical:
        # Base filtering by continent and category
        filtered_df = df[
            (df['continent'].isin(selected_continents)) &
            (df[selected_indicator].isin(selected_categories))
        ].dropna(subset=[selected_indicator])
    else:
        # Base filtering by continent and value range
        filtered_df = df[
            (df['continent'].isin(selected_continents)) &
            (df[selected_indicator] >= filter_range[0]) &
            (df[selected_indicator] <= filter_range[1])
        ].dropna(subset=[selected_indicator])

    # Show warning if no data after filtering
    if filtered_df.empty:
        st.warning("No data matches your selected filters. Please adjust your criteria.")
        st.stop()


    # --- Choropleth Map Creation ---
    color_scale = color_scales[polarity]

    # Display a loading spinner for map creation
    with st.spinner("Generating map..."):
        if is_categorical:
            hover_data = {selected_indicator: True}
            
            # Define standard category order
            standard_categories = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
            
            # Check if all categories in the data are in our standard list
            all_standard = all(cat in standard_categories for cat in filtered_df[selected_indicator].unique())
            
            if all_standard:
                # Create a fixed numerical mapping
                numerical_mapping = {
                    'Very Low': 0,
                    'Low': 1,
                    'Moderate': 2,
                    'High': 3,
                    'Very High': 4
                }
                
                # Apply mapping and ensure sorting order is correct
                filtered_df['numerical_value'] = filtered_df[selected_indicator].map(numerical_mapping)
                
                # Get actual categories present in the filtered data
                present_categories = sorted(
                    filtered_df[selected_indicator].unique(),
                    key=lambda x: numerical_mapping[x]  # Sort by the numerical mapping
                )
                
                # Create the map with continuous color scale
                fig = px.choropleth(
                    filtered_df,
                    locations='country',
                    locationmode='country names',
                    color='numerical_value',
                    hover_name='country',
                    hover_data={selected_indicator: True, 'numerical_value': False},
                    color_continuous_scale=color_scale,
                    title=f'World Map of {selected_indicator}',
                    range_color=[0, 4]  # Fixed range for all 5 categories
                )
                
                # Update colorbar to show only the present categories
                fig.update_layout(
                    coloraxis_colorbar=dict(
                        title=selected_indicator,
                        tickvals=[numerical_mapping[cat] for cat in present_categories],
                        ticktext=present_categories
                    )
                )
            else:
                # For non-standard categories, use a discrete color map
                # Get the actual categories present in the data
                present_categories = sorted(filtered_df[selected_indicator].unique())
                num_categories = len(present_categories)
                
                # FIX: Handle the case when num_categories is 0 (no categories to display)
                if num_categories == 0:
                    st.warning("No data available for the selected filters.")
                    st.stop()
                
                # FIX: Make sure we have at least 2 points when sampling colorscale
                if num_categories == 1:
                    # If only one category, use a fixed color based on polarity
                    if polarity == 'higher_is_better':
                        colors = ['#00CC00']  # Green for the single category (higher is better)
                    else:
                        colors = ['#CC0000']  # Red for the single category (lower is better)
                else:
                    # Create custom color mapping to ensure consistency
                    if polarity == 'higher_is_better':
                        # For higher_is_better: Red -> Yellow -> Green
                        colors = px.colors.sample_colorscale('RdYlGn', num_categories)
                    else:
                        # For lower_is_better: Green -> Yellow -> Red
                        colors = px.colors.sample_colorscale('RdYlGn_r', num_categories)
                
                # Create a category color map
                category_color_map = {cat: colors[i] for i, cat in enumerate(present_categories)}
                
                # Create the map with discrete color scheme
                fig = px.choropleth(
                    filtered_df,
                    locations='country',
                    locationmode='country names',
                    color=selected_indicator,
                    hover_name='country',
                    hover_data=hover_data,
                    color_discrete_map=category_color_map,
                    title=f'World Map of {selected_indicator}',
                    scope="world"
                )
        else:
            # Determine if we should use log scale for visualization
            if use_log_scale and filtered_df[selected_indicator].min() > 0:
                filtered_df['Scale'] = np.log(filtered_df[selected_indicator])
                hover_data = {
                    selected_indicator: ':.2f',
                    'Scale': False  # Hide the log value in the hover
                }
                color_column = 'Scale'
                colorbar_title = f'Log of {selected_indicator}'
            else:
                filtered_df['Scale'] = filtered_df[selected_indicator]
                hover_data = {selected_indicator: ':.2f'}
                color_column = 'Scale'
                colorbar_title = selected_indicator
            
            # Add continent to hover data
            hover_data['continent'] = True
        
            fig = px.choropleth(
                filtered_df,
                locations='country',
                locationmode='country names',
                color=color_column,
                hover_name='country',
                hover_data=hover_data,
                color_continuous_scale=color_scale,
                title=f'World Map of {selected_indicator}',
                # Using robust quantiles for color range to handle outliers
                range_color=[filtered_df[color_column].quantile(0.05), filtered_df[color_column].quantile(0.95)]
            )
            
            # Update colorbar title
            fig.update_layout(coloraxis_colorbar=dict(title=colorbar_title))

        # Improved layout for better readability
        layout_update = dict(
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font_color='white',
            title_font_size=24,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                coastlinecolor='rgba(255, 255, 255, 0.5)',
                projection_type='equirectangular',
                bgcolor='#0E1117',
                landcolor='rgba(50, 50, 50, 0.2)',
                lakecolor='#0E1117',
                showcountries=True,
                countrycolor='rgba(255, 255, 255, 0.3)',
                showland=True
            ),
            margin={"r": 0, "t": 50, "l": 0, "b": 0}
        )
        
        fig.update_layout(**layout_update)
        fig.update_traces(marker_line_color='white', marker_line_width=0.3)
        fig.update_geos(fitbounds=False, visible=True)
        
        # Enable map zoom and pan for better interactivity
        fig.update_geos(projection_type="natural earth", showframe=True)
        
        # Add source citation to the figure
        fig.add_annotation(
            xref="paper", yref="paper",
            x=0.01, y=0.01,
            text="",
            showarrow=False,
            font=dict(size=10, color="rgba(255,255,255,0.5)"),
            align="left"
        )
        
        # Allow the map to take more vertical space
        st.plotly_chart(fig, use_container_width=True, height=600)

    # --- Supporting Information ---
    st.divider()

    tab3, tab2, tab1 = st.tabs(["📑 Description", "📋 Data Table", "📊 Statistics"])

    with tab1:
        # First show numerical statistics for the value version
        if not filtered_df.empty:
            avg_val = filtered_df[selected_indicator].mean()
            min_val = filtered_df[selected_indicator].min()
            max_val = filtered_df[selected_indicator].max()
            median_val = filtered_df[selected_indicator].median()
            std_val = filtered_df[selected_indicator].std()
            
            min_country = filtered_df.loc[filtered_df[selected_indicator].idxmin(), 'country']
            max_country = filtered_df.loc[filtered_df[selected_indicator].idxmax(), 'country']
            
            # Create a metrics display row
            metric_cols = st.columns(5)
            metric_cols[0].metric("Average", f"{avg_val:.2f}")
            metric_cols[1].metric("Median", f"{median_val:.2f}")
            metric_cols[2].metric("Std Dev", f"{std_val:.2f}")
            metric_cols[3].metric(f"Min ({min_country})", f"{min_val:.2f}")
            metric_cols[4].metric(f"Max ({max_country})", f"{max_val:.2f}")
            

            # Then also show the category distribution if available
            if category_indicator and category_indicator in df.columns:
                st.subheader("Category Distribution")
                cat_df = df[df['continent'].isin(selected_continents)].dropna(subset=[category_indicator])
                category_counts = cat_df[category_indicator].value_counts().reset_index()
                category_counts.columns = ['Category', 'Count']
                
                # Sort categories if they're standard
                standard_categories = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
                if all(cat in standard_categories for cat in category_counts['Category']):
                    category_order = {cat: i for i, cat in enumerate(standard_categories)}
                    category_counts['Sort_Order'] = category_counts['Category'].map(category_order)
                    category_counts = category_counts.sort_values('Sort_Order').drop('Sort_Order', axis=1)
                
                # Calculate percentages
                total = category_counts['Count'].sum()
                category_counts['Percentage'] = (category_counts['Count'] / total * 100).round(1)
                
                # Create a bullet chart using a single color with various opacities
                fig = go.Figure()
                
                # Determine the base color based on your theme
                base_color = '#4287f5'  # A pleasing blue that works well with dark themes
                
                # Add bars for each category
                for i, row in enumerate(category_counts.itertuples()):
                    fig.add_trace(go.Bar(
                        y=[row.Category],
                        x=[row.Percentage],
                        orientation='h',
                        name=row.Category,
                        text=[f"{row.Count} countries ({row.Percentage}%)"],
                        textposition='outside',
                        marker=dict(
                            color=base_color,
                            opacity=0.3 + (0.7 * (i / (len(category_counts) - 1 if len(category_counts) > 1 else 1)))
                        ),
                        hoverinfo='text',
                        hovertext=[f"{row.Category}: {row.Count} countries ({row.Percentage}%)"]
                    ))
                
                # Update layout
                fig.update_layout(
                    title=f"Distribution of {selected_base_indicator} Categories",
                    paper_bgcolor='#0E1117',
                    plot_bgcolor='rgba(17, 17, 17, 0.3)',
                    font_color='white',
                    showlegend=False,
                    xaxis=dict(
                        title='Percentage of Countries (%)',
                        range=[0, max(category_counts['Percentage']) * 1.15]  # Add space for labels
                    ),
                    yaxis=dict(
                        title='',
                        categoryorder='array',
                        categoryarray=category_counts['Category'].tolist()
                    ),
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=max(250, 100 + (len(category_counts) * 50))  # Dynamic height based on categories
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"**Number of Countries Displayed:** {len(filtered_df)}")

    with tab2:
        if not filtered_df.empty:
            st.subheader("Data Table")
            
            # Add search box and sorting options
            col1, col2 = st.columns([3, 1])
            with col1:
                search_table = st.text_input("Search in table", "")
            with col2:
                sort_order = st.selectbox(
                    "Sort by",
                    ["Highest First", "Lowest First"],
                    index=0 if polarity == 'higher_is_better' else 1
                )
            
            # Apply sorting based on user selection
            ascending = sort_order == "Lowest First"
            
            if search_table:
                filtered_table_df = filtered_df[
                    filtered_df['country'].str.contains(search_table, case=False) | 
                    filtered_df['continent'].str.contains(search_table, case=False)
                ]
            else:
                filtered_table_df = filtered_df
                
            # Apply sorting
            if not is_categorical:
                display_df = filtered_table_df.sort_values(by=selected_indicator, ascending=ascending)
            else:
                # For categorical data, create a sorting order
                if all(cat in ['Very Low', 'Low', 'Moderate', 'High', 'Very High'] 
                    for cat in filtered_table_df[selected_indicator].unique()):
                    cat_order = {'Very Low': 0, 'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}
                    filtered_table_df['sort_key'] = filtered_table_df[selected_indicator].map(cat_order)
                    display_df = filtered_table_df.sort_values(
                        by='sort_key', 
                        ascending=not ascending if polarity == 'higher_is_better' else ascending
                    ).drop('sort_key', axis=1)
                else:
                    display_df = filtered_table_df
            
            # First define the original columns
            original_columns = ['country', 'continent', selected_indicator]

            # Create a copy to avoid modifying the original
            display_df = display_df.copy()

            # Create a mapping from original to capitalized columns for display
            display_columns = [col.capitalize() if col in ['country', 'continent'] else col for col in original_columns]

            # Rename the DataFrame columns
            display_df.columns = [col.capitalize() if col in ['country', 'continent'] else col for col in display_df.columns]

            # Now use the capitalized column names
            st.dataframe(
                display_df[display_columns],
                use_container_width=True,
                hide_index=True
            )
            
            # Add export functionality
            csv = display_df[display_columns].to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f'{selected_indicator.replace(" ", "_")}_data.csv',
                mime='text/csv',
            )
        else:
            st.info("No data available with the current filters.")

    with tab3:
        # Display information about the selected indicator
        st.subheader(f"About {selected_indicator.replace(' Category', '').replace(' Value', '')}")
        
        # Get the base indicator name without category/value suffix
        base_indicator = selected_indicator.replace(' Value', '').replace(' Category', '')
        
        # Display the description if available
        if base_indicator in descriptions:
            st.markdown(descriptions[base_indicator])
        else:
            st.info(f"No detailed description available for {base_indicator}.")


    # --- Footer ---
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #888;">
        <p>Data source: Numbeo Quality of Life Indices | Dashboard created with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)



    # Add caching for improved performance
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_indicator_stats(indicator_name):
        """Get basic stats for an indicator to use in descriptions"""
        stats = {
            'min': float(df[indicator_name].min()),
            'max': float(df[indicator_name].max()),
            'mean': float(df[indicator_name].mean()),
            'median': float(df[indicator_name].median()),
            'std': float(df[indicator_name].std())
        }
        return stats
