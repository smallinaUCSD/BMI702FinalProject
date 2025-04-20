import streamlit as st
import requests
import re
import json
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="MedAnnotate",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for custom styling
st.markdown("""
<style>
    /* Main styling */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Hide default sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Navigation bar */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background-color: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .navbar-brand {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4169E1;
        display: flex;
        align-items: center;
    }
    
    .navbar-links {
        display: flex;
        gap: 1.5rem;
    }
    
    .nav-link {
        color: #4B5563;
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .nav-link:hover, .nav-link.active {
        background-color: #EEF2FF;
        color: #4169E1;
    }
    
    /* Hero section */
    .hero-container {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #f5f7ff 0%, #e4ecff 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    
    /* Feature cards */
    .feature-section {
        padding: 2rem 0;
    }
    
    .feature-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 2rem;
        color: #4169E1;
        margin-bottom: 1rem;
    }
    
    /* Team cards */
    .team-card {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .team-img-container {
        height: 200px;
        overflow: hidden;
    }
    
    .team-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .team-info {
        padding: 1rem;
    }
    
    .team-name {
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.3rem;
    }
    
    .team-role {
        color: #4169E1;
        font-size: 0.9rem;
        margin-bottom: 0.7rem;
    }
    
    /* Tool section */
    .tool-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    .annotation-result {
        background: #f9f9f9;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #4169E1;
        margin-top: 1.5rem;
    }
    
    /* Contact Form */
    .contact-form {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    /* Buttons */
    .primary-btn {
        background-color: #4169E1;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    
    .primary-btn:hover {
        background-color: #3158d6;
    }
    
    /* Drug annotations */
    .drug-name {
        color: #4169E1;
        font-weight: 600;
        background-color: #EEF2FF;
        padding: 0 3px;
        border-radius: 3px;
    }
    
    .drug-dosage {
        color: #10B981;
        font-weight: 600;
        background-color: #ECFDF5;
        padding: 0 3px;
        border-radius: 3px;
    }
    
    .drug-frequency {
        color: #F59E0B;
        font-weight: 600;
        background-color: #FEF3C7;
        padding: 0 3px;
        border-radius: 3px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #6B7280;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Navigation menu
def create_navbar(active_page):
    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">
            <span>MedAnnotate</span>
        </div>
        <div class="navbar-links">
            <a href="#" class="nav-link {'active' if active_page == 'Home' else ''}" id="home-link">🏠 Home</a>
            <a href="#" class="nav-link {'active' if active_page == 'About Us' else ''}" id="about-link">👥 About Us</a>
            <a href="#" class="nav-link {'active' if active_page == 'Tool' else ''}" id="tool-link">🧪 Use Tool</a>
            <a href="#" class="nav-link {'active' if active_page == 'Contact' else ''}" id="contact-link">📬 Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# State management
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Navigation JavaScript
st.markdown("""
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const homeLink = document.getElementById('home-link');
        const aboutLink = document.getElementById('about-link');
        const toolLink = document.getElementById('tool-link');
        const contactLink = document.getElementById('contact-link');
        
        homeLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = "?page=Home";
        });
        
        aboutLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = "?page=About Us";
        });
        
        toolLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = "?page=Tool";
        });
        
        contactLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = "?page=Contact";
        });
    });
</script>
""", unsafe_allow_html=True)

# Check URL parameters
query_params = st.experimental_get_query_params()
if 'page' in query_params:
    st.session_state.page = query_params['page'][0]

# Create the navbar with the active page
create_navbar(st.session_state.page)

# Define placeholder image function
def get_placeholder_image(width, height, text="Team Member"):
    from PIL import Image, ImageDraw, ImageFont
    import io
    import base64
    
    # Create a placeholder image
    img = Image.new('RGB', (width, height), color=(200, 200, 200))
    d = ImageDraw.Draw(img)
    
    # Add text
    d.text((width//2, height//2), text, fill=(80, 80, 80), anchor="mm")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

# Home page
if st.session_state.page == 'Home':
    # Hero section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">MedAnnotate</h1>
        <p class="hero-subtitle">AI-powered extraction of structured drug data from messy doctor notes</p>
        <button class="primary-btn" onclick="window.location.href='?page=Tool'">Try it now</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("<h2 style='text-align: center; margin-bottom: 1.5rem;'>Our Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💊</div>
            <h3>Drug Detection</h3>
            <p>Advanced AI algorithms identify medication names in free-text clinical notes with high precision.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Dosage & Frequency Parsing</h3>
            <p>Extract detailed medication information including dosage, frequency, and route of administration.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <h3>Color-Coded Highlights</h3>
            <p>Visual formatting makes it easy to review and validate extracted medication data at a glance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Why section
    st.markdown("<h2 style='text-align: center; margin: 2rem 0 1.5rem;'>Why MedAnnotate?</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>Save Time</h3>
            <p>Reduce manual chart review time by up to 70% by automating the extraction of medication information.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>Improve Accuracy</h3>
            <p>Minimize human error and ensure that critical medication details are never missed.</p>
        </div>
        """, unsafe_allow_html=True)

# About Us page
elif st.session_state.page == 'About Us':
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Meet Our Team</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; max-width: 800px; margin: 0 auto 2rem;'>We're a group of graduate students and researchers from Harvard DBMI and UCSD working on healthcare AI tools that solve real-world problems.</p>", unsafe_allow_html=True)
    
    # Team members
    col1, col2, col3 = st.columns(3)
    
    # Using placeholders instead of real images
    with col1:
        st.markdown(f"""
        <div class="team-card">
            <div class="team-img-container">
                <img src="{get_placeholder_image(300, 300, 'Seshu Mallina')}" class="team-img" alt="Seshu Mallina"/>
            </div>
            <div class="team-info">
                <h3 class="team-name">Seshu Mallina</h3>
                <p class="team-role">ML/OPS Engineer</p>
                <p>Seshu completed his undergraduate studies at UCSD, earning a degree in Bioinformatics and Computer Science. He specializes in building ML pipelines for healthcare applications with expertise in medical data analysis.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="team-card">
            <div class="team-img-container">
                <img src="{get_placeholder_image(300, 300, 'Chuck Lin')}" class="team-img" alt="Chuck Lin"/>
            </div>
            <div class="team-info">
                <h3 class="team-name">Chuck Lin</h3>
                <p class="team-role">ML/OPS Engineer (Future MD)</p>
                <p>Chuck obtained his degree in Biology at William & Mary, where he discovered compounds for regulating cellular processes. He's researching infectious disease correlation using patient data with interests in genomics and health data integration.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="team-card">
            <div class="team-img-container">
                <img src="{get_placeholder_image(300, 300, 'Ritvik Rania')}" class="team-img" alt="Ritvik Rania"/>
            </div>
            <div class="team-info">
                <h3 class="team-name">Ritvik Rania</h3>
                <p class="team-role">ML/OPS Engineer</p>
                <p>Ritvik completed his undergraduate studies in Biomedical Engineering at City University of Hong Kong, with expertise in accessibility innovation and healthcare automation, having designed systems for preventive maintenance.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="team-card">
            <div class="team-img-container">
                <img src="{get_placeholder_image(300, 300, 'Kyla Gabriel')}" class="team-img" alt="Kyla Gabriel"/>
            </div>
            <div class="team-info">
                <h3 class="team-name">Kyla Gabriel</h3>
                <p class="team-role">ML/OPS Engineer (Future MD)</p>
                <p>Kyla completed her undergraduate studies in biomedical engineering with a focus on neuroscience. Her research spans segmentation for surgical applications and diabetes prediction models.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="team-card">
            <div class="team-img-container">
                <img src="{get_placeholder_image(300, 300, 'Harry Li')}" class="team-img" alt="Harry Li"/>
            </div>
            <div class="team-info">
                <h3 class="team-name">Harry Li</h3>
                <p class="team-role">ML/OPS Engineer</p>
                <p>Harry completed his undergraduate studies at UPenn with a double major in Computational Biology and Biochemistry, specializing in machine learning and bioinformatics analysis for drug discovery applications.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Tool page
elif st.session_state.page == 'Tool':
    st.markdown("<h1 style='text-align: center; margin-bottom: 1.5rem;'>MedAnnotate Tool</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; max-width: 800px; margin: 0 auto 2rem;'>Extract structured medication information from clinical notes with our AI-powered annotation tool.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
    
    # Example notes
    example_notes = [
        "Patient is to continue with Lisinopril 10mg once daily for hypertension. Also prescribed Metformin 500mg twice daily with meals for diabetes management.",
        "Started on Atorvastatin 40mg daily at bedtime. Will continue Aspirin 81mg once daily.",
        "Discharged with prescriptions for Amoxicillin 500mg TID for 7 days and Acetaminophen 650mg q6h PRN for pain."
    ]
    
    st.markdown("<h3>Patient Note</h3>", unsafe_allow_html=True)
    st.markdown("<p>Paste a clinical note or select an example below:</p>", unsafe_allow_html=True)
    
    # Example selector
    example_option = st.selectbox(
        "Select an example or paste your own text:",
        ["Custom input"] + example_notes
    )
    
    if example_option == "Custom input":
        user_note = st.text_area("", height=150, key="custom_note")
    else:
        user_note = st.text_area("", example_option, height=150, key="example_note")
    
    # Process button
    if st.button("Extract Medication Data", key="process_btn"):
        if user_note:
            st.markdown("<h3>Annotated Result:</h3>", unsafe_allow_html=True)
            
            # Simulate API processing - Replace this with actual Gemini API call
            def process_note(note):
                # Simple regex-based annotation for demo purposes
                # In production, this would call the Gemini API with a proper prompt
                
                # Define patterns for drugs, dosages, and frequencies
                drug_pattern = r"\b(?:Lisinopril|Metformin|Atorvastatin|Aspirin|Amoxicillin|Acetaminophen)\b"
                dosage_pattern = r"\b\d+(?:\.\d+)?(?:mg|g|mcg|mL)\b"
                frequency_pattern = r"\b(?:once|twice|three times|daily|BID|TID|QID|q\dh|PRN)\b"
                
                # Apply annotations
                note = re.sub(drug_pattern, r'<span class="drug-name">\g<0></span>', note)
                note = re.sub(dosage_pattern, r'<span class="drug-dosage">\g<0></span>', note)
                note = re.sub(frequency_pattern, r'<span class="drug-frequency">\g<0></span>', note)
                
                return note
            
            # Process the note
            annotated_note = process_note(user_note)
            
            # Display the result
            st.markdown(f"""
            <div class="annotation-result">
                {annotated_note}
            </div>
            """, unsafe_allow_html=True)
            
            # Display legend
            st.markdown("""
            <div style="margin-top: 1rem;">
                <h4>Legend:</h4>
                <span class="drug-name">Drug Names</span> | 
                <span class="drug-dosage">Dosages</span> | 
                <span class="drug-frequency">Frequencies</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Info about API
            st.info("Note: In a production environment, this would use the Gemini API with a medical prompt to perform more accurate extraction.")
        else:
            st.warning("Please enter a clinical note to process.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Integration guide
    st.markdown("<h3 style='margin-top: 2rem;'>How It Works</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>1. Input</h4>
            <p>Paste in your unstructured clinical notes containing medication information.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>2. Process</h4>
            <p>Our AI model analyzes the text to identify medications, dosages, frequencies, and routes.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>3. Result</h4>
            <p>View color-coded annotations that highlight the extracted medication information.</p>
        </div>
        """, unsafe_allow_html=True)

# Contact page
elif st.session_state.page == 'Contact':
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Get in Touch</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="padding: 2rem;">
            <h3>Contact Us</h3>
            <p>Have questions about MedAnnotate? We're here to help! Fill out the form and we'll get back to you as soon as possible.</p>
            <div style="margin-top: 2rem;">
                <h4>Email</h4>
                <p>info@medannotate.ai</p>
                
                <h4>Location</h4>
                <p>Harvard Medical School<br>Boston, MA</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='contact-form'>", unsafe_allow_html=True)
        with st.form("contact_form"):
            st.text_input("Name", placeholder="Your full name")
            st.text_input("Email", placeholder="Your email address")
            st.text_input("Subject", placeholder="What would you like to discuss?")
            st.text_area("Message", placeholder="How can we help you?", height=150)
            
            submit = st.form_submit_button("Send Message")
            if submit:
                st.success("Thank you for reaching out! We'll get back to you soon.")
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 MedAnnotate | Developed at Harvard DBMI</p>
</div>
""", unsafe_allow_html=True)

# Add functionality for Gemini API integration (commented out, replace with actual API key/implementation)
"""
def annotate_with_gemini(patient_note):
    # Replace with your actual Gemini API key and endpoint
    api_key = "YOUR_GEMINI_API_KEY"
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    
    prompt = f'''
    You are a medical assistant specialized in extracting medication information from clinical notes.
    Given the following patient note, identify:
    1. Drug names
    2. Dosage information
    3. Frequency information
    
    Format your response as JSON with the following structure:
    {{
        "annotations": [
            {{
                "drug": "drug name",
                "dosage": "dosage value",
                "frequency": "frequency value"
            }}
        ]
    }}
    
    Patient Note:
    {patient_note}
    '''
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    # Parse the response and extract the JSON
    try:
        text_response = result['candidates'][0]['content']['parts'][0]['text']
        # Extract JSON from the response
        json_start = text_response.find('{')
        json_end = text_response.rfind('}') + 1
        json_str = text_response[json_start:json_end]
        annotations = json.loads(json_str)
        return annotations
    except Exception as e:
        return {"error": str(e)}
"""