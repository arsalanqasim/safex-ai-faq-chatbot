import streamlit as st
import os
from .engine import generate_report

def render_ui():
    # Injected Premium Custom CSS for "Wow Factor" (Dark Modern Theme)
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #f8fafc;
        }
        /* Style Metric Cards */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 15px 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            border-color: #6366f1;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.25);
        }
        /* Buttons styling */
        .stButton>button {
            background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);
            transition: all 0.3s;
        }
        .stButton>button:hover {
            opacity: 0.9;
            transform: scale(1.02);
            box-shadow: 0 6px 15px rgba(79, 70, 229, 0.5);
        }
        /* Styled header divider */
        .header-divider {
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
            border-radius: 2px;
            margin-bottom: 25px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/combo-chart.png", width=70)
        st.title("Settings")
        st.write("SafeX Solutions Business Analytics")
        st.markdown("---")
        
        # Refresh Data Button
        if st.button("🔄 Refresh / Re-run Report"):
            if "data" in st.session_state:
                del st.session_state.data
            st.rerun()

    # Main Page UI
    st.title("📊 SafeX AI Report Generator")
    st.write(f"Debug File Path: {generate_report.__code__.co_filename}")
    st.markdown("##### *Business Automation Research - Week 2 Component*")
    st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

    # Lazy-loading/Caching mechanism
    if "data" not in st.session_state:
        with st.spinner("Generating Reports & Running Gemini AI Analysis..."):
            try:
                st.session_state.data = generate_report()
            except Exception as e:
                st.error(f"Failed to generate report: {e}")
                return
    
    data = st.session_state.data

    # Metric Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Projects", data["total_projects"])
    col2.metric("Completed", data["completed_projects"])
    col3.metric("Average Completion %", f'{data["average_completion"]:.2f}%')
    col4.metric("Operational Health", f'{data["health_score"]}/100')

    st.markdown("---")

    # Tabs for Clean visual layout
    tab_summary, tab_charts, tab_ai, tab_downloads = st.tabs([
        "📄 Weekly Report Summary", 
        "📈 Performance Charts", 
        "🤖 AI Analyst Insights", 
        "📥 Download PDF & Reports"
    ])

    with tab_summary:
        st.subheader("📝 Text Operations Report")
        st.text_area("Live Report View", data["report"], height=400)

    with tab_charts:
        st.subheader("📊 Visual Performance Analytics")
        # Layout charts into clean 2-column grid instead of a single long column
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.image(data["CHART_PATHS"]["status"], use_container_width=True, caption="Project Status")
            st.image(data["CHART_PATHS"]["risk"], use_container_width=True, caption="Risk Levels")
            st.image(data["CHART_PATHS"]["satisfaction"], use_container_width=True, caption="Client Satisfaction")
            st.image(data["CHART_PATHS"]["hours"], use_container_width=True, caption="Hours Worked")
        with col_c2:
            st.image(data["CHART_PATHS"]["department"], use_container_width=True, caption="Projects by Department")
            st.image(data["CHART_PATHS"]["budget"], use_container_width=True, caption="Budget vs Actual Cost")
            st.image(data["CHART_PATHS"]["completion"], use_container_width=True, caption="Completion % Distribution")
            st.image(data["CHART_PATHS"]["completion_department"], use_container_width=True, caption="Completion by Department")

    with tab_ai:
        st.subheader("🤖 Gemini Business Analyst Recommendations")
        # Format the AI output with markdown inside Streamlit safely
        st.markdown(data["ai_report"])

    with tab_downloads:
        st.subheader("💾 Export & Downloads")
        st.write("Generate and download offline report formats:")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            if os.path.exists(data["PDF_PATH"]):
                with open(data["PDF_PATH"], "rb") as pdf:
                    pdf_data = pdf.read()
                st.download_button(
                    label="📥 Download Executive PDF Report",
                    data=pdf_data,
                    file_name="Weekly_Business_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.error("PDF file not found.")

        with col_d2:
            if os.path.exists(data["TEXT_REPORT_PATH"]):
                with open(data["TEXT_REPORT_PATH"], "r", encoding="utf-8") as txt:
                    text_data = txt.read()
                st.download_button(
                    label="📥 Download Plain Text Report",
                    data=text_data,
                    file_name="weekly_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.error("Text report file not found.")