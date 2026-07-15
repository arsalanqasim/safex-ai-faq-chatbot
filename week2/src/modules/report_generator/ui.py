import streamlit as st
from .engine import generate_report

def render_ui():
    if "data" not in st.session_state:
        with st.spinner("Generating Report..."):
            st.session_state.data = generate_report()
    
    data = st.session_state.data 
        
    st.title("📊 SafeX AI Report Generator")

    st.write("Business Automation Research - Week 2")

    st.divider()

    col1,col2,col3,col4=st.columns(4)

    col1.metric("Projects",data["total_projects"])

    col2.metric("Completed",data["completed_projects"])

    col3.metric(
    "Completion %",
    f'{data["average_completion"]:.2f}%'
    )

    col4.metric(
    "Health Score",
    f'{data["health_score"]}/100'
    )

    st.divider()

    st.subheader("🤖 AI Insights")

    st.write(data["ai_report"])

    st.divider()

    st.subheader("📈 Charts")

    st.image(data["CHART_PATHS"]["status"])

    st.image(data["CHART_PATHS"]["department"])

    st.image(data["CHART_PATHS"]["risk"])

    st.image(data["CHART_PATHS"]["budget"])

    st.image(data["CHART_PATHS"]["satisfaction"])

    st.image(data["CHART_PATHS"]["completion"])

    st.image(data["CHART_PATHS"]["hours"])

    st.image(data["CHART_PATHS"]["completion_department"])

    st.divider()

    st.subheader("📄 Reports")

    with open(data["PDF_PATH"], "rb") as pdf:
        pdf_data = pdf.read()
        
    st.download_button(
    "Download PDF",
    pdf_data,
    file_name="Weekly_Business_Report.pdf",
    mime="application/pdf"
    )

    with open(data["TEXT_REPORT_PATH"],"r",encoding="utf-8") as txt:

        st.download_button(
            "Download Text Report",
            txt.read(),
            file_name="weekly_report.txt"
        )

    st.divider()

    st.subheader("Weekly Report")

    st.text(data["report"])