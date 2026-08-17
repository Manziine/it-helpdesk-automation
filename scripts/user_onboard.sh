#!/usr/bin/env bash
# user_onboard.sh — Automate new Linux user creation
# Usage: sudo bash scripts/user_onboard.sh --username jdoe --fullname "Jane Doe" --group developers
# Requires: root or sudo

set -euo pipefail

USERNAME=""
FULLNAME=""
GROUP="users"
while [[ $# -gt 0 ]]; do
    case $1 in
        --username) USERNAME="$2"; shift 2;;
        --fullname) FULLNAME="$2"; shift 2;;
        --group) GROUP="$2"; shift 2;;
        *) echo "Unknown option: $1"; exit 1;;
    esac
done

[[ -z "$USERNAME" ]] && { echo "Error: --username required"; exit 1; }

# Generate secure random password
PASSWORD=$(openssl rand -base64 16)

# Create group if it doesn't exist
groupadd "$GROUP" 2>/dev/null || true

# Create user
useradd -m -s /bin/bash -c "$FULLNAME" -G "$GROUP" "$USERNAME"
echo "$USERNAME:$PASSWORD" | chpasswd
passwd -e "$USERNAME"  # Force password change on first login

# Setup SSH directory
mkdir -p "/home/$USERNAME/.ssh"
chmod 700 "/home/$USERNAME/.ssh"
chown "$USERNAME:$USERNAME" "/home/$USERNAME/.ssh"

echo "User '$USERNAME' created successfully."
echo "Temporary password: $PASSWORD"
echo "Note: Password change required on first login."