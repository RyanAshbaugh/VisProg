# Specify the installer and installation directory
$installer = "Miniconda3-latest-Windows-x86_64.exe"
$install_dir = "$HOME\Miniconda3"
$outfile_path = "$HOME\$installer"
$repo_dir = "$HOME\visprog"

# Download the Miniconda installer
Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/$installer -OutFile $outfile_path

# Install Miniconda
Start-Process $outfile_path -ArgumentList "/InstallationType=JustMe /AddToPath=0 /RegisterPython=0 /S /D=$install_dir" -Wait -NoNewWindow

# Remove the installer
Remove-Item -Path $outfile_path

# Add the conda command to the current user's PATH environment variable
$env:Path = "$env:Path;$install_dir;$install_dir\Scripts;$install_dir\Library\bin"

conda init powershell

conda env create -f environment.yaml

conda activate visprog

pip install python-magic-bin

Pause
