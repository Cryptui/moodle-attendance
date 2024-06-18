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

## 🔄 GitHub Actions Workflow <a name="github-actions-workflow"></a>

The `attendance_workflow.yml` file in the `.github/workflows` directory configures the GitHub Actions workflow for this project. It automates the attendance marking process by running the Selenium script on a schedule.

### Key Components of the Workflow:
- **Triggers**: The workflow is triggered on a schedule defined in cron syntax, allowing the script to run automatically at specified times.
- **Environment**: It runs on the latest Ubuntu virtual environment provided by GitHub Actions.
- **Steps**:
  1. **Checkout**: Clones the repository to the GitHub Actions runner.
  2. **Set Up Python**: Installs Python.
  3. **Setup Firefox**: Ensures Firefox is installed and configured.
  4. **Install geckodriver**: Downloads and sets up geckodriver needed for Selenium to interact with Firefox.
  5. **Install Dependencies**: Installs required Python libraries from `requirements.txt`.
  6. **Run Script**: Executes the `attendance.py` script.
  7. **Upload Logs**: If enabled, uploads logs from geckodriver for debugging.

### Editing the Workflow:
To adjust when the script runs or make changes to the workflow, edit the `.github/workflows/attendance_workflow.yml` file. You can modify the cron schedule or add additional steps to the workflow as needed.

For more details on configuring GitHub Actions, see the [GitHub Actions documentation](https://docs.github.com/en/actions).

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


