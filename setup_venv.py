import os
import subprocess
import sys

def setup_venv():
    """Set up virtual environment and install dependencies"""
    # Create virtual environment if it doesn't exist
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
    
    # Determine the pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = os.path.join('venv', 'Scripts', 'pip.exe')
        activate_cmd = 'venv\\Scripts\\activate'
    else:  # macOS/Linux
        pip_path = os.path.join('venv', 'bin', 'pip')
        activate_cmd = 'source venv/bin/activate'
    
    print("Installing dependencies...")
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'])
    
    print("\nVirtual environment setup complete!")
    print(f"To activate the virtual environment, run: {activate_cmd}")
    print("Then run: streamlit run app.py")

if __name__ == "__main__":
    setup_venv()