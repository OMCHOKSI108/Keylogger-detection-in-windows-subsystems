
# 🔍 Keylogger Detection System

A sophisticated Python-based system that leverages AI to detect potential keyloggers in Windows environments. This tool analyzes system processes, network connections, and startup items to identify suspicious patterns that might indicate the presence of keylogging malware.

##  Features

-  **Real-time System Analysis**
  - Monitors running processes
  - Tracks network connections
  - Analyzes startup items
  
-  **AI-Powered Detection**
  - Utilizes Google's Gemini AI
  - Provides probability scores
  - Offers detailed reasoning
  
-  **Security Recommendations**
  - Actionable security suggestions
  - Risk mitigation strategies
  - System hardening tips

##  Requirements

- Python 3.8+
- Windows OS
- Internet connection
- Google Gemini API key
- Required Python packages (see `requirements.txt`)

##  Quick Start

1. **Clone & Setup:**
   ```bash
   git clone https://github.com/OMCHOKSI108/Keylogger-detection-in-windows-subsystems.git
   cd Keylogger-detection-in-windows-subsystems
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure API Key:**
   - Create `.env` file:
     ```env
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Or set environment variable:
     ```powershell
     $env:GEMINI_API_KEY="your_gemini_api_key_here"
     ```

3. **Run Detection:**
   ```bash
   python project_detection.py
   ```

##  Scripts

### `project_detection.py`
- Main detection script using Gemini 2.5 Flash
- Comprehensive system analysis
- Enhanced error handling
- Detailed JSON output

### `keylogger.py`
- Alternative detection using Gemini Pro
- Simplified analysis approach
- Basic reporting format

## Sample Output

```json
{
    "probability": 15,
    "reasoning": "System analysis shows no immediate threats, but potential vulnerabilities detected in startup items",
    "suggestions": [
        "Review and clean startup programs",
        "Update security software",
        "Monitor unusual network activity"
    ]
}
```

##  Security Notes

- Never commit API keys
- Keep dependencies updated
- Regular system scans recommended
- Follow security best practices

##  Method

1. **Data Collection**
   - Process enumeration via `psutil`
   - Network connection monitoring
   - Startup item analysis

2. **AI Analysis**
   - Pattern recognition
   - Threat probability calculation
   - Security recommendation generation

3. **Reporting**
   - JSON-formatted results
   - Human-readable output
   - Actionable insights

##  Documentation

For detailed information about:
- System requirements
- API documentation
- Security guidelines

Visit our [Wiki](https://github.com/OMCHOKSI108/Keylogger-detection-in-windows-subsystems/)

##  Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

##  License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
