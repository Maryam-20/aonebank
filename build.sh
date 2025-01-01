ECHO is on.
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate --noinput

# Convert static asset files
python manage.py collectstatic --no-input
