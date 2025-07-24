import psutil
import subprocess
import platform
import os
import requests
import json
from datetime import datetime

# !! IMPORTANT: Replace with your actual Gemini API Key !!
# It's better to load this from an environment variable or a secure config.
# For demonstration, I'm setting it directly asYOUR_GEMINI_API_KEY_HERE you did, but be mindful in production.
os.environ["GEMINI_API_KEY"] = "AIzaSyC2S2IYETRRJRdrWu-lL8s4M0fuU1yuujA"

# Function to gather system data (from your original script, unchanged)
def gather_system_data():
    system_data = {"processes": [], "network": [], "startup_items": []}
    
    # Collect running processes
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            proc_info = {
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "exe": proc.info['exe'] or "N/A",
                "cmdline": " ".join(proc.info['cmdline']) if proc.info['cmdline'] else "N/A"
            }
            system_data["processes"].append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Collect network connections
    for conn in psutil.net_connections(kind='inet'):
        try:
            conn_info = {
                "laddr": f"{conn.laddr.ip}:{conn.laddr.port}",
                "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                "status": conn.status,
                "pid": conn.pid
            }
            system_data["network"].append(conn_info)
        except:
            continue
    
    # Collect startup items (Windows-specific)
    if platform.system() == "Windows":
        try:
            # Use PowerShell to get startup items
            powershell_cmd = 'powershell "Get-CimInstance -ClassName Win32_StartupCommand | Select-Object Name, Command | ConvertTo-Json"'
            output = subprocess.check_output(powershell_cmd, shell=True, text=True)
            startup_items = json.loads(output)
            if isinstance(startup_items, list):
                for item in startup_items:
                    system_data["startup_items"].append(f"{item.get('Name', 'N/A')}: {item.get('Command', 'N/A')}")
            elif isinstance(startup_items, dict): # Handle single item case
                system_data["startup_items"].append(f"{startup_items.get('Name', 'N/A')}: {startup_items.get('Command', 'N/A')}")
        except Exception as e:
            system_data["startup_items"].append(f"Unable to retrieve startup items: {str(e)}")
    
    return system_data

# Function to call Gemini API (Modified for Gemini 2.5 Flash)
def analyze_with_gemini(data):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        return {"error": "Gemini API key not found or not replaced in environment variables"}
    
    # Use the correct model name and endpoint for Gemini 2.5 Flash
    model_name = "gemini-2.5-flash" 
    api_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    prompt = f"""
    You are a cybersecurity expert. Analyze the following system data for signs of a potential keylogger:
    - Processes: {json.dumps(data['processes'], indent=2)}
    - Network Connections: {json.dumps(data['network'], indent=2)}
    - Startup Items: {json.dumps(data['startup_items'], indent=2)}
    
    Look for suspicious patterns such as:
    - Unknown or unsigned processes with vague names.
    - Processes with unusual command lines or executable paths.
    - Network connections to unknown or suspicious IP addresses or ports.
    - Unfamiliar startup items that could indicate persistence.
    - Processes attempting to inject into other processes or hook keyboard/mouse events.
    
    Provide:
    1. A percentage chance (0-100%) that a keylogger is present, based on your analysis.
    2. A brief, concise explanation of your reasoning, highlighting any specific suspicious findings.
    3. Three actionable suggestions to secure the system.
    
    Respond in JSON format:
    ```json
    {{
        "probability": <percentage>,
        "reasoning": "<explanation>",
        "suggestions": ["<suggestion1>", "<suggestion2>", "<suggestion3>"]
    }}
    ```
    """
    
    try:
        headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            # Add generation_config to ensure JSON output if possible
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }
        response = requests.post(
            api_endpoint,
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        result = response.json()
        
        if "candidates" in result and result["candidates"]:
            text_part = result["candidates"][0]["content"]["parts"][0]["text"]
            try:
                # The response_mime_type should help, but sometimes models still wrap it.
                # Attempt to parse directly, or extract if wrapped in markdown code block.
                if text_part.strip().startswith("```json") and text_part.strip().endswith("```"):
                    json_string = text_part.strip()[len("```json"):-len("```")].strip()
                else:
                    json_string = text_part.strip()
                return json.loads(json_string)
            except json.JSONDecodeError as e:
                return {"error": f"Gemini response could not be parsed as JSON. Error: {e}", "raw": text_part}
            except Exception as e:
                return {"error": f"An unexpected error occurred parsing Gemini response: {e}", "raw": text_part}
        else:
            return {"error": "No candidates returned from Gemini API.", "raw": result}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error calling Gemini API: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": f"Failed to call Gemini API: {str(e)}"}

# Main function (unchanged)
def main():
    print(f"[{datetime.now()}] Starting keylogger detection...")
    
    # Gather system data
    system_data = gather_system_data()
    print(f"[{datetime.now()}] System data collected. Processes: {len(system_data['processes'])}, "
          f"Network connections: {len(system_data['network'])}, Startup items: {len(system_data['startup_items'])}")
    
    # Analyze with Gemini API
    result = analyze_with_gemini(system_data)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        if "raw" in result:
            print("Raw API response (for debugging):")
            print(result["raw"])
        return
    
    # Print results
    print("\nKeylogger Detection Results:")
    print(f"Probability of Keylogger: {result.get('probability', 'N/A')}%")
    print(f"Reasoning: {result.get('reasoning', 'N/A')}")
    print("\nSuggestions:")
    for i, suggestion in enumerate(result.get('suggestions', []), 1):
        print(f"{i}. {suggestion}")

if __name__ == "__main__":
    main()