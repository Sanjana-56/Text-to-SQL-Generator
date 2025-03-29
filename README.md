# Text-to-SQL-Generator
AI-powered Natural Language to SQL query converter

# Talk to Your Database in Plain English 🗣️➡️🗃️

Convert everyday questions into MySQL queries instantly using AI. Designed for users who want to interact with databases without writing SQL manually.

**Problem Solved**: Reduces errors in manual SQL writing and speeds up data retrieval.

## Key Features
- **AI-Powered Translation**: Google Gemini converts natural language to SQL
- **Instant Results**: Execute queries and see tabular results immediately
- **MySQL Focused**: Works seamlessly with MySQL databases
- **Simple Interface**: User-friendly Streamlit web app

## Tech Stack
<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" height="25"> <img src="https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white" height="25"> <img src="https://img.shields.io/badge/Google_Gemini-4285F4?logo=google" height="25">

## How It Works
1. **Ask** a question:  
   *"Show patients with high cholesterol"*
2. **Get** auto-generated SQL:  
   ```sql
   SELECT name, cholesterol_level FROM patients 
   WHERE cholesterol_level > 200 
   ORDER BY cholesterol_level DESC;
3. **See** results displayed in a clean table
