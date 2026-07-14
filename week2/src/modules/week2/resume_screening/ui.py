import streamlit as st
from src.modules.registry import MODULE_REGISTRY
from src.modules.week2.resume_screening.engine import ResumeScreeningEngineStub

def render_ui():
    """Renders the Streamlit frontend tab for Resume Screening Prototype."""
    metadata = MODULE_REGISTRY["week2"]["resume_screening"]
    
    st.markdown(f'''
    <div class="hero-wrap">
        <div class="hero-badge">⚙️ Business Automation Suite</div>
        <div class="hero-title">{metadata["title"]}</div>
        <div class="hero-subtitle">
            Assigned to: <strong>{metadata["developer"]}</strong> ({metadata["role"]})
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Info Details Box
    st.info(
        f"**Developer E-mail:** {metadata['email']}  \n"
        f"**Difficulty Level:** {metadata['difficulty']}  \n"
        f"**Required Stack:** {', '.join(metadata['tech'])}"
    )
    
    st.subheader("Objective & Scope")
    st.write(metadata["description"])
    
    st.markdown("---")
    
    # Warning Notice
    st.warning("⚠️ **Notice:** This is a placeholder scaffolding tab. No actual business automation logic has been implemented. Implementation is pending developer assignment.")
    
    # Interactive Mock Console
    st.write("### Interactive Mock Console")
    mock_input = st.text_input("Simulated Input Data", placeholder="Enter dummy data to test UI elements...")
    
    if st.button("Trigger Test Run", key="trigger_resume_screening"):
        if mock_input:
            engine = ResumeScreeningEngineStub()
            result = engine.run_stub_process(mock_input)
            st.success("Successfully processed simulated input using engine stub!")
            st.json(result)
        else:
            st.error("Please enter simulated input data first.")
