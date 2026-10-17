import os
import datetime
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from google import genai
from google.genai import errors

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="TripCraft AI – Intelligent Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Gemini Client: {e}")

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "itinerary_data" not in st.session_state:
    st.session_state.itinerary_data = None
if "budget_data" not in st.session_state:
    st.session_state.budget_data = None

# Sidebar Configuration for Trip Details
st.sidebar.markdown("## 🧭 Trip Parameters")
st.sidebar.markdown("Configure your travel preferences below:")

with st.sidebar.form("trip_form"):
    destination = st.text_input("Destination City / Country", "Goa, India")
    start_loc = st.text_input("Starting Location", "Mumbai, India")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.date.today() + datetime.timedelta(days=10))
    with col2:
        end_date = st.date_input("End Date", datetime.date.today() + datetime.timedelta(days=13))
        
    col3, col4 = st.columns(2)
    with col3:
        budget = st.number_input("Total Budget", min_value=1000, value=25000, step=1000)
    with col4:
        currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"])
        
    travelers = st.number_input("Number of Travellers", min_value=1, value=2, step=1)
    
    preferences = st.multiselect(
        "Travel Preferences",
        ["Adventure", "Nature", "History & Culture", "Shopping", "Food & Dining", "Relaxation & Spa", "Nightlife", "Beach & Relaxation"],
        default=["Beach & Relaxation", "Food & Dining", "Nightlife"]
    )
    
    accommodation = st.selectbox(
        "Preferred Accommodation", 
        ["Budget Hostel / Backpacker", "Mid-range Hotel (3-Star)", "Luxury Resort / 5-Star", "Homestay / Villa"]
    )
    
    transport_pref = st.selectbox(
        "Preferred Transport", 
        ["Public Transport / Buses", "Rental Car / Scooty", "Taxis / Cabs", "Flights / Trains"]
    )
    
    submitted = st.form_submit_button("✨ Generate Itinerary & Plan Budget")

# Validation and Generation Logic
if submitted:
    if end_date < start_date:
        st.sidebar.error("Error: End date cannot be earlier than the start date.")
    elif not client:
        st.sidebar.error("API Key missing! Please set GEMINI_API_KEY in your .env file.")
    else:
        num_days = (end_date - start_date).days + 1
        if num_days <= 0:
            num_days = 1

        with st.spinner("TripCraft AI is crafting your personalized journey..."):
            prompt = f"""
            You are an expert AI travel planner and budget analyst. Generate a complete travel itinerary and cost breakdown for the following trip:
            - Destination: {destination}
            - Starting Location: {start_loc}
            - Dates: {start_date} to {end_date} ({num_days} days)
            - Total Budget: {budget} {currency}
            - Number of Travellers: {travelers}
            - Preferences: {', '.join(preferences)}
            - Accommodation Style: {accommodation}
            - Transport Preference: {transport_pref}

            Please provide your response clearly separated into two main sections:
            1. **DAILY ITINERARY**: Day-by-day plan (Day 1 to Day {num_days}) including Morning, Afternoon, Evening activities, recommended meals, transport tips, and estimated costs per activity.
            2. **BUDGET BREAKDOWN**: Estimated costs structured into categories: Transportation, Accommodation, Food & Dining, Attractions & Activities, Local Transit, and Miscellaneous. Include Estimated Total and Remaining Balance against the user's budget of {budget} {currency}. Mention clearly that prices are estimates.
            """
            try:
                # UPDATED MODEL NAME TO gemini-3.8-flash
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )
                
                # Store output in session state
                st.session_state.itinerary_data = response.text
                st.session_state.messages = [{"role": "assistant", "content": f"Hello! I have generated your personalized trip to **{destination}**. Check out the tabs on the main screen for your daily plan and budget breakdown. Feel free to ask me any follow-up questions!"}]
                st.success("Trip successfully planned!")
            except errors.APIError as e:
                st.sidebar.error(f"Gemini API Error: {e}")
            except Exception as e:
                st.sidebar.error(f"An unexpected error occurred: {e}")

# Main Layout Area
st.markdown('<p class="main-header">✈️ TripCraft AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your intelligent companion for personalized travel planning and expense management.</p>', unsafe_allow_html=True)

if st.session_state.itinerary_data is None:
    st.info("👈 Fill out your trip details in the sidebar and click **Generate Itinerary & Plan Budget** to get started!")
else:
    tab1, tab2, tab3 = st.tabs(["📅 Daily Itinerary", "💰 Budget Breakdown", "💬 Trip Assistant Chat"])
    
    with tab1:
        st.subheader(f"Your Itinerary to {destination}")
        st.markdown("---")
        st.markdown(st.session_state.itinerary_data)
        
    with tab2:
        st.subheader("Estimated Budget Breakdown")
        st.markdown("All costs are calculated estimates and may vary based on live conditions.")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Budget Allocated", value=f"{budget:,.2f} {currency}")
        with col2:
            st.metric(label="Number of Travellers", value=travelers)
        with col3:
            st.metric(label="Trip Duration", value=f"{(end_date - start_date).days + 1} Days")
            
        st.markdown("---")
        
        # Sample structured budget table view
        budget_table_data = {
            "Expense Category": ["Accommodation", "Transportation", "Food & Dining", "Attractions & Activities", "Local Transit", "Miscellaneous"],
            "Estimated Cost (Approx.)": [
                f"{budget * 0.40:,.2f} {currency}",
                f"{budget * 0.25:,.2f} {currency}",
                f"{budget * 0.15:,.2f} {currency}",
                f"{budget * 0.10:,.2f} {currency}",
                f"{budget * 0.05:,.2f} {currency}",
                f"{budget * 0.05:,.2f} {currency}"
            ]
        }
        df_budget = pd.DataFrame(budget_table_data)
        st.table(df_budget)
        
        if budget < 10000:
            st.warning("⚠️ **Budget Alert:** Your specified budget is on the lower side for this destination. Consider adjusting or prioritizing free attractions and budget hostels.")

    with tab3:
        st.subheader("Chat with TripCraft Assistant")
        st.markdown("Ask follow-up questions, modify activities, or request restaurant recommendations while retaining your trip context.")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        # Chat input
        if user_prompt := st.chat_input("Ask about weather, packing, vegetarian restaurants, etc..."):
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    context_prompt = f"""
                    You are TripCraft AI, an expert travel assistant. 
                    Current Trip Details:
                    - Destination: {destination}
                    - Dates: {start_date} to {end_date}
                    - Budget: {budget} {currency}
                    - Travellers: {travelers}
                    - Preferences: {', '.join(preferences)}
                    
                    Chat History:
                    {[m['content'] for m in st.session_state.messages]}
                    
                    User's latest question: {user_prompt}
                    """
                    try:
                        # UPDATED MODEL NAME TO gemini-3.8-flash
                        chat_response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=context_prompt
                        )
                        bot_reply = chat_response.text
                        st.markdown(bot_reply)
                        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    except Exception as e:
                        error_msg = f"Sorry, I encountered an error responding to your question: {e}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Reset button in sidebar
    if st.sidebar.button("🔄 Reset Conversation & Itinerary"):
        st.session_state.itinerary_data = None
        st.session_state.messages = []
        st.rerun()
