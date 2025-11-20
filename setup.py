#!/usr/bin/env python3
import os
import subprocess
import sys

def run(cmd):
    print(f"\n=== Running: {cmd} ===")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(result.returncode)

def main():
    # Must be root or using sudo
    if os.geteuid() != 0:
        print("Please run this script using sudo:")
        print("sudo python3 setup_docker.py")
        sys.exit(1)

    print("\nUpdating system...")
    run("apt-get update -y")
    run("apt-get upgrade -y")

    print("\nInstalling required dependencies...")
    run("apt-get install -y ca-certificates curl gnupg lsb-release")

    print("\nAdding Docker GPG key...")
    run("install -m 0755 -d /etc/apt/keyrings")
    run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.gpg")
    run("chmod a+r /etc/apt/keyrings/docker.gpg")

    print("\nAdding Docker repository...")
    distro = subprocess.getoutput("lsb_release -cs")
    run(f'echo "deb [arch=$(dpkg --print-architecture) '
        f'signed-by=/etc/apt/keyrings/docker.gpg] '
        f'https://download.docker.com/linux/ubuntu {distro} stable" '
        f'> /etc/apt/sources.list.d/docker.list')

    print("\nUpdating package list...")
    run("apt-get update -y")

    print("\nInstalling Docker engine...")
    run("apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")

    print("\nAdding current user to docker group...")
    username = os.getenv("SUDO_USER") or os.getenv("USER")
    run(f"usermod -aG docker {username}")

    print("\nChecking Docker version...")
    run("docker --version")

    print("\nChecking Docker Compose version...")
    run("docker compose version")

    print("\nRunning Docker test container...")
    run("docker run --rm hello-world")

    print("\nALL DONE ✔️")
    print("You must log out and log back in for docker group permissions to apply.")
    print("After logging back in, test with: docker run hello-world")


if __name__ == "__main__":
    main()
