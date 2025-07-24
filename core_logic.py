import os
import psutil
import google.generativeai as genai
from datetime import datetime

def gather_and_save_system_data():
    """Gathers system data and saves it to a timestamped log file in the /logs folder."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(log_dir, f"system_snapshot_{timestamp}.log")

    process_data = "--- RUNNING PROCESSES ---\nPID\tName\t\tUsername\n"
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            process_data += f"{proc.info['pid']}\t{proc.info['name']}\t{proc.info['username']}\n"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    net_data = "\n--- ACTIVE NETWORK CONNECTIONS ---\n"
    for conn in psutil.net_connections(kind='inet'):
        try:
            net_data += f"PID: {conn.pid or 'N/A'}\tStatus: {conn.status}\tLocal: {conn.laddr}\tRemote: {conn.raddr or 'N/A'}\n"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    full_system_data = process_data + net_data
    with open(log_filename, 'w', encoding='utf-8') as f:
        f.write(full_system_data)
        
    return full_system_data

def analyze_with_llm(system_data):
    """Sends system data to the LLM for a more detailed and conclusive analysis."""
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("API key not found.")
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # --- NEW, ENHANCED PROMPT ---
        prompt = f"""
        You are a world-class cybersecurity analyst and malware reverse engineer. Your task is to perform a deep analysis of the provided system data to detect keyloggers or other malware. Your conclusion must be as definitive as possible.

        Analyze the data against these keylogger heuristics:
        1.  **Suspicious Process Names:** Look for names that are misspelled versions of system processes (e.g., 'svch0st.exe'), contain random characters, or are overly generic (e.g., 'service.exe', 'update.exe').
        2.  **Processes Without Owners:** Processes with 'None' or an unusual username are highly suspicious.
        3.  **Suspicious Network Activity:** Look for processes making many connections to various IPs, especially on non-standard ports. A legitimate browser will have many connections, but a less common application doing so is a major red flag.
        4.  **Uncommon Processes:** Note any process name that is not a well-known part of a standard operating system or common application.

        Provide your report in the following strict format:

        **1. SUSPICIOUS FINDINGS:**
        A numbered list of every suspicious item. If none, state "No suspicious items were found." For each item, provide:
        - Process Name/Connection:
        - PID:
        - Reason for Suspicion: [Explain exactly why it matches the heuristics]
        - Threat Score: [A score from 1 to 10, where 100 is highest]

        **2. OVERALL ASSESSMENT:**
        A summary paragraph explaining how the findings correlate. For example, do suspicious processes also have suspicious network connections?

        **3. FINAL VERDICT:**
        A single, conclusive rating. Must be one of these three:
        - [NO MALICIOUS ACTIVITY DETECTED]
        - [SUSPICIOUS ACTIVITY DETECTED]
        - [HIGHLY LIKELY MALICIOUS ACTIVITY DETECTED]

        **4. RECOMMENDED ACTIONS:**
        A numbered list of concrete steps the user should take right now.

        Final ratings chances of Keylogger installed on system out of 100 with safety score 

        --- SYSTEM DATA ---
        {system_data}
        --- END OF DATA ---
        """
        
        response = model.generate_content(prompt)
        report_text = response.text

        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_filename = os.path.join(results_dir, f"{timestamp}.txt")

        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        return report_text
    except Exception as e:
        return f"An error occurred during AI analysis: {e}"