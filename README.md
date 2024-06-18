# 🎓 Moodle Attendance Automation

This project automates the process of checking attendance on the Moodle platform using Selenium WebDriver and GitHub Actions. It is designed to run on GitHub's virtual environments, specifically using Ubuntu latest versions.

## ✨ Features <a name="features"></a>
- Automated login and attendance marking on Moodle.
- Configurable for different Moodle instances.
- Runs headlessly on GitHub Actions.
- Scheduled runs using cron jobs in GitHub Actions.
- Error handling and logging to troubleshoot issues in automation.

## 📋 Requirements <a name="requirements"></a>
- GitHub Account
- Python 3.x+
- Selenium WebDriver

## ⚙️ Installation <a name="installation"></a>

1. Fork or clone the repository:
git clone https://github.com/yourgithubusername/moodle-attendance

2. Install required Python packages:
pip install -r requirements.txt


## 🚀 Usage <a name="usage"></a>

Configure the `secrets` in your GitHub repository settings for `MOODLE_USERNAME` and `MOODLE_PASSWORD` to store your credentials securely.

## 📁 Directory Structure <a name="directory-structure"></a>

- `attendance.py`: Python script that performs the automated login and attendance check.
- `.github/workflows/attendance-check.yml`: GitHub Actions workflow that schedules and runs the automation script.

## 🛠️ Configuration <a name="configuration"></a>

Edit the `.github/workflows/attendance-check.yml` file to set the schedule or adjust other GitHub Actions settings according to your requirements.

## 🖥️ Local Testing <a name="local-testing"></a>

To test the script locally:
python attendance.py
Ensure that your local machine has all the necessary browser drivers installed and that the script is configured to run in a non-headless mode if needed.

## 🤝 Contributing <a name="contributing"></a>

Contributions are welcome! Feel free to fork the project and submit pull requests. You can also open issues if you find bugs or have feature suggestions.

## 📝 License <a name="license"></a>

This project is released under the MIT License. See the `LICENSE` file for more details.

## Maintainers 👷 <a name="maintainers"></a>

For questions or support, please contact [your GitHub](https://github.com/yourgithubusername).


