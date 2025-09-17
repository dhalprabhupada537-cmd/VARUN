import subprocess
import sys

def update_requirements():
    """Update requirements.txt with currently installed packages"""
    with open('requirements.txt', 'w') as f:
        # Get list of installed packages
        result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], 
                              capture_output=True, text=True)
        f.write(result.stdout)
    print("Requirements updated successfully!")

if __name__ == "__main__":
    update_requirements()