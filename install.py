import os
import sys
import win32com.client
import subprocess

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)

def get_current_conda_env():
    try:
        # Get the current Conda environment name
        result = subprocess.run(
            ['conda', 'env', 'list'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output = result.stdout

        # Parse the active environment
        for line in output.splitlines():
            if "*" in line:
                # The current environment is marked with '*'
                env_name = line.split()[0]
                return env_name
    except Exception as e:
        print(f"Error fetching Conda environment: {e}")
        return None

try:
    conda_base_path = subprocess.Popen(['conda', 'info', '--base'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()[0].decode('utf-8').strip()
    
    # Construct the path to activate.bat
    activate_bat_path = os.path.join(conda_base_path, 'Scripts', 'activate.bat')



    # Check if the activate.bat file exists
    if os.path.exists(activate_bat_path):
        print(f"Found activate.bat at: {activate_bat_path}")
    #     # Define the shortcut target
        app_name = "process_app.py"
        conda_script_path = r"C:/ProgramData/anaconda3/Scripts/activate.bat"  # Adjust to your path
        conda_env = get_current_conda_env()
        print(f"Found activate.bat at: {conda_env}")  # Name of the Conda environment
        python_script = os.path.join(script_directory, app_name)  # Path to your Python script

    #     # Create the full command that the shortcut will run
        command = f'"{activate_bat_path}" && conda activate {conda_env} && python "{python_script}"'

    #     # Define the shortcut's location and name
        shortcut_path = os.path.join(os.environ["USERPROFILE"], "Desktop", "APS_VBO_APP.lnk")

    #     # Create the shell object to create the shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)

    #     # Set the shortcut properties
        shortcut.TargetPath = "cmd.exe"
        shortcut.Arguments = f'/C "{command}"'  # /C runs the command and then closes the window
        shortcut.WorkingDirectory = os.environ["USERPROFILE"]  # Set the working directory
        # shortcut.Ic2onLocation = "C:\\path\\to\\icon.ico"  # Optional: Set an icon for the shortcut

    #     # Save the shortcut
        shortcut.save()
    
except subprocess.CalledProcessError:
    print("Conda is not installed or not found in PATH.")



print(f"Shortcut created at {shortcut_path}")
