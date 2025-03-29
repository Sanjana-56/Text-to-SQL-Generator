import mysql.connector

def create_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS healthcare_db")
        cursor.execute("USE healthcare_db")
        print("Database created successfully")
        return connection
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
        exit(1)

def create_tables(connection):
    tables = [
        """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            dob DATE NOT NULL,
            gender ENUM('Male', 'Female', 'Other'),
            phone VARCHAR(15),
            insurance_id VARCHAR(20)
        )
        """,
        """
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        specialization VARCHAR(50),
        department_id INT,
        license_number VARCHAR(20),
        phone VARCHAR(15)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS departments (
        department_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        head_doctor_id INT)
    """,
    """
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        doctor_id INT,
        appointment_date DATETIME,
        status ENUM('Scheduled', 'Completed', 'Cancelled'),
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS medical_records (
        record_id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        doctor_id INT,
        diagnosis TEXT,
        prescription TEXT,
        record_date DATE,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS lab_results (
        lab_id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        test_name VARCHAR(100),
        test_date DATE,
        result_value DECIMAL(10,2),
        reference_range VARCHAR(50),
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
    )
    """
        
    ]
    
    try:
        cursor = connection.cursor()
        for table in tables:
            cursor.execute(table)
        connection.commit()
        print("Tables created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
        exit(1)

def insert_sample_data(connection):
    sample_data = [
        # Departments
    """INSERT INTO departments (name) VALUES 
    ('Cardiology'), ('Pediatrics'), ('Oncology')""",
    
    # Doctors
    """INSERT INTO doctors (first_name, last_name, specialization, department_id) VALUES
    ('Emily', 'White', 'Cardiologist', 1),
    ('Raj', 'Patel', 'Pediatrician', 2),
    ('Sophia', 'Lee', 'Oncologist', 3)""",
    
    # Patients
    """INSERT INTO patients (first_name, last_name, dob, gender, insurance_id) VALUES
    ('Alice', 'Johnson', '1990-05-15', 'Female', 'INS-12345'),
    ('Bob', 'Smith', '1985-12-22', 'Male', 'INS-67890'),
    ('Charlie', 'Brown', '2000-03-08', 'Other', 'INS-11223')""",
    
    # Appointments
    """INSERT INTO appointments (patient_id, doctor_id, appointment_date, status) VALUES
    (1, 1, '2024-03-20 10:00:00', 'Completed'),
    (2, 2, '2024-03-21 14:30:00', 'Scheduled')""",
    
    # Medical Records
    """INSERT INTO medical_records (patient_id, doctor_id, diagnosis, prescription, record_date) VALUES
    (1, 1, 'Hypertension Stage 1', 'Lisinopril 10mg daily', '2024-03-20'),
    (2, 2, 'Childhood Asthma', 'Albuterol inhaler PRN', '2024-03-15')""",
    
    # Lab Results
    """INSERT INTO lab_results (patient_id, test_name, test_date, result_value, reference_range) VALUES
    (1, 'Cholesterol Level', '2024-03-20', 210.5, '<200 mg/dL'),
    (2, 'Peak Flow Rate', '2024-03-15', 350.0, '300-500 L/min')"""
    ]
    
    try:
        cursor = connection.cursor()
        for data in sample_data:
            cursor.execute(data)
        connection.commit()
        print("Sample data inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        exit(1)

if __name__ == "__main__":
    conn = create_database()
    create_tables(conn)
    insert_sample_data(conn)
    conn.close()