
# Keylogger Detection in Windows Subsystems

This project provides Python scripts to detect potential keyloggers on Windows systems using system data analysis and Google Gemini AI models.

## Features
- **System Data Collection:** Gathers running processes, network connections, and startup items.
- **AI-Powered Analysis:** Uses Google Gemini (Gemini Pro or Gemini 2.5 Flash) to analyze system data for suspicious patterns.
- **JSON Output:** Returns a probability score, reasoning, and actionable security suggestions.

## Scripts Overview

### project_detection.py
- Collects system data (processes, network, startup items).
- Sends data to Gemini 2.5 Flash for analysis.
- Prints probability of keylogger presence, reasoning, and security suggestions.
- Handles API responses and errors robustly.
- also in GUI format first click on SCAN button and then see results

### `keylogger.py`
- Similar to project_detection.py, but uses Gemini Pro model.
- Gathers system data and sends to Gemini for analysis.
- Prints results in a user-friendly format.

## How to Run

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/OMCHOKSI108/Keylogger-detection-in-windows-subsystems.git
   cd Keylogger-detection-in-windows-subsystems
   ```

2. **Set up a Python virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set your Gemini API key:**
   - Create a .env file in the project root:
     ```
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     ```
   - Or set it in your shell before running:
     ```powershell
     $env:GEMINI_API_KEY="your_actual_gemini_api_key_here"
     ```

5. **Run the detection script:**
   ```powershell
   python project_detection.py 
   # or
   python keylogger.py
   ```

## Method Used
- **System Data Collection:** Uses `psutil` and PowerShell to gather process, network, and startup information.
- **AI Analysis:** Sends a structured prompt to Gemini via REST API, requesting JSON-formatted results.
- **Security:** API key is loaded from environment variable or `.env` file (never hardcoded).

## Security Note
- **Do NOT commit your API key to source control.**
- The `.gitignore` file is configured to exclude `.env` and other sensitive files.

## Requirements
- Python 3.8+
- Internet connection (for Gemini API)
- Google Gemini API key

## Example Output
```
Keylogger Detection Results:
Probability of Keylogger: 15%
Reasoning: No suspicious processes found, but one startup item is unsigned.
Suggestions:
1. Update antivirus definitions
2. Remove unknown startup items
3. Monitor network connections
```

## License
MIT

---
by Om Choksi
