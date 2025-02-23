import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import subprocess
import wmi
from fpdf import FPDF
import platform
from tkinter import ttk  # To add checkbox functionality

class ForensicToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Forensic Tool")
        self.root.geometry("800x500")

        # Create a frame for the buttons on the left
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        # Title
        self.title_label = tk.Label(self.left_frame, text="Digital Forensic Tool", font=("Arial", 20))
        self.title_label.pack(pady=20)

        # Buttons for different features
        self.wifi_btn = tk.Button(self.left_frame, text="Analyze WiFi Credentials", command=self.wifi_credentials)
        self.wifi_btn.pack(pady=10)

        self.uninstall_btn = tk.Button(self.left_frame, text="List Uninstalled Software", command=self.uninstalled_software)
        self.uninstall_btn.pack(pady=10)

        self.usb_btn = tk.Button(self.left_frame, text="List USB Devices", command=self.list_usb_devices)
        self.usb_btn.pack(pady=10)

        self.download_btn = tk.Button(self.left_frame, text="Download Forensic Results", command=self.download_results)
        self.download_btn.pack(pady=20)

        # Create a frame for the preview screen on the right
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Preview output area
        self.output_preview = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, height=20, width=50)
        self.output_preview.pack(fill=tk.BOTH, expand=True)

        # Variables to hold results
        self.wifi_info = []
        self.uninstalled_software_info = []
        self.usb_devices_info = []

    # Display system information
    def system_info(self):
        system_data = platform.uname()
        return (f"System: {system_data.system}, Node Name: {system_data.node}, "
                f"Release: {system_data.release}, Version: {system_data.version}, "
                f"Machine: {system_data.machine}, Processor: {system_data.processor}\n"
                f"RAM: {self.get_system_ram()} GB, Disk: {self.get_disk_space()} GB Free")

    def get_system_ram(self):
        # Retrieve total RAM in GB
        c = wmi.WMI()
        for sys in c.Win32_ComputerSystem():
            ram = float(sys.TotalPhysicalMemory) / (1024**3)
            return round(ram, 2)

    def get_disk_space(self):
        # Retrieve free disk space
        c = wmi.WMI()
        for disk in c.Win32_LogicalDisk(DriveType=3):
            free_space = float(disk.FreeSpace) / (1024**3)
            return round(free_space, 2)

    # WiFi Credentials Analyzer
    def wifi_credentials(self):
        try:
            profiles_data = subprocess.check_output('netsh wlan show profiles', shell=True, encoding='unicode_escape')
            profiles = [line.split(":")[1].strip() for line in profiles_data.splitlines() if "All User Profile" in line]

            self.wifi_info = []
            for profile in profiles:
                try:
                    profile_info_cmd = f'netsh wlan show profile "{profile}" key=clear'
                    profile_info = subprocess.check_output(profile_info_cmd, shell=True, encoding='unicode_escape')
                    password_line = [line.split(":")[1].strip() for line in profile_info.splitlines() if "Key Content" in line]
                    password = password_line[0] if password_line else "No Password"
                    self.wifi_info.append(f"WiFi: {profile}, Password: {password}")
                except subprocess.CalledProcessError:
                    self.wifi_info.append(f"WiFi: {profile}, Password: [Could not retrieve]")

            self.update_output_preview("\n".join(self.wifi_info))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve WiFi credentials: {e}")

     # Uninstalled Software (from Event Logs)
    def uninstalled_software(self):
        try:
            # Using PowerShell to retrieve uninstallation logs from the Application event log
            uninstall_cmd = "Get-WinEvent -LogName Application | Where-Object { $_.Id -eq 11724 } | Format-Table TimeCreated, Message -AutoSize"
            uninstalled_data = subprocess.check_output(['powershell', '-Command', uninstall_cmd], shell=True, encoding='unicode_escape')

            self.uninstalled_software_info = uninstalled_data.splitlines()
            self.update_output_preview("\n".join(self.uninstalled_software_info))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve uninstalled software logs: {e}")

    # List USB Devices
    def list_usb_devices(self):
        try:
            self.usb_devices_info = []
            c = wmi.WMI()
            for usb in c.Win32_USBControllerDevice():
                self.usb_devices_info.append(f"Device: {usb.Dependent.Caption}, Serial: {usb.Dependent.PNPDeviceID}")

            self.update_output_preview("\n".join(self.usb_devices_info))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve USB devices: {e}")

    # Update the preview screen
    def update_output_preview(self, text):
        self.output_preview.delete(1.0, tk.END)
        self.output_preview.insert(tk.END, text)

    # Download forensic results as PDF
    def download_results(self):
        # Create a new window for checkbox selection
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Information to Download")
        selection_window.geometry("400x300")

        # Checkbox options for selecting results to include
        self.wifi_var = tk.BooleanVar()
        self.uninstalled_var = tk.BooleanVar()
        self.usb_var = tk.BooleanVar()
        self.all_var = tk.BooleanVar()

        tk.Checkbutton(selection_window, text="WiFi Credentials", variable=self.wifi_var).pack(anchor="w")
        tk.Checkbutton(selection_window, text="Uninstalled Software", variable=self.uninstalled_var).pack(anchor="w")
        tk.Checkbutton(selection_window, text="USB Devices", variable=self.usb_var).pack(anchor="w")
        tk.Checkbutton(selection_window, text="All Information", variable=self.all_var).pack(anchor="w")

        # Add button to confirm the selection
        tk.Button(selection_window, text="Download", command=self.generate_pdf).pack(pady=20)

    # Generate the PDF with more detailed and colorful output
    def generate_pdf(self):
        # Close the selection window
        if hasattr(self, 'selection_window'):
            self.selection_window.destroy()

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()

        # Add a title with color
        pdf.set_font("Arial", size=16, style='B')
        pdf.set_text_color(0, 0, 255)
        pdf.cell(200, 10, txt="Digital Forensic Report", ln=True, align="C")

        # Add system information
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(10)
        pdf.cell(200, 10, txt="System Information", ln=True, align="L")
        pdf.multi_cell(0, 10, self.system_info())

        # Add selected forensic results
        if self.wifi_var.get() or self.all_var.get():
            pdf.ln(10)
            pdf.set_font("Arial", size=14, style='B')
            pdf.set_text_color(0, 100, 0)
            pdf.cell(200, 10, txt="WiFi Credentials", ln=True, align="L")
            pdf.set_font("Arial", size=12)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 10, "\n".join(self.wifi_info) if self.wifi_info else "No WiFi credentials retrieved.")

        if self.uninstalled_var.get() or self.all_var.get():
            pdf.ln(10)
            pdf.set_font("Arial", size=14, style='B')
            pdf.set_text_color(0, 100, 0)
            pdf.cell(200, 10, txt="Uninstalled Software", ln=True, align="L")
            pdf.set_font("Arial", size=12)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 10, "\n".join(self.uninstalled_software_info) if self.uninstalled_software_info else "No uninstalled software data.")

        if self.usb_var.get() or self.all_var.get():
            pdf.ln(10)
            pdf.set_font("Arial", size=14, style='B')
            pdf.set_text_color(0, 100, 0)
            pdf.cell(200, 10, txt="USB Devices", ln=True, align="L")
            pdf.set_font("Arial", size=12)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 10, "\n".join(self.usb_devices_info) if self.usb_devices_info else "No USB device data.")

        # Save the PDF to a user-specified file
        pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if pdf_filename:
            pdf.output(pdf_filename)
            messagebox.showinfo("Success", f"Results saved to {pdf_filename}")

# Main application launch
if __name__ == "__main__":
    root = tk.Tk()
    app = ForensicToolGUI(root)
    root.mainloop()
