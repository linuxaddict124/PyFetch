#!/bin/bash

echo "Preparing to install PyFetch..."

# Detecting distros to give warnings or to fail installation for unsupported distros
if grep -qi nixos /etc/os-release; then
    echo "NixOS is not supported by PyFetch."
    exit 1
elif grep -qi void /etc/os-release; then
    echo "WARNING: Some dependencies for PyFetch will be outdated on Void Linux. Continuing..."
elif grep -qi gentoo /etc/os-release; then
    echo "WARNING: PyFetch has never been tested on Gentoo Linux."
elif grep -qi vanilla /etc/os-release; then
    echo "Vanilla OS is a atomic immutable Linux distribution, which are not supported."
    exit 1
elif grep -qi android /etc/os-release; then
    echo "Did you know that ANDROID CAN'T EVEN RUN PYFETCH?? This is a CLI command, not a GUI Android app."
    exit 1
fi
sleep 1
# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "python3 is not installed. Please install it now. (If your on Linux, HOW DO YOU NOT HAVE PYTHON??)"
    exit 1
fi

# Check if Python Pip is installed
if grep -qi arch /etc/os-release; then
    echo "Arch detected, skipping pip check."
elif grep -qi void /etc/os-release; then
    echo "Void Linux detected, skipping pip check."
elif grep -qi fedora /etc/os-release; then
    echo "Fedora detected, skipping pip check."
elif grep -qi ubuntu /etc/os-release; then
    echo "Ubuntu detected, skipping pip check."
elif grep -qi zorin /etc/os-release; then
    echo "Zorin OS detected, skipping pip check."
elif grep -qi debian /etc/os-release; then
    echo "Saving Python Pip check for later."
elif grep -qi cachyos /etc/os-release; then
    echo "CachyOS detected, skipping pip check."
else
    if ! command -v pip &> /dev/null; then
      echo "Python Pip is not installed. Please install it now."
      exit 1
    fi
fi

# Check if running as root
if [ "$EUID" -eq 0 ]; then
  echo "Please do not run install.sh as root. This is unsafe!"
  exit 1
fi

# Start installation process
read -p "Do you want to install PyFetch? (y/n): " choice

case "$choice" in
  y|Y )
    echo "Installing dependencies..."
    if grep -qi arch /etc/os-release; then
      sudo pacman -S --noconfirm python-pyfiglet python-packaging python-psutil python-requests
    elif grep -qi void /etc/os-release; then
      sudo xbps-install -Sy python3-setuptools python3-pyfiglet python3-packaging python3-psutil python3-requests
    elif grep -qi fedora /etc/os-release; then
      sudo dnf install -y python3-setuptools python3-pyfiglet python3-packaging python3-psutil python3-requests
    elif grep -qi ubuntu /etc/os-release; then
      sudo apt-get install -y python3-setuptools python3-pyfiglet python3-packaging python3-psutil python3-requests
    elif grep -qi zorin /etc/os-release; then
      sudo apt-get install -y python3-setuptools python3-pyfiglet python3-packaging python3-psutil python3-requests
    elif grep -qi debian /etc/os-release; then
      sudo apt-get install -y python3-setuptools python3-pyfiglet python3-psutil python3-requests
      echo "WARNING: Debian does not have the package python3-packaging in it's official repo. Checking for python pip..."
      sleep 1
      if ! command -v pip &> /dev/null; then
        echo "Python Pip is not installed. Good luck on getting python3-packaging!"
      else
        echo "Python Pip detected, installing packaging..."
        pip install packaging
      fi
    elif grep -qi cachyos /etc/os-release; then
      sudo pacman -S --noconfirm python-pyfiglet python-packaging python-psutil python-requests
    else
      pip install pyfiglet
      pip install packaging
      pip install psutil
      pip install requests
    fi
    sleep 1
    echo "Installing Pyfetch..."
    if [ -f /usr/bin/pyfetch ]; then
      echo "pyfetch detected, reinstalling..."
      sudo rm /usr/bin/pyfetch
      rm -rf ~/.config/pyfetch
      sudo cp ./.files/pyfetch /usr/bin/pyfetch
      cp -r ./.files/config/ ~/.config/pyfetch/
      sudo chmod +x /usr/bin/pyfetch
    else
      if [ -f ~/.config/pyfetch ]; then
        rm -rf ~/.config/pyfetch
        cp -r ./.files/config/ ~/.config/pyfetch/
      else
        cp -r ./.files/config/ ~/.config/pyfetch/
      fi
      sudo cp ./.files/pyfetch /usr/bin/pyfetch
      sudo chmod +x /usr/bin/pyfetch
    fi
    if [ -f /usr/bin/pyfetch-beta ]; then
        echo "pyfetch-beta detected, deleting file..."
        sudo rm /usr/bin/pyfetch-beta
    fi

    echo "PyFetch is now installed."

    # Optional Files
    read -p "Do you want to download optional documents? (y/n): " optionalchoice

    case "$optionalchoice" in
      y|Y )
        mkdir ~/Documents/pyfetch
        cp ./.files/optional/LICENSE ~/Documents/pyfetch/LICENSE
        cp ./.files/optional/README.md ~/Documents/pyfetch/README.md
        echo "Completed. Go to ~/Documents/pyfetch to read them."
        exit 0
      ;;
      n|N )
        echo "Exiting..."
        exit 0
      ;;
      * )
        echo "Wrong input. Please type in y/n."
        exit 1
      ;;
    esac
    ;;
  n|N )
    echo "Installation aborted."
    exit 0
    ;;
  * )
    echo "Wrong input. Please type in y/n."
    exit 1
    ;;
esac
