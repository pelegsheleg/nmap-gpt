import nmap
import openai
import argparse
import tkinter as tk
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('scan_results.db')  # Creates a connection to the SQLite database
cursor = conn.cursor()  # Creates a cursor object

# Creates a table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS scan_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target TEXT,
    profile TEXT,
    result TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()  # Commits the changes

openai.api_key = "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"
model_engine = "text-davinci-003"
nm = nmap.PortScanner()

parser = argparse.ArgumentParser(description='Python-Nmap and chatGPT integrated Vulnerability scanner')
parser.add_argument('target', metavar='target', type=str, help='Target IP or hostname')
args = parser.parse_args()

target = args.target


class Scanner:
    def __init__(self):
        self.scan_profiles = {
            'p1': '-Pn -sV -T4 -O -F',
            'p2': '-Pn -T4 -A -v',
            'p3': '-Pn -sS -sU -T4 -A -v',
            'p4': '-Pn -p- -T4 -A -v',
            'p5': ' - Pn - sS - sU - T4 - A - PE - PP - PS80, 443 - PA3389 - PU40125 - PY - g 53 - -script = vuln',
            'p6': '-Pn --script http-apache-negotiation,c,http-default-accounts,http-methods,http-method-tamper,http-passwd,http-php-version,http-robots.txt,http-shellshock,http-sitemap-generator,http-svn-enum,http-trace,http-userdir-enum,http-vuln-cve2015-1635,http-vuln-cve2017-5638,http-vuln-cve2017-8917,http-vuln-cve201',
            'p7': '-Pn -sU -T4  -p 53,69,111,123,137,138,161,162,445,500,514,520,623,626,1900,4500 --script broadcast-dhcp-discover,broadcast-dhcp6-discover,dns-service-discovery,snmp-info,snmp-sysdescr -vvv',
            'p8': '-Pn  --script banner -p 21,22,23,25,53,80,110,111,135,139,143,389,443,445,465,514,587,636,993,995,1025,1433,1521,2049,3306,3389,5900,5985,6000,6667,8000,8080,8443,8888,9100,9200,10000,49152,49153,49154,49155,49156,49157 -vvv',
            'p9': '-Pn -O -sS -sV -Pn -T4 --max-os-tries 2 --max-retries 1 --min-rtt-timeout 100ms --initial-rtt-timeout 500ms --max-rtt-timeout 3s --open -p 1-65535 -vvv',
            'p10': '-Pn --script=vuln,-Pn -O -sS -sV -Pn -T4 --max-os-tries 2 --max-retries 1 --min-rtt-timeout 100ms --initial-rtt-timeout 500ms --max-rtt-timeout 3s --open -p 1-65535 -vvv',
            'p11': '--script=http-vuln-cve2017-1000353.nse',
            'p12': '--script=http-wordpress-brute.nse ',
            'p13': '--script=http-wordpress-brute.nse ',
            'p14': '--script=http-sql-injection.nse '

        }

    def scan(self, target, profile, custom_options=""):
        if profile not in self.scan_profiles:
            return 'Invalid profile selected'

        # Append the custom options to the Nmap arguments
        nm.scan(target, arguments=self.scan_profiles[profile] + " " + custom_options)

        json_data = nm.analyse_nmap_xml_scan()
        analyze = json_data["scan"]

        # Prompt about what the query is all about
        prompt = f"Do a vulnerability analysis of {analyze} and return a list of detected vulnerabilities. ..."
        # A structure for the request
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
        )

        response = completion.choices[0].text
        conn = sqlite3.connect('scan_results.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scan_results (target, profile, result) VALUES (?, ?, ?)",
                       (target, profile, response))
        conn.commit()
        return response

        # ... existing scan code ...



class Gui:
    def __init__(self, master):
        self.master = master
        self.master.title("Python-Nmap and GPT Vulnerability Scanner")

        # Create frames
        self.frame1 = tk.Frame(self.master)
        self.frame1.pack()
        self.frame2 = tk.Frame(self.master)
        self.frame2.pack()
        self.frame3 = tk.Frame(self.master)
        self.frame3.pack()

        # Create widgets for frame 1
        self.label1 = tk.Label(self.frame1, text=f"Welcome! to the nmap gpt analyzer the ip you entered is {target}:")
        self.label1.pack(side="left")
        self.button1 = tk.Button(self.frame1, text="Scan", command=self.scan)
        self.button1.pack(side="left")

        # Create widgets for frame 2
        self.label2 = tk.Label(self.frame2, text="Select a scan profile:")
        self.label2.pack(side="left")
        self.combobox1 = ttk.Combobox(self.frame2, values=list(Scanner().scan_profiles.keys()))
        self.combobox1.current(0)
        self.combobox1.pack(side="left", padx=10)

        # Create label for scan profile explanation
        self.label3 = tk.Label(self.frame2, text="")
        self.label3.pack(side="left")

        # Create widgets for frame 3
        self.label4 = tk.Label(self.frame3, text="GPT Response:")
        self.label4.pack()
        self.textbox1 = tk.Text(self.frame3, height=70, width=100)
        self.textbox1.pack()

        # Bind combobox selection to update label3
        self.combobox1.bind("<<ComboboxSelected>>", self.update_label3)
        # In the Gui.__init__ function:
        self.entry1 = tk.Entry(self.frame2)
        self.entry1.pack(side="left", padx=10)

        # In the Gui.scan function:
        profile = self.combobox1.get()
        custom_options = self.entry1.get()
        scanner = Scanner()
        result = scanner.scan(target, profile, custom_options)

    def update_label3(self, event):
        selected_profile = self.combobox1.get()
        profile_explanation = self.get_profile_explanation(selected_profile)
        self.label3.configure(text=profile_explanation)

    def get_profile_explanation(self, profile):
        explanations = {
            'p1': "Nmap command that scans for open ports and service versions on the target host. It uses aggressive timing and operating system detection.",
            'p2': " Nmap command performs a basic scan with service detection enabled. It uses aggressive timing and verbose output to provide more information about the target",
            'p3': "more aggressive Nmap command that scans for open ports, operating system information, and service information. It also performs stealthy scans to avoid detection and uses verbose output.",
            'p4': "Nmap command is similar to 'p2', but it scans for all ports instead of just the common ones. This increases the scan time but can provide a more complete view of the target's network services",
            'p5': "This is a very aggressive Nmap command that scans for open ports and services using both TCP and UDP. It also uses various techniques to bypass firewalls and evade detection, and includes a script that looks for vulnerabilities in the target's web server.",
            'p6': "specifically targets web servers by scanning for vulnerabilities related to Apache, HTTP authentication, HTTP methods, HTTP password files, PHP version, robots.txt files, shellshock, sitemap generators, Subversion repositories, HTTP trace methods, user directories, and several other web-related issues",
            'p7': "This Nmap command performs a UDP scan of several common ports and includes scripts that search for DHCP and DNS information as well as SNMP data. This can help identify devices on the network and gather information about them",
            'p8': "Nmap command performs a detailed scan of several common TCP ports and includes a banner-grabbing script to gather information about the target's services. It uses verbose output to provide more information about the scan results",
            'p9': "This Nmap command is a comprehensive scan that includes operating system detection, service detection, and port scanning. It uses several aggressive techniques to speed up the scan and avoid detection",
            'p10': "This Nmap command is similar to 'p9', but it also includes a script that looks for vulnerabilities in the target's network services",
            'p11': "Checks for the Drupalgeddon vulnerability in web applications.",
            'p12': "Checks for the GitLab vulnerability in web applications.",
            'p13': "Performs brute-force attacks against WordPress sites.",
            'p14': "Attempts SQL injection attacks against web applications.."

        }
        if profile not in explanations:
            return "Invalid profile selected"
        return explanations[profile]

    def scan(self):
        profile = self.combobox1.get()
        custom_options = self.entry1.get()
        scanner = Scanner()
        result = scanner.scan(target, profile, custom_options)
        self.textbox1.delete("1.0", tk.END)
        self.textbox1.insert(tk.END, result)



def main():
    root = tk.Tk()
    gui = Gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
