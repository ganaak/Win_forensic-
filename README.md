# Win_forensic-
windows log analysis tool

## Overview  
The **Digital Forensic Tool** is a Windows-based forensic analysis application built using Python and `tkinter`. It allows users to gather and analyze system forensic data, such as WiFi credentials, uninstalled software logs, and connected USB devices. The tool also provides an option to export the results as a **PDF report** for further investigation.  

## Features  
✔ **WiFi Credentials Analyzer** – Retrieves saved WiFi profiles and their passwords (if available).  
✔ **Uninstalled Software Logs** – Extracts software uninstallation logs from Windows Event Viewer.  
✔ **USB Device List** – Displays connected USB devices along with their details.  
✔ **System Information** – Gathers system details like RAM, disk space, and processor information.  
✔ **Download Report** – Saves forensic results in a structured and formatted **PDF report**.  
✔ **User-Friendly GUI** – Provides an easy-to-use interface with real-time output previews.  


You can convert your Python script into an executable (`.exe`) file using **PyInstaller** and then run it like any Windows application. Follow these steps:

### **Step 1: Install PyInstaller**  
Open Command Prompt and install PyInstaller if you haven't already:  
```bash
pip install pyinstaller
```


### **Step 2: Convert to EXE**  
Run the following command to create a standalone `.exe` file:  
```bash
pyinstaller --onefile --windowed forensic_tool.py
```
- `--onefile`: Creates a single executable file.  
- `--windowed`: Hides the console window (important for GUI apps).  

### **Step 4: Locate and Run the EXE**  
- Once the process is completed, go to the **`dist`** folder inside your script's directory.  
- You’ll find `forensic_tool.exe` there.  
- Double-click it to run your forensic tool as a standalone application.  


