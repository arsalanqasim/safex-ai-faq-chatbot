# ============================
# SECTION 1: IMPORT LIBRARIES
# ============================
import pandas as pd
import os
import google.generativeai as genai
import matplotlib
# Streamlit/Headless server par matplotlib GUI warning se bachne ke liye backend set karein
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import html
import re

from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import navy
from reportlab.lib.units import inch

# ============================
# UTILS: TEXT SANITIZATION FOR REPORTLAB
# ============================
def clean_text_for_pdf(text):
    """
    ReportLab PDF crash hone se bachane ke liye special characters escape karein
    aur markdown bold (**) ko ReportLab HTML tags (<b>) mein convert karein.
    """
    if not text:
        return ""
    # Safe HTML characters
    text = html.escape(text)
    # Convert markdown **bold** to ReportLab <b>bold</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Convert markdown *italic* to ReportLab <i>italic</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Convert bullets
    text = re.sub(r'^\s*[-*+]\s+(.*?)$', r'• \1', text, flags=re.MULTILINE)
    # Replace newlines with HTML breaks
    text = text.replace("\n", "<br/>")
    return text

# ============================
# SECTION 2: LOAD DATASET
# ============================
def generate_report():
    BASE_DIR = Path(__file__).resolve().parent
    dataset_path = BASE_DIR / "data" / "weekly_projects_40_enhanced.csv"
    
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Please check data path.")
        
    df = pd.read_csv(dataset_path)

    # ============================
    # SECTION 2.5: FOLDER MANAGEMENT
    # ============================
    print("\n========== FOLDER MANAGEMENT ==========")
    OUTPUT_DIR = BASE_DIR / "outputs"
    CHART_DIR = OUTPUT_DIR / "charts"
    REPORT_DIR = OUTPUT_DIR / "reports"
    LOG_DIR = BASE_DIR / "logs"

    # Create Required Folders
    folders = [OUTPUT_DIR, CHART_DIR, REPORT_DIR, LOG_DIR]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"✓ Folder Ready: {folder}")

    # File Paths Management
    PDF_PATH = REPORT_DIR / "Weekly_Business_Report.pdf"
    TEXT_REPORT_PATH = REPORT_DIR / "weekly_report.txt"

    # Chart Paths
    CHART_PATHS = {
        "status": CHART_DIR / "project_status_pie.png",
        "department": CHART_DIR / "projects_by_department.png",
        "risk": CHART_DIR / "risk_levels.png",
        "budget": CHART_DIR / "budget_vs_cost.png",
        "satisfaction": CHART_DIR / "client_satisfaction.png",
        "completion": CHART_DIR / "completion_distribution.png",
        "hours": CHART_DIR / "hours_worked.png",
        "completion_department": CHART_DIR / "completion_by_department.png"
    }

    # ============================
    # GEMINI CONFIGURATION
    # ============================
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # ============================
    # SECTION 4: CALCULATE KPIs
    # ============================
    total_projects = len(df)
    completed_projects = len(df[df["Status"] == "Completed"])
    in_progress_projects = len(df[df["Status"] == "In Progress"])
    pending_projects = len(df[df["Status"] == "Pending"])
    average_completion = df["Completion %"].mean()
    total_hours = df["Hours Worked"].sum()
    average_hours = df["Hours Worked"].mean()
    total_budget = df["Budget ($)"].sum()
    total_actual_cost = df["Actual Cost ($)"].sum()

    # Department Analysis
    department_projects = df["Department"].value_counts()
    department_completion = df.groupby("Department")["Completion %"].mean().round(2)
    department_satisfaction = df.groupby("Department")["Client Satisfaction"].mean().round(2)
    top_department = department_projects.idxmax()

    # Project Analysis
    top_project = df.loc[df["Completion %"].idxmax()]
    highest_budget = df.loc[df["Budget ($)"].idxmax()]
    highest_cost = df.loc[df["Actual Cost ($)"].idxmax()]
    best_rating = df.loc[df["Client Satisfaction"].idxmax()]
    delayed_projects = df[df["Delay (Days)"] > 0]
    high_risk_projects = df[df["Risk Level"] == "High"]

    budget_difference = total_budget - total_actual_cost
    risk_summary = df["Risk Level"].value_counts()
    on_time_projects = len(df[df["On Time"] == "Yes"])
    late_projects = len(df[df["On Time"] == "No"])

    average_rating = df["Client Satisfaction"].mean()
    highest_rating = df["Client Satisfaction"].max()
    lowest_rating = df["Client Satisfaction"].min()

    # ============================
    # SECTION X: DATA VISUALIZATION (Object-Oriented Matplotlib)
    # ============================
    print("\n========== GENERATING CHARTS ==========")

    # Chart 1: Status Pie Chart
    status_counts = df["Status"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(status_counts.values, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Project Status Distribution")
    fig.tight_layout()
    fig.savefig(CHART_PATHS["status"])
    plt.close(fig)

    # Chart 2: Projects by Department
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(department_projects.index, department_projects.values, color='royalblue')
    ax.set_title("Projects by Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Number of Projects")
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    for i, value in enumerate(department_projects.values):
        ax.text(i, value + 0.2, str(value), ha='center')
    fig.tight_layout()
    fig.savefig(CHART_PATHS["department"])
    plt.close(fig)

    # Chart 3: Risk Level Distribution
    risk_counts = df["Risk Level"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.bar(risk_counts.index, risk_counts.values, color='coral')
    ax.set_title("Risk Level Distribution")
    ax.set_xlabel("Risk Level")
    ax.set_ylabel("Projects")
    for i, value in enumerate(risk_counts.values):
        ax.text(i, value + 0.2, str(value), ha='center')
    fig.tight_layout()
    fig.savefig(CHART_PATHS["risk"])
    plt.close(fig)

    # Chart 4: Budget vs Actual Cost
    budget_data = {"Budget": total_budget, "Actual Cost": total_actual_cost}
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.bar(list(budget_data.keys()), list(budget_data.values()), color=['navy', 'crimson'])
    ax.set_title("Budget vs Actual Cost")
    ax.set_ylabel("Amount ($)")
    for i, value in enumerate(budget_data.values()):
        ax.text(i, value * 0.9, f"${value:,.0f}", ha='center', color='white', fontweight='bold')
    fig.tight_layout()
    fig.savefig(CHART_PATHS["budget"])
    plt.close(fig)

    # Chart 5: Client Satisfaction
    department_rating = df.groupby("Department")["Client Satisfaction"].mean()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(department_rating.index, department_rating.values, color='teal')
    ax.set_title("Average Client Satisfaction")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average Rating")
    ax.set_ylim(0, 5)
    for i, value in enumerate(department_rating.values):
        ax.text(i, value + 0.1, f"{value:.2f}", ha='center')
    fig.tight_layout()
    fig.savefig(CHART_PATHS["satisfaction"])
    plt.close(fig)

    # Chart 6: Completion Percentage
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(df["Completion %"], bins=10, color='mediumpurple', edgecolor='black')
    ax.set_title("Completion Percentage Distribution")
    ax.set_xlabel("Completion %")
    ax.set_ylabel("Projects")
    fig.tight_layout()
    fig.savefig(CHART_PATHS["completion"])
    plt.close(fig)

    # Chart 7: Hours Worked
    hours = df.groupby("Department")["Hours Worked"].sum()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(hours.index, hours.values, color='forestgreen')
    ax.set_title("Total Hours Worked by Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Hours")
    for i, value in enumerate(hours.values):
        ax.text(i, value + 5, str(int(value)), ha='center')
    fig.tight_layout()
    fig.savefig(CHART_PATHS["hours"])
    plt.close(fig)

    # Chart 8: Completion by Department
    completion = df.groupby("Department")["Completion %"].mean()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(completion.index, completion.values, color='darkorange')
    ax.set_title("Average Completion by Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Completion %")
    for i, value in enumerate(completion.values):
        ax.text(i, value + 1, f"{value:.1f}%", ha='center')
    fig.tight_layout()
    fig.savefig(CHART_PATHS["completion_department"])
    plt.close(fig)

    # ============================
    # AI REPORT ANALYSIS (Safe Health Score Calc)
    # ============================
    print("\n========== AI BUSINESS INSIGHTS ==========")
    on_time_ratio = (on_time_projects / total_projects) if total_projects > 0 else 0
    health_score = round(
        average_completion * 0.4 +
        average_rating * 20 * 0.3 +
        on_time_ratio * 100 * 0.3,
        2
    )

    business_prompt = f"""
    You are a Senior Business Analyst at SafeX Solutions.
    Analyze the following weekly business performance data and output a structured report containing:
    1. Executive Summary
    2. Performance Analysis
    3. Financial Analysis
    4. Risk Analysis
    5. Client Satisfaction Analysis
    6. Business Recommendations

    Data Summary:
    - Total Projects: {total_projects} (Completed: {completed_projects}, In Progress: {in_progress_projects}, Pending: {pending_projects})
    - Average Project Completion: {average_completion:.2f}%
    - Client Satisfaction Rating: {average_rating:.2f}/5 (High: {highest_rating}, Low: {lowest_rating})
    - Total Budget: ${total_budget:,.2f} vs Actual Cost: ${total_actual_cost:,.2f} (Diff: ${budget_difference:,.2f})
    - Delayed Projects: {len(delayed_projects)}, High Risk Projects: {len(high_risk_projects)}
    - Overall Project Health Score: {health_score}/100
    """

    # try:
    #     response = model.generate_content(business_prompt)
    #     ai_report = response.text
    # except Exception as e:
    #     ai_report = f"AI Analysis could not be generated. Error: {e}"

    try:
        response = model.generate_content(business_prompt)
        ai_report = response.text
        
    except Exception as e:
        import traceback
        traceback.print_exc()       
        print("MODEL:", model)      
        ai_report = f"AI Analysis could not be generated. Error: {e}"

    # Duplicate sections avoid karne ke liye unique Text Report banayein
    current_date = datetime.now().strftime("%d-%m-%Y")
    report = f"""============================================================
            SAFEX SOLUTIONS - BUSINESS METRICS REPORT
============================================================
Report Date: {current_date}
Overall Health Score: {health_score}/100

------------------------------------------------------------
KPI & STATISTICAL SUMMARY
------------------------------------------------------------
Total Projects          : {total_projects}
Completed Projects      : {completed_projects}
In Progress Projects    : {in_progress_projects}
Pending Projects        : {pending_projects}
Average Completion      : {average_completion:.2f}%
Total Hours Worked      : {total_hours}
Average Hours Worked    : {average_hours:.2f}

------------------------------------------------------------
FINANCIAL SUMMARY
------------------------------------------------------------
Total Budget            : ${total_budget:,.2f}
Total Actual Cost       : ${total_actual_cost:,.2f}
Budget Difference       : ${budget_difference:,.2f} ({'UNDER BUDGET' if budget_difference > 0 else 'OVER BUDGET'})

------------------------------------------------------------
TOP PERFORMING PROJECT
------------------------------------------------------------
Project Name            : {top_project['Project Name']}
Department              : {top_project['Department']}
Completion              : {top_project['Completion %']}%
Client Satisfaction     : {top_project['Client Satisfaction']} / 5

------------------------------------------------------------
AI ANALYSIS & EXECUTIVE INSIGHTS
------------------------------------------------------------
{ai_report}

============================================================
            END OF REPORT
============================================================
"""

    # ============================
    # GENERATE PDF REPORT
    # ============================
    print("\nGenerating Professional PDF Report...")
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        textColor=navy,
        fontSize=20,
        spaceAfter=15
    )
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    pdf = SimpleDocTemplate(str(PDF_PATH))
    elements = []

    # Title & Metadata
    elements.append(Paragraph("SafeX Solutions - Weekly Business Report", title_style))
    elements.append(Paragraph(f"<b>Report Date:</b> {current_date} | <b>Health Score:</b> {health_score}/100", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # AI Report Section (HTML clean functions wrap taake parser fail na ho)
    elements.append(Paragraph("AI Business Insights", heading_style))
    safe_ai_text = clean_text_for_pdf(ai_report)
    elements.append(Paragraph(safe_ai_text, normal_style))
    elements.append(Spacer(1, 0.25 * inch))

    # Add Charts
    elements.append(Paragraph("Visual Performance Charts", heading_style))
    chart_keys = ["status", "department", "risk", "budget", "satisfaction", "completion", "hours", "completion_department"]
    
    for key in chart_keys:
        chart_path = CHART_PATHS[key]
        if chart_path.exists():
            try:
                img = Image(str(chart_path))
                img.drawHeight = 3.2 * inch
                img.drawWidth = 5.0 * inch
                elements.append(img)
                elements.append(Spacer(1, 0.15 * inch))
            except Exception as chart_err:
                print(f"Error appending chart {key}: {chart_err}")

    # Build PDF
    try:
        pdf.build(elements)
        print("✅ PDF Generated Successfully!")
    except Exception as e:
        print("PDF ERROR:", e)
        raise

    # Save TXT Report
    with open(str(TEXT_REPORT_PATH), "w", encoding="utf-8") as file:
        file.write(report)

    return {
        "total_projects": total_projects,
        "completed_projects": completed_projects,
        "average_completion": average_completion,
        "health_score": health_score,
        "ai_report": ai_report,
        "report": report,
        "PDF_PATH": str(PDF_PATH),
        "TEXT_REPORT_PATH": str(TEXT_REPORT_PATH),
        "CHART_PATHS": {k: str(v) for k, v in CHART_PATHS.items()}
    }