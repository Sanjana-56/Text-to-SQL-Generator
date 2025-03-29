from dotenv import load_dotenv
import streamlit as st
import os
import mysql.connector
import pandas as pd
import google.generativeai as genai

# Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Database Connection
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="healthcare_db"
        )
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        st.stop()

# AI Response Generation
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    try:
        response = model.generate_content([prompt[0], question])
        return response.text
    except Exception as e:
        st.error(f"AI Error: {str(e)}")
        st.stop()

# Query Execution
def execute_sql_query(sql_query):
    sql_query = sql_query.strip().strip("```sql").strip("```")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return columns, rows
        return None, None
        
    except mysql.connector.Error as err:
        st.error(f"SQL Error: {err}")
        return None, None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Streamlit UI
def main():
    st.set_page_config(page_title="Healthcare Analytics", layout="wide")
    st.title("🏥 Smart Healthcare Data Explorer")
    
    prompt = [
        """You are a healthcare SQL expert. Database schema:
        PATIENTS (patient_id, first_name, last_name, dob, gender, phone, insurance_id)
        DOCTORS (doctor_id, first_name, last_name, specialization, department_id, license_number, phone)
        DEPARTMENTS (department_id, name, head_doctor_id)
        APPOINTMENTS (appointment_id, patient_id, doctor_id, appointment_date, status)
        MEDICAL_RECORDS (record_id, patient_id, doctor_id, diagnosis, prescription, record_date)
        LAB_RESULTS (lab_id, patient_id, test_name, test_date, result_value, reference_range)
        
        Rules:
        1. Use explicit JOIN syntax
        2. Format dates using DATE_FORMAT()
        3. Always qualify column names with table aliases
        4. Include relevant WHERE clauses
        5. Handle NULL values appropriately"""
    ]
    
    question = st.text_area("Enter your healthcare data question:", 
                          placeholder="e.g., Show patients with cholesterol levels above 200 mg/dL",
                          height=100)
    
    if st.button("Analyze Data"):
        if not question:
            st.warning("Please enter a question")
            return
            
        with st.spinner("🔍 Analyzing medical data..."):
            try:
                # Generate and execute query
                sql = get_gemini_response(question, prompt)
                columns, data = execute_sql_query(sql)
                
                # Display results
                st.subheader("Generated SQL Query")
                st.code(sql, language="sql")
                
                if columns and data:
                    st.subheader("Analysis Results")
                    df = pd.DataFrame(data, columns=columns)
                    st.dataframe(df, use_container_width=True)
                    
                    # Basic visualizations
                    if len(df) > 0:
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        if not numeric_cols.empty:
                            selected_col = st.selectbox("Select column to visualize:", numeric_cols)
                            st.line_chart(df[selected_col])
                else:
                    st.info("No results found for this query")
                    
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")
    
    # Sample questions sidebar
    with st.sidebar:
        st.markdown("### 💡 Sample Questions")
        st.write("- List patients with cholesterol above 200 mg/dL")
        st.write("- Show average lab results by test type")
        st.write("- Find doctors with most appointments this month")
        st.write("- Patients with multiple prescriptions in March 2024")
        st.write("- Upcoming appointments for cardiology department")

if __name__ == "__main__":
    main()