# Python-Nmap and GPT Vulnerability Scanner

This project is a Python script that integrates the Nmap scanning tool with the GPT-3 language model by OpenAI to perform vulnerability
scanning and generate reports. It allows you to scan a target IP address or hostname for open ports and services, 
and then use GPT-3 to analyze the scan results and identify potential vulnerabilities.

## Features

- **Nmap Integration**: The script uses the `nmap` library to perform network scans on the specified target.

- **GPT-3 Integration**: It utilizes OpenAI's GPT-3 model to generate vulnerability analysis reports based on the scan results.

- **Scan Profiles**: The script offers predefined scan profiles with different scanning options. Users can select a scan profile to customize the scan.

- **SQLite Database**: Scan results are stored in an SQLite database for future reference.

- **Graphical User Interface (GUI)**: The script provides a simple GUI for user interaction.

## Getting Started

To use this Python-Nmap and GPT Vulnerability Scanner, follow these steps:

### Prerequisites

1. You need to have Python installed on your system. If not, download and install it from the official [Python website](https://www.python.org/downloads/).
2.  you will need to install the official nmap scanner from the site enable it and add the root to the systme enviroment varibels 
3. Install the required Python libraries using the following command :
go to the terminal python terminal and type 
   ```bash
   pip install nmap openai tkinter
   ```

4. You will also need an OpenAI API key. Sign up for an API key on the [OpenAI website](https://beta.openai.com/signup/) and replace `YOUR_API_KEY` with your actual API key in the script.

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your_username/your_project.git
   ```

2. Change the directory to the project folder:

   ```bash
   cd your_project
   ```

3. Run the script:

   ```bash
   python your_script.py target_ip_or_hostname
   ```

## Usage

1. Launch the script by running `python your_script.py target_ip_or_hostname`.

2. In the GUI, you'll see a welcome message indicating the target IP or hostname you entered.

3. Select a scan profile from the dropdown list. Each profile corresponds to different Nmap scanning options.

4. Optionally, you can enter custom Nmap scan options in the text entry field.

5. Click the "Scan" button to initiate the scan.

6. The GPT-3 model will generate a vulnerability analysis report based on the scan results.

7. The report will be displayed in the GUI, providing information about detected vulnerabilities and potential issues.

## Configuration

- You can modify the predefined scan profiles and their corresponding Nmap options in the `Scanner` class constructor.

- If you want to customize GPT-3 interactions further, you can adjust the prompts and responses in the `Scanner` class.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit pull requests. Contributions are welcome in the form of bug fixes, new features, or improvements to the code or documentation.

## License

This project is licensed under the [MIT License](LICENSE), which means you are free to use, modify, and distribute the code as long as you retain the license text.

## Acknowledgments

- This project makes use of the [Nmap](https://nmap.org/) network scanning tool.

- It also integrates the [OpenAI GPT-3](https://beta.openai.com/signup/) language model for text generation.

---

This README provides a comprehensive guide on how to use and contribute to your Python-Nmap and GPT Vulnerability Scanner project. Make sure to update it with any changes or additional information as needed.
