import pyodbc
import time
import concurrent.futures

# Connection details
import os 
from dotenv import load_dotenv
load_dotenv()
conn_str = os.getenv('DATABASE_URL')


def execute_stored_procedure():
    try:
        # Establish a connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Stored procedure name
        stored_procedure = "spTop10_DH1"

        # Measure the execution time
        start_time = time.time()
        cursor.execute(f"EXEC {stored_procedure}")
        cursor.fetchall()  # Fetch results if needed
        end_time = time.time()

        # Calculate the duration
        execution_time = end_time - start_time

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return execution_time, True  # True indicates success

    except Exception as e:
        return 0, False  # 0 execution time indicates failure

# Function to run stored procedures in parallel and gather results
def run_stored_procedures_parallel(n_times):
    execution_times = []
    failures = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(execute_stored_procedure) for _ in range(n_times)]
        for future in concurrent.futures.as_completed(futures):
            exec_time, success = future.result()
            if success:
                execution_times.append(exec_time)
            else:
                failures += 1

    return execution_times, failures

# Number of times to run the stored procedure
n_times = 100

# Run the stored procedures and gather results
execution_times, failures = run_stored_procedures_parallel(n_times)

# Calculate average response time
if execution_times:
    average_response_time = sum(execution_times) / len(execution_times)
else:
    average_response_time = float('inf')

# Print the results
print(f"Average Response Time: {average_response_time} seconds")
print(f"Failure Rate: {failures} out of {n_times} ({(failures / n_times) * 100}%)")
