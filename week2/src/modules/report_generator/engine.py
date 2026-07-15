# ============================
# SECTION 1: IMPORT LIBRARIES
# ============================
import pandas as pd
import os
import google.generativeai as genai
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

from reportlab.platypus import *
from reportlab.lib.styles import *
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import navy
from reportlab.lib.units import inch

# ============================
# SECTION 2: LOAD DATASET
# ============================

def generate_report():

    dataset_path = "data/weekly_projects_40_enhanced.csv"

    df = pd.read_csv(dataset_path)

    # ============================
    # SECTION 2.5: FOLDER MANAGEMENT
    # ============================


    print("\n========== FOLDER MANAGEMENT ==========")


    # Main Project Directory

    BASE_DIR = Path(__file__).parent


    # Output Directory

    OUTPUT_DIR = BASE_DIR / "outputs"


    # Chart Directory

    CHART_DIR = OUTPUT_DIR / "charts"


    # Report Directory

    REPORT_DIR = OUTPUT_DIR / "reports"


    # Logs Directory

    LOG_DIR = BASE_DIR / "logs"



    # Create Required Folders

    folders = [

        BASE_DIR,

        OUTPUT_DIR,

        CHART_DIR,

        REPORT_DIR,

        LOG_DIR

    ]


    for folder in folders:

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        print(
            f"✓ Folder Ready: {folder}"
        )



    # File Paths Management


    PDF_PATH = REPORT_DIR / "Weekly_Business_Report.pdf"


    TEXT_REPORT_PATH = REPORT_DIR / "weekly_report.txt"



    # Chart Paths

    CHART_PATHS = {


    "status":
    CHART_DIR / "project_status_pie.png",


    "department":
    CHART_DIR / "projects_by_department.png",


    "risk":
    CHART_DIR / "risk_levels.png",


    "budget":
    CHART_DIR / "budget_vs_cost.png",


    "satisfaction":
    CHART_DIR / "client_satisfaction.png",


    "completion":
    CHART_DIR / "completion_distribution.png",


    "hours":
    CHART_DIR / "hours_worked.png",


    "completion_department":
    CHART_DIR / "completion_by_department.png"


    }



    print("\n✅ Folder Structure Created Successfully!")

    print("\nProject Structure:")

    print(
    f"""

    {BASE_DIR}/

    │
    ├── outputs/
    │     │
    │     ├── charts/
    │     │
    │     └── reports/
    │
    └── logs/

    """
    )

    # ============================
    # GEMINI CONFIGURATION
    # ============================

    load_dotenv()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel("gemini-2.5-flash")

    print("✅ Dataset Loaded Successfully!")

    # ============================
    # SECTION 3: DISPLAY DATASET INFORMATION
    # ============================

    print("\n========== FIRST 5 ROWS ==========")
    print(df.head())

    print("\n========== DATASET INFORMATION ==========")
    print(df.info())

    print("\n========== NUMERICAL SUMMARY ==========")
    print(df.describe())

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

    print("\n========== KEY PERFORMANCE INDICATORS ==========")

    print(f"Total Projects: {total_projects}")

    print(f"Completed Projects: {completed_projects}")

    print(f"In Progress Projects: {in_progress_projects}")

    print(f"Pending Projects: {pending_projects}")

    print(f"Average Completion: {average_completion:.2f}%")

    print(f"Total Hours Worked: {total_hours}")

    print(f"Average Hours Worked: {average_hours:.2f}")

    print(f"Total Budget: ${total_budget:,.2f}")

    print(f"Total Actual Cost: ${total_actual_cost:,.2f}")

    # ============================
    # SECTION 5: DEPARTMENT ANALYSIS
    # ============================

    print("\n========== DEPARTMENT ANALYSIS ==========")

    # Total projects in each department
    department_projects = df["Department"].value_counts()

    print("\nProjects by Department:")
    print(department_projects)

    # Average completion percentage by department
    department_completion = df.groupby("Department")["Completion %"].mean().round(2)

    print("\nAverage Completion by Department:")
    print(department_completion)

    # Average client satisfaction by department
    department_satisfaction = df.groupby("Department")["Client Satisfaction"].mean().round(2)

    print("\nAverage Client Satisfaction by Department:")
    print(department_satisfaction)

    # Department with maximum projects
    top_department = department_projects.idxmax()

    print(f"\nDepartment with Highest Number of Projects: {top_department}")

    # ============================
    # SECTION 6: PROJECT ANALYSIS
    # ============================

    print("\n========== PROJECT ANALYSIS ==========")

    # Top project based on completion percentage
    top_project = df.loc[df["Completion %"].idxmax()]

    print("\nTop Performing Project:")
    print(f"Project Name       : {top_project['Project Name']}")
    print(f"Department         : {top_project['Department']}")
    print(f"Completion         : {top_project['Completion %']}%")
    print(f"Client Satisfaction: {top_project['Client Satisfaction']}")

    # Project with highest budget
    highest_budget = df.loc[df["Budget ($)"].idxmax()]

    print("\nHighest Budget Project:")
    print(f"Project Name : {highest_budget['Project Name']}")
    print(f"Budget       : ${highest_budget['Budget ($)']:,.2f}")

    # Project with highest actual cost
    highest_cost = df.loc[df["Actual Cost ($)"].idxmax()]

    print("\nHighest Actual Cost Project:")
    print(f"Project Name : {highest_cost['Project Name']}")
    print(f"Actual Cost  : ${highest_cost['Actual Cost ($)']:,.2f}")

    # Project with highest client satisfaction
    best_rating = df.loc[df["Client Satisfaction"].idxmax()]

    print("\nHighest Client Satisfaction:")
    print(f"Project Name : {best_rating['Project Name']}")
    print(f"Rating       : {best_rating['Client Satisfaction']} / 5")

    # Delayed projects
    delayed_projects = df[df["Delay (Days)"] > 0]

    print(f"\nDelayed Projects : {len(delayed_projects)}")

    # High-risk projects
    high_risk_projects = df[df["Risk Level"] == "High"]

    print(f"High Risk Projects : {len(high_risk_projects)}")

    # ============================
    # SECTION 7: BUDGET & COST ANALYSIS
    # ============================

    print("\n========== BUDGET ANALYSIS ==========")

    budget_difference = total_budget - total_actual_cost

    print(f"Total Budget      : ${total_budget:,.2f}")
    print(f"Total Actual Cost : ${total_actual_cost:,.2f}")
    print(f"Budget Difference : ${budget_difference:,.2f}")

    if budget_difference > 0:
        print("\nStatus : Project is UNDER budget.")
    elif budget_difference < 0:
        print("\nStatus : Project is OVER budget.")
    else:
        print("\nStatus : Project is ON budget.")

    # ============================
    # SECTION 8: RISK ANALYSIS
    # ============================

    print("\n========== RISK ANALYSIS ==========")

    risk_summary = df["Risk Level"].value_counts()

    print(risk_summary)

    on_time_projects = len(df[df["On Time"] == "Yes"])

    late_projects = len(df[df["On Time"] == "No"])

    print(f"\nProjects Delivered On Time : {on_time_projects}")

    print(f"Projects Delivered Late    : {late_projects}")

    # ============================
    # SECTION 9: CLIENT SATISFACTION ANALYSIS
    # ============================

    print("\n========== CLIENT SATISFACTION ==========")

    average_rating = df["Client Satisfaction"].mean()

    highest_rating = df["Client Satisfaction"].max()

    lowest_rating = df["Client Satisfaction"].min()

    print(f"Average Rating : {average_rating:.2f} / 5")

    print(f"Highest Rating : {highest_rating}")

    print(f"Lowest Rating  : {lowest_rating}")





    # ============================
    # SECTION X: DATA VISUALIZATION
    # ============================

    print("\n========== GENERATING CHARTS ==========")

    # ---------------------------------
    # Chart 1: Project Status Pie Chart
    # ---------------------------------

    status_counts = df["Status"].value_counts()

    plt.figure(figsize=(7,7))
    plt.pie(
        status_counts.values,
        labels=status_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Project Status Distribution")
    plt.tight_layout()
    plt.savefig(CHART_PATHS["status"])
    plt.close()

    print("✓ Project Status Pie Chart Saved")

    # ---------------------------------
    # Chart 2: Projects by Department
    # ---------------------------------

    department_projects = df["Department"].value_counts()

    plt.figure(figsize=(9,5))
    plt.bar(
        department_projects.index,
        department_projects.values
    )

    plt.title("Projects by Department")
    plt.xlabel("Department")
    plt.ylabel("Number of Projects")
    plt.xticks(rotation=25)

    for i, value in enumerate(department_projects.values):
        plt.text(i, value+0.2, str(value), ha='center')

    plt.tight_layout()
    plt.savefig(CHART_PATHS["department"])
    plt.close()

    print("✓ Department Chart Saved")

    # ---------------------------------
    # Chart 3: Risk Level Distribution
    # ---------------------------------

    risk_counts = df["Risk Level"].value_counts()

    plt.figure(figsize=(7,5))
    plt.bar(
        risk_counts.index,
        risk_counts.values
    )

    plt.title("Risk Level Distribution")
    plt.xlabel("Risk Level")
    plt.ylabel("Projects")

    for i, value in enumerate(risk_counts.values):
        plt.text(i, value+0.2, str(value), ha='center')

    plt.tight_layout()
    plt.savefig(CHART_PATHS["risk"])
    plt.close()

    print("✓ Risk Chart Saved")

    # ---------------------------------
    # Chart 4: Budget vs Actual Cost
    # ---------------------------------

    budget_data = {
        "Budget": total_budget,
        "Actual Cost": total_actual_cost
    }

    plt.figure(figsize=(6,5))
    plt.bar(
        budget_data.keys(),
        budget_data.values()
    )

    plt.title("Budget vs Actual Cost")
    plt.ylabel("Amount ($)")

    for i, value in enumerate(budget_data.values()):
        plt.text(i, value, f"${value:,.0f}", ha='center')

    plt.tight_layout()
    plt.savefig(CHART_PATHS["budget"])
    plt.close()

    print("✓ Budget Comparison Chart Saved")

    # ---------------------------------
    # Chart 5: Client Satisfaction
    # ---------------------------------

    department_rating = df.groupby("Department")["Client Satisfaction"].mean()

    plt.figure(figsize=(9,5))
    plt.bar(
        department_rating.index,
        department_rating.values
    )

    plt.title("Average Client Satisfaction")
    plt.xlabel("Department")
    plt.ylabel("Average Rating")

    plt.ylim(0,5)

    for i, value in enumerate(department_rating.values):
        plt.text(i, value+0.05, f"{value:.2f}", ha='center')

    plt.tight_layout()
    plt.savefig(CHART_PATHS["satisfaction"])
    plt.close()

    print("✓ Client Satisfaction Chart Saved")

    # ---------------------------------
    # Chart 6: Completion Percentage
    # ---------------------------------

    plt.figure(figsize=(8,5))

    plt.hist(
        df["Completion %"],
        bins=10
    )

    plt.title("Completion Percentage Distribution")
    plt.xlabel("Completion %")
    plt.ylabel("Projects")

    plt.tight_layout()
    plt.savefig(CHART_PATHS["completion"])
    plt.close()

    print("✓ Completion Distribution Saved")

    # ---------------------------------
    # Chart 7: Hours Worked
    # ---------------------------------

    hours = df.groupby("Department")["Hours Worked"].sum()

    plt.figure(figsize=(9,5))
    plt.bar(
        hours.index,
        hours.values
    )

    plt.title("Total Hours Worked by Department")
    plt.xlabel("Department")
    plt.ylabel("Hours")

    for i, value in enumerate(hours.values):
        plt.text(i, value+1, str(int(value)), ha='center')

    plt.tight_layout()
    plt.savefig(CHART_PATHS["hours"])
    plt.close()

    print("✓ Hours Worked Chart Saved")

    # ---------------------------------
    # Chart 8: Completion by Department
    # ---------------------------------

    completion = df.groupby("Department")["Completion %"].mean()

    plt.figure(figsize=(9,5))
    plt.bar(
        completion.index,
        completion.values
    )

    plt.title("Average Completion by Department")
    plt.xlabel("Department")
    plt.ylabel("Completion %")

    for i, value in enumerate(completion.values):
        plt.text(i, value+1, f"{value:.1f}%", ha='center')

    plt.tight_layout()
    plt.savefig(CHART_PATHS["completion_department"])
    plt.close()

    print("✓ Completion Chart Saved")

    print("\n✅ All Charts Generated Successfully!")
    print("📁 Saved in outputs/charts/")



    # ============================
    # AI REPORT ANALYSIS
    # ============================


    print("\n========== AI BUSINESS INSIGHTS ==========")


    # Calculate Business Health Score

    health_score = round(
        average_completion * 0.4 +
        average_rating * 20 * 0.3 +
        (on_time_projects / total_projects) * 100 * 0.3,
        2
    )


    business_prompt = f"""

    You are a Senior Business Analyst at SafeX Solutions.

    Analyze the following weekly business performance data.

    Business Performance:

    Total Projects:
    {total_projects}

    Completed Projects:
    {completed_projects}

    Projects In Progress:
    {in_progress_projects}

    Pending Projects:
    {pending_projects}


    Project Completion:

    Average Completion:
    {average_completion:.2f}%


    Client Satisfaction:

    Average Client Rating:
    {average_rating:.2f}/5


    Financial Performance:

    Total Budget:
    ${total_budget:,.2f}

    Actual Cost:
    ${total_actual_cost:,.2f}

    Budget Difference:
    ${budget_difference:,.2f}


    Risk Analysis:

    Delayed Projects:
    {len(delayed_projects)}

    High Risk Projects:
    {len(high_risk_projects)}


    Overall Business Health Score:

    {health_score}/100


    Generate a professional business report containing:


    1. Executive Summary

    2. Performance Analysis

    3. Financial Analysis

    4. Risk Analysis

    5. Client Satisfaction Analysis

    6. Business Recommendations


    Use professional language suitable for management.

    """


    try:

        response = model.generate_content(
            business_prompt
        )

        ai_report = response.text


    except Exception as e:


        ai_report = f"""

    AI Analysis could not be generated.

    Error:

    {e}

    """


    print(ai_report)

    # Extract AI report as recommendations
    recommendations = [
        ai_report
    ]

    # Use AI report as executive summary
    executive_summary = ai_report

    # ============================
    # SECTION 10: GENERATE WEEKLY REPORT
    # ============================

    current_date = datetime.now().strftime("%d-%m-%Y")

    report = f"""
    ============================================================
                SAFEX SOLUTIONS
        WEEKLY BUSINESS OPERATIONS REPORT
    ============================================================

    Report Date: {current_date}

    ------------------------------------------------------------
    EXECUTIVE SUMMARY
    ------------------------------------------------------------

    {executive_summary}

    ------------------------------------------------------------
    KEY PERFORMANCE INDICATORS (KPIs)
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
    Budget Difference       : ${budget_difference:,.2f}

    ------------------------------------------------------------
    CLIENT SATISFACTION
    ------------------------------------------------------------

    Average Rating          : {average_rating:.2f} / 5

    ------------------------------------------------------------
    PROJECT STATUS
    ------------------------------------------------------------

    High Risk Projects      : {len(high_risk_projects)}
    Delayed Projects        : {len(delayed_projects)}

    Projects Delivered On Time : {on_time_projects}
    Projects Delivered Late    : {late_projects}

    ------------------------------------------------------------
    TOP PERFORMING PROJECT
    ------------------------------------------------------------

    Project Name            : {top_project['Project Name']}
    Department              : {top_project['Department']}
    Completion              : {top_project['Completion %']}%
    Client Satisfaction     : {top_project['Client Satisfaction']} / 5

    ------------------------------------------------------------
    RECOMMENDATIONS
    ------------------------------------------------------------

    {chr(10).join(recommendations)}

    ------------------------------------------------------------
    AI GENERATED BUSINESS ANALYSIS
    ------------------------------------------------------------

    {ai_report}

    ------------------------------------------------------------
    PROJECT HEALTH SCORE
    ------------------------------------------------------------

    Overall Health Score    : {health_score}/100

    ------------------------------------------------------------
    CONCLUSION
    ------------------------------------------------------------

    Overall, the organization demonstrated strong project execution
    during the reporting period. Most projects are progressing well,
    client satisfaction remains positive, and financial performance
    is within acceptable limits.

    ============================================================
                END OF WEEKLY REPORT
    ============================================================
    """

    # ============================
    # SECTION 10.5
    # GENERATE PDF REPORT (PART 1)
    # ============================

    print("\nGenerating Professional PDF Report...")

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        textColor=navy,
        fontSize=22,
        spaceAfter=20
    )

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]

    pdf = SimpleDocTemplate(
        PDF_PATH
    )

    elements = []

    # -----------------------------------
    # Title
    # -----------------------------------

    elements.append(
        Paragraph(
            "SafeX Solutions<br/>Weekly Business Report",
            title_style
        )
    )

    elements.append(Spacer(1,0.25*inch))

    # -----------------------------------
    # Report Date
    # -----------------------------------

    elements.append(
        Paragraph(
            f"<b>Report Date:</b> {current_date}",
            normal_style
        )
    )

    elements.append(Spacer(1,0.25*inch))

    # -----------------------------------
    # Executive Summary
    # -----------------------------------

    elements.append(
        Paragraph(
            "Executive Summary",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            executive_summary.replace("\n","<br/>"),
            normal_style
        )
    )

    elements.append(
        Spacer(1,0.25*inch)
    )

    # -----------------------------------
    # KPI Section
    # -----------------------------------

    elements.append(
        Paragraph(
            "Key Performance Indicators",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Total Projects:</b> {total_projects}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Completed Projects:</b> {completed_projects}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Projects In Progress:</b> {in_progress_projects}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Pending Projects:</b> {pending_projects}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Average Completion:</b> {average_completion:.2f}%",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Total Hours Worked:</b> {total_hours}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Average Hours Worked:</b> {average_hours:.2f}",
            normal_style
        )
    )

    elements.append(
        Spacer(1,0.25*inch)
    )

    # -----------------------------------
    # Financial Summary
    # -----------------------------------

    elements.append(
        Paragraph(
            "Financial Summary",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Total Budget:</b> ${total_budget:,.2f}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Total Actual Cost:</b> ${total_actual_cost:,.2f}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Budget Difference:</b> ${budget_difference:,.2f}",
            normal_style
        )
    )

    elements.append(
        Spacer(1,0.3*inch)
    )

    # -----------------------------------
    # AI Insights
    # -----------------------------------

    elements.append(
        Paragraph(
            "AI Insights & Recommendations",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Overall Health Score:</b> {health_score}/100",
            normal_style
        )
    )

    elements.append(Spacer(1,0.10*inch))

    for recommendation in recommendations:
        elements.append(
            Paragraph(
                recommendation,
                normal_style
            )
        )

    elements.append(Spacer(1,0.25*inch))

    # -----------------------------------
    # Client Satisfaction
    # -----------------------------------

    elements.append(
        Paragraph(
            "Client Satisfaction",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Average Rating:</b> {average_rating:.2f} / 5",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Highest Rating:</b> {highest_rating}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Lowest Rating:</b> {lowest_rating}",
            normal_style
        )
    )

    elements.append(Spacer(1,0.25*inch))

    # -----------------------------------
    # Top Performing Project
    # -----------------------------------

    elements.append(
        Paragraph(
            "Top Performing Project",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Project Name:</b> {top_project['Project Name']}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Department:</b> {top_project['Department']}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Completion:</b> {top_project['Completion %']}%",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Client Satisfaction:</b> {top_project['Client Satisfaction']} / 5",
            normal_style
        )
    )

    elements.append(Spacer(1,0.30*inch))

    # -----------------------------------
    # Add Charts
    # -----------------------------------

    from reportlab.platypus import Image

    chart_files = [

        CHART_PATHS["status"],

        CHART_PATHS["department"],

        CHART_PATHS["risk"],

        CHART_PATHS["budget"],

        CHART_PATHS["satisfaction"],

        CHART_PATHS["completion"],

        CHART_PATHS["hours"],

        CHART_PATHS["completion_department"]

    ]

    elements.append(
        Paragraph(
            "Generated Charts",
            heading_style
        )
    )

    for chart in chart_files:

        if os.path.exists(chart):

            try:

                img = Image(chart)

                img.drawHeight = 3.8 * inch
                img.drawWidth = 5.8 * inch

                elements.append(img)

                elements.append(Spacer(1,0.20*inch))

            except Exception:

                pass

    # -----------------------------------
    # Conclusion
    # -----------------------------------

    elements.append(
        Paragraph(
            "Conclusion",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            """
            The generated report provides a comprehensive overview of
            weekly business performance. Key Performance Indicators,
            financial statistics, project performance, client satisfaction,
            risk analysis and AI-generated recommendations help management
            make informed business decisions quickly.
            """,
            normal_style
        )
    )

    elements.append(Spacer(1,0.30*inch))

    # -----------------------------------
    # Footer
    # -----------------------------------

    elements.append(
        Paragraph(
            "<b>Generated Automatically using Python AI Report Generator Prototype</b>",
            normal_style
        )
    )

    # -----------------------------------
    # Build PDF
    # -----------------------------------

    pdf.build(elements)

    print("✅ PDF Report Generated Successfully!")
    print("📄 File Saved As : Weekly_Business_Report.pdf")



    # ============================
    # SECTION 11: SAVE REPORT
    # ============================

    with open(TEXT_REPORT_PATH, "w", encoding="utf-8") as file:
        file.write(report)

    print("\n✅ Weekly Report Generated Successfully!")
    print("📄 File Saved As: weekly_report.txt")

    # ============================
    # SECTION 12: DISPLAY REPORT
    # ============================

    print(report)
    
    return {
        "total_projects": total_projects,
        "completed_projects": completed_projects,
        "average_completion": average_completion,
        "health_score": health_score,
        "ai_report": ai_report,
        "report": report,
        "PDF_PATH": PDF_PATH,
        "TEXT_REPORT_PATH": TEXT_REPORT_PATH,
        "CHART_PATHS": CHART_PATHS
    }
    