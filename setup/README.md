# Setting Up Your Python Environment in VS Code

This guide will walk you through the full setup process step-by-step.

## Step 1: Create or Open Your Workspace Folder
Open Visual Studio Code and make sure you have a dedicated top-level folder for your project.  
If you don't have one yet, create a new folder and open it in VS Code.

## Step 2: Set Up a Python Virtual Environment
1. Press **Ctrl+Shift+P** (or Cmd+Shift+P on Mac) to open the Command Palette.  
2. Search for **Python: Create Environment**.  
3. Select **Virtual Environment** (do NOT choose Conda).  
4. When the setup completes, you should see a `.venv` folder in your workspace.  
5. Open your `.gitignore` file and add the following line:  
```
.venv
.env
```
This prevents your local virtual environment and credentials from being uploaded to GitHub.
### To verify that your local virtual environment is set up correctly:
- Open a **new terminal** by clicking the Terminal menu on the top bar.
- Check the terminal prompt. If your environment is activated, you should see **(.venv) PS C:\Users\xxx** at the beginning of the prompt.

## Step 3: Download and Copy the Setup Folder
1. Go to the GitHub link provided by your team.  
2. Download the repository as a **ZIP file**.  
3. Unzip it on your computer.  
4. Inside the unzipped project, locate the folder named **setup**.  
5. Copy **everything inside the setup folder** into your workspace folder in VS Code.

## Step 4: Obtain the Common Folder and `.env` File
Your team lead will share:
- The **common** folder  
- The **.env** file (contains API keys and credentials)

⚠️ You **must** sign the consent form before receiving the `.env` file.  
This ensures that all credentials are used responsibly and stored securely.

Place the `.env` file inside your workspace folder.

## Step 5: Install Required Python Libraries
1. Open **Terminal** → **New Terminal** in VS Code.  
2. Ensure that the terminal shows your virtual environment as activated (you will see `(venv)` or similar).  
3. Run the following command:

```
pip install -r requirements.txt
```

This installs all dependencies required for the shared components and for your project to run correctly.

---

You are now fully set up and ready to run Python scripts in VS Code using the shared components!


