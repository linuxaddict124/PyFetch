#!/usr/bin/env python3

PYFETCH_VERSION = "1.2.0"

import os

# Load ~/.config/pyfetch/pyfetch.conf
def load_conf(path):
    config = {}
    if not os.path.exists(path):
        return config

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            config[key.strip()] = value.strip().lower()
    return config
cfg = load_conf(os.path.expanduser("~/.config/pyfetch/pyfetch.conf"))

import platform
import getpass
import socket
import psutil
import pyfiglet
import sys
import traceback
import importlib.util
import subprocess
import argparse
import time
import requests
import random
pluginloader_path = os.path.expanduser("~/.config/pyfetch")
sys.path.append(pluginloader_path)
from pluginloader import load_plugins, run_plugins
if cfg.get('enable_plugin_guard', 'true') == 'true':
    pluginguard_path = os.path.expanduser("~/.config/pyfetch/pluginguard.py")
    spec = importlib.util.spec_from_file_location("pluginguard", pluginguard_path)
    pluginguard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pluginguard)

    # Search for activate
    if hasattr(pluginguard, "activate"):
        pluginguard.activate()
    else:
        print("pluginGuard does not define an activate() function.")
else:
    print("WARNING: PluginGuard is not enabled.")

# Load battery percentage
def get_battery_percentage():
    try:
        output = subprocess.check_output(
            "upower -i $(upower -e | grep BAT) | grep percentage",
            shell=True, text=True
        )
        return output.strip().split(":")[1].strip()
    except Exception:
        return "Battery info not available"

# Load shell version
def get_shell_version():
    shell_path = os.environ.get("SHELL", "")
    shell_name = os.path.basename(shell_path)

    try:
        version_output = subprocess.check_output([shell_name, '--version'], stderr=subprocess.STDOUT, text=True)
        return version_output.split('\n')[0]  # First line only
    except Exception:
        return f"{shell_name} (version unknown)"

# Load Public IP Address
def get_public_ip():
    try:
        ip = requests.get("https://api.ipify.org").text
        return ip
    except requests.RequestException:
        return "Unavailable"

# Load plugins
plugin_dir = os.path.expanduser("~/.config/pyfetch/plugins")
plugins = load_plugins(plugin_dir)
def run_plugins(plugins, cfg, PYFETCH_VERSION):
    from packaging import version
    for plugin in plugins:
        try:
            required = getattr(plugin, "required_version", PYFETCH_VERSION)
            if version.parse(PYFETCH_VERSION) < version.parse(required):
                print(f"Plugin '{plugin.__name__}' requires PyFetch {required}, but you're running {PYFETCH_VERSION}")
                continue

            if hasattr(plugin, "run"):
                plugin.run(cfg)

        except Exception as e:
            print(f"Plugin '{plugin.__name__}' failed: {e}")
            traceback.print_exc()

# Getting distro name
def get_distro_name():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("NAME="):
                    return line.strip().split("=")[1].strip('"')
    except FileNotFoundError:
        return None

if get_distro_name() == "Manjaro Linux":
    distro_name = "Trashjaro Linux"
else:
    distro_name = get_distro_name()

# Read raw config line (not just parsed values)
config_path = os.path.expanduser("~/.config/pyfetch/pyfetch.conf")
banner_text = None

# Checking for banner
with open(config_path) as f:
    for line in f:
        if "banner_text" in line:
            if line.strip().startswith("#"):
                banner_text = distro_name
            else:
                banner_text = line.split("=", 1)[1].strip()
            break

if banner_text is None:
    banner_text = distro_name

ascii_banner = pyfiglet.figlet_format(banner_text)
trashjaro_backup = pyfiglet.figlet_format("Trashjaro Linux")

# Find amount of packages
def get_package_count():
    managers = {
        "pacman": "pacman -Q",
        "dpkg": "dpkg -l | grep '^ii'",
        "rpm": "rpm -qa",
        "apk": "apk info",
        "xbps-query": "xbps-query -l",
        "pkg": "pkg info",
        "apt": "apt list --installed"
    }

    for cmd, query in managers.items():
        if subprocess.call(f"which {cmd}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            try:
                output = subprocess.check_output(query + " | wc -l", shell=True)
                return int(output.strip())
            except Exception:
                return None
    return None

pkg_count = get_package_count()

# Get Desktop Environment
def get_desktop_environment():
    de = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION") or "Unknown"
    if "KDE" in de.upper() or "PLASMA" in de.upper():
        return f"KDE Plasma (You have great taste!)"
    if "zorin:GNOME" in de.upper():
        return f"GNOME"
    return de

de = get_desktop_environment()

# Import fun facts
facts = [
    "Did you know that Tux the mascot is a penguin because in 1993, Linus Torvalds got bitten by a Penguin?",
    "International Linux Day is celebrated in August 25th.",
    "The creator of PyFetch is a big KDE Plasma fan.",
    "If you want the best experience with PyFetch, use Arch.",
    "Did you know Manjaro users are the only Linux users that loves suffering?",
    "Windows does not support PyFetch.",
    "Did you know Gentoo users compiled their entire soul?",
    "Be aware of penguinitis!",
    "Your IP Address is 62.57.128.236",
    "Did you know Arch users never touch grass?",
    "Does people even read these?",
    "Did you know Windows users think that Linux users are like hackers?",
    "PyFetch was inspired by Neofetch.",
    "Candice? Who's candice?",
    "The Linux kernel was created by Linus Torvalds",
    "Did you know KDE Plasma was created in October 14, 1996 and was originally named KDE for K Desktop Environment?",
    "Did you know PyFetch has the MIT License?",
    "The PyFetch github is https://github.com/linuxaddict124/pyfetch",
    "Python is great for AI!",
    "I wonder if Python websites exist.",
    "Did you know that the official PyFetch website is pyfetch.github.io?",
    "Did you know the most popular distros are based on Ubuntu?",
    "Did you know both MacOS and Ubuntu are based on Unix? I wonder why XNU stands for 'X is Not Unix' then...",
    "Java is more complicated than Python. Don't believe it? Try to print Hello World in Java.",
    "GNOME is a minimalist desktop environment that was made to be a open-source alternative to both CDE and KDE, although KDE became completely open-source after Qt switched to the GPL license."
    ]
random_fact = random.choice(facts)

# Turn entire base of PyFetch to 1 command
def pyfetchbase():
    if cfg.get('ascii_art', 'true') == 'true':
        if banner_text == "Manjaro" or banner_text == "Manjaro Linux":
            print("Autocorrecting to Trashjaro.")
            print(trashjaro_backup)
        else:
            print(ascii_banner)
    if cfg.get('show_distro', 'true') == 'true':
        print(f"Distro: {distro_name}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"User: {getpass.getuser()}")
    if cfg.get('show_kernel', 'true') == 'true':
        print(f"Kernel: {platform.system()} {platform.release()}")
    if cfg.get('show_de', 'true') == 'true':
        print(f"Desktop Environment: {de}")
    if cfg.get('show_packages', 'true') == 'true':
        if pkg_count is not None:
            print(f"Packages: {pkg_count}")
        else:
            print("Packages: Unknown")
    if cfg.get('fun_facts', 'true') == 'true':
        print("Fun Fact:", random_fact)
    if cfg.get('show_pyfversion', 'true') == 'true':
        print(f"PyFetch Version:", PYFETCH_VERSION)
    if cfg.get('show_ip', 'true') == 'true':
        print(f"Public IP: {get_public_ip()}")
    if cfg.get('show_shell_version', 'true') == 'true':
        print("Shell:", get_shell_version())
    if cfg.get('show_battery', 'true') == 'true':
        print("Battery:", get_battery_percentage())
    print(f"CPU: {os.uname().machine}")
    print(f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    if cfg.get('allow_plugins', 'true') == 'true':
        run_plugins(plugins, cfg, PYFETCH_VERSION)

def pyfetchbasenonconfig():
    if banner_text == "Manjaro" or banner_text == "Manjaro Linux":
        print("Autocorrecting to Trashjaro Linux.")
        print(trashjaro_backup)
    else:
        print(ascii_banner)
    print(f"Distro: {distro_name}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"User: {getpass.getuser()}")
    print(f"Kernel: {platform.system()} {platform.release()}")
    print(f"Desktop Environment: {de}")
    if pkg_count is not None:
        print(f"Packages: {pkg_count}")
    else:
        print("Packages: Unknown")
    print("Fun Fact:", random_fact)
    print(f"PyFetch Version:", PYFETCH_VERSION)
    print(f"Public IP: {get_public_ip()}")
    print("Shell:", get_shell_version())
    print("Battery:", get_battery_percentage())
    print(f"CPU: {os.uname().machine}")
    print(f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    run_plugins(plugins, cfg, PYFETCH_VERSION)

def nopluginsbase():
    if cfg.get('ascii_art', 'true') == 'true':
        if banner_text == "Manjaro" or banner_text == "Manjaro Linux":
            print("Autocorrecting to Trashjaro Linux.")
            print(trashjaro_backup)
        else:
            print(ascii_banner)
    if cfg.get('show_distro', 'true') == 'true':
        print(f"Distro: {distro_name}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"User: {getpass.getuser()}")
    if cfg.get('show_kernel', 'true') == 'true':
        print(f"Kernel: {platform.system()} {platform.release()}")
    if cfg.get('show_de', 'true') == 'true':
        print(f"Desktop Environment: {de}")
    if cfg.get('show_packages', 'true') == 'true':
        if pkg_count is not None:
            print(f"Packages: {pkg_count}")
        else:
            print("Packages: Unknown")
    if cfg.get('fun_facts', 'true') == 'true':
        print("Fun Fact:", random_fact)
    if cfg.get('show_pyfversion', 'true') == 'true':
        print(f"PyFetch Version:", PYFETCH_VERSION)
    if cfg.get('show_ip', 'true') == 'true':
        print(f"Public IP: {get_public_ip()}")
    if cfg.get('show_shell_version', 'true') == 'true':
        print("Shell:", get_shell_version())
    if cfg.get('show_battery', 'true') == 'true':
        print("Battery:", get_battery_percentage())
    print(f"CPU: {os.uname().machine}")
    print(f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    
def pyfetchprofile():
    profile_banner_text = None
    with open(profile_path) as f:
        for line in f:
            if "banner_text" in line:
                if line.strip().startswith("#"):
                    profile_banner_text = distro_name
                else:
                    profile_banner_text = line.split("=", 1)[1].strip()
                break
    if profile_banner_text is None:
        profile_banner_text = distro_name
    profile_ascii_banner = pyfiglet.figlet_format(profile_banner_text)
    if profile_cfg.get('ascii_art', 'true') == 'true':
        if profile_banner_text == "Manjaro" or banner_text == "Manjaro Linux":
            print("Autocorrecting to Trashjaro.")
            print(trashjaro_backup)
        else:
            print(profile_ascii_banner)
    if profile_cfg.get('show_distro', 'true') == 'true':
        print(f"Distro: {distro_name}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"User: {getpass.getuser()}")
    if profile_cfg.get('show_kernel', 'true') == 'true':
        print(f"Kernel: {platform.system()} {platform.release()}")
    if profile_cfg.get('show_de', 'true') == 'true':
        print(f"Desktop Environment: {de}")
    if profile_cfg.get('show_packages', 'true') == 'true':
        if pkg_count is not None:
            print(f"Packages: {pkg_count}")
        else:
            print("Packages: Unknown")
    if profile_cfg.get('fun_facts', 'true') == 'true':
        print("Fun Fact:", random_fact)
    if profile_cfg.get('show_pyfversion', 'true') == 'true':
        print(f"PyFetch Version:", PYFETCH_VERSION)
    if profile_cfg.get('show_ip', 'true') == 'true':
        print(f"Public IP: {get_public_ip()}")
    if profile_cfg.get('show_shell_version', 'true') == 'true':
        print("Shell:", get_shell_version())
    if profile_cfg.get('show_battery', 'true') == 'true':
        print("Battery:", get_battery_percentage())
    print(f"CPU: {os.uname().machine}")
    print(f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    if profile_cfg.get('allow_plugins', 'true') == 'true':
        run_plugins(plugins, cfg, PYFETCH_VERSION)

# Flags Manager
if cfg.get('enable_flags', 'true') == 'true':
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Python-based Neofetch Alternative")
        parser.add_argument("--minimal", action="store_true", help="Show minimal output")
        parser.add_argument("--banner", action="store_true", help="Show banner ONLY")
        parser.add_argument("--version", action="store_true", help="Version of PyFetch")
        parser.add_argument("--shell", action="store_true", help="View your bash version")
        parser.add_argument("--skipconfig", action="store_true", help="Skip pyfetch.conf")
        parser.add_argument("--noplugins", action="store_true", help="Exclude Plugins")
        parser.add_argument("--list-plugins", action="store_true", help="List all available plugins")
        parser.add_argument("--fun-fact", action="store_true", help="Show some fun facts")
        parser.add_argument("--edit-config", action="store_true", help="A easier way to edit pyfetch.conf")
        parser.add_argument("--desktop", action="store_true", help="Show your desktop environment")
        parser.add_argument("--public-ip", action="store_true", help="Show your Public IP")
        parser.add_argument("--kernel", action="store_true", help="Show your Kernel Version")
        parser.add_argument("--create-profile", metavar="NAME", help="Create a new profile")
        parser.add_argument("--profile", metavar="NAME", help="Run PyFetch with a personalized profile")
        parser.add_argument("--edit-profile", metavar="NAME", help="Edit your profile")
        parser.add_argument("--rm-profile", metavar="NAME", help="Delete a profile")
        parser.add_argument("--ls-profiles", action="store_true", help="List profiles")
        args = parser.parse_args()

        if args.minimal:
            print(f"Hostname: {socket.gethostname()}")
            print(f"User: {getpass.getuser()}")
            print(f"CPU: {os.uname().machine}")
            print(f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
            exit()

        if args.banner:
            if banner_text == "Manjaro" or banner_text == "Manjaro Linux":
                print("Autocorrecting to Trashjaro Linux.")
                print(trashjaro_backup)
            else:
                print(ascii_banner)
            exit()

        if args.version:
            print(f"PyFetch", PYFETCH_VERSION)
            exit()

        if args.shell:
            print("Shell:", get_shell_version())
            exit()

        if args.skipconfig:
            pyfetchbasenonconfig()
            exit()

        if args.noplugins:
            nopluginsbase()
            exit()

        if args.list_plugins:
            from pluginloader import load_plugins, list_plugins
            plugin_dir = os.path.expanduser("~/.config/pyfetch/plugins")
            plugins = load_plugins(plugin_dir)
            list_plugins(plugins)
            exit()

        if args.fun_fact:
            print(random_fact)
            exit()

        if args.edit_config:
            os.system('nano ~/.config/pyfetch/pyfetch.conf')
            exit()

        if args.desktop:
            print(f"Desktop Environment: {de}")
            exit()
        
        if args.public_ip:
            print(f"Public IP: {get_public_ip()}")
            exit()
        
        if args.kernel:
            print(f"Kernel: {platform.system()} {platform.release()}")
            exit()
        
        if args.create_profile:
            profile_name = args.create_profile.strip()
            source = os.path.expanduser("~/.config/pyfetch/profile.conf")
            dest = os.path.expanduser(f"~/.config/pyfetch/profiles/{profile_name}.ini")
            if os.path.exists(dest):
                print(f"Profile '{profile_name}' already exists.")
                exit(1)
            if not profile_name:
                print("Input is required. (Example: pyfetch --create-profile work)")
                exit(1)
            else:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                os.system(f"cp '{source}' '{dest}'")
                os.system(f"nano '{dest}'")
                print(f"{profile_name} has been created.")
                exit(0)
        
        if args.profile:
            profile_name = args.profile.strip()
            profile_path = os.path.expanduser(f"~/.config/pyfetch/profiles/{profile_name}.ini")
            if not os.path.exists(profile_path):
                print(f"Error: {profile_name} not found.")
                exit(1)
            if not profile_name:
                print(f"Input is required. (Example: pyfetch --profile work)")
                exit(1)
            profile_cfg = load_conf(profile_path)
            pyfetchprofile()
            exit()
        
        if args.edit_profile:
            profile_name = args.edit_profile.strip()
            path = os.path.expanduser(f"~/.config/pyfetch/profiles/{profile_name}.ini")
            if not os.path.exists(path):
                print(f"Error: {profile_name} not found.")
                exit(1)
            if not profile_name:
                print(f"Input is required. (Example: pyfetch --edit-profile work)")
                exit(1)
            os.system(f"nano {path}")
            exit()

        if args.rm_profile:
            profile_name = args.rm_profile.strip()
            path = os.path.expanduser(f"~/.config/pyfetch/profiles/{profile_name}.ini")
            if not os.path.exists(path):
                print(f"Error: {profile_name} not found.")
                exit(1)
            os.remove(path)
            print("Profile deleted successfully.")
            exit(0)

        if args.ls_profiles:
            path = os.path.expanduser("~/.config/pyfetch/profiles")
            if not os.listdir(path):
                print("The directory is empty.")
            else:
                print(os.listdir(path))
                print("Disclaimer: The file extension (.ini) is not part of the profile name.")
            exit()

        # If no flags are running
        pyfetchbase()
else:
    # Fallback
    pyfetchbase()
