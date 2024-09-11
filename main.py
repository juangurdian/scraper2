import streamlit as st
import requests
from parse import parse_with_ollama  # Import the parsing function

# API configuration
API_KEY = '6e7ee8b4862c0615e828ef7ab69988f5'
SCRAPER_API_URL = 'https://api.scraperapi.com/'

# Function to scrape website
def scrape_website(url):
    payload = {'api_key': API_KEY, 'url': url}
    response = requests.get(SCRAPER_API_URL, params=payload)
    
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Failed to scrape the website. Status code: {response.status_code}")
        return ""

# Function to split content into chunks (assuming a chunk size for LLaMA input)
def split_content(content, chunk_size=5000):
    return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

# Streamlit UI
st.title("Car Models Scraper")
url = st.text_input("Enter Car Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")
        
        # Scrape the website
        scraped_content = scrape_website(url)
        
        # Store the content in Streamlit session state
        st.session_state.scraped_content = scraped_content
        
        # Display the scraped content in an expandable text box
        with st.expander("View Scraped Content"):
            st.text_area("Scraped Content", scraped_content, height=300)

if "scraped_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Split the content into chunks for LLaMA processing
            dom_chunks = split_content(st.session_state.scraped_content)
            
            # Parse the content with LLaMA
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            
            if parsed_result.strip():  # Check if the result is not empty
                st.write(parsed_result)
            else:
                st.write("No matching information found based on the provided description.")