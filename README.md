![wall1](https://github.com/user-attachments/assets/fc8678e0-55fe-4933-9c9d-92eb8351ff40)# Win_forensic-
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
![image](https://github.com/user-attachments/assets/8bb3fc35-0d75-46b8-990e-1cf9909535ea)



### **Step 2: Convert to EXE**  
Run the following command to create a standalone `.exe` file:  
```bash
pyinstaller --onefile --windowed win_analysis.py
```
- `--onefile`: Creates a single executable file.  
- `--windowed`: Hides the console window (important for GUI apps).  

### **Step 4: Locate and Run the EXE**  
- Once the process is completed, go to the **`dist`** folder inside your script's directory.  
- You’ll find `forensic_tool.exe` there.  
- Double-click it to run your forensic tool as a standalone application.  


