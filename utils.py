import streamlit as st

def custom_navigation():
    # Inject Font Awesome CSS and custom styles
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
    .navigation {
        display: flex;
        justify-content: center;
        background-color: #1C1C1C;
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255,255,255,0.05);
    }
    .nav-button {
        margin: 0 10px;
        padding: 10px 20px;
        text-decoration: none;
        color: #CCCCCC;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
        font-size: 0.9rem;
        position: relative;
        display: flex;
        align-items: center;
    }
    .nav-button i {
        margin-right: 8px;
    }
    .nav-button:hover {
        background-color: rgba(255,255,255,0.15);
        color: #FFFFFF;
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .nav-button.active {
        background-color: #333333;
        color: #FFFFFF;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        border-bottom: 2px solid #FFFFFF;
    }
    @media (max-width: 600px) {
        .navigation {
            flex-direction: column;
        }
        .nav-button {
            margin: 5px 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Get current page from query parameters
    query_params = st.query_params
    current_page = query_params.get("page", "main")

    # Render the navigation bar with buttons and icons
    st.markdown(f"""
    <div class="navigation" role="navigation">
        <a href="?page=main" class="nav-button {'active' if current_page == 'main' else ''}" aria-label="Home"><i class="fas fa-home"></i> Home</a>
        <a href="?page=WorldMap" class="nav-button {'active' if current_page == 'WorldMap' else ''}" aria-label="World Map"><i class="fas fa-globe"></i> World Map</a>
        <a href="?page=ComparisonOfCountries" class="nav-button {'active' if current_page == 'ComparisonOfCountries' else ''}" aria-label="Country & Continent Comparison"><i class="fas fa-chart-bar"></i> Country & Continent Comparison</a>
        <a href="?page=TopvBottom" class="nav-button {'active' if current_page == 'TopvBottom' else ''}" aria-label="Top vs Bottom"><i class="fas fa-sort-amount-up"></i> Top vs Bottom</a>
        <a href="?page=GlobalMetrics" class="nav-button {'active' if current_page == 'GlobalMetrics' else ''}" aria-label="Global Metrics"><i class="fas fa-chart-line"></i> Global Metrics</a>
    </div>
    """, unsafe_allow_html=True)