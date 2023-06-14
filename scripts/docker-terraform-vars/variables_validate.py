import os
import re
import sys
import argparse
import json
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Argument parser for command-line arguments
parser = argparse.ArgumentParser(description='Validate environment variables.')
parser.add_argument('--dockerfile_path', type=str, required=True, help='Path to the Dockerfile')
parser.add_argument('--terraform_dir', type=str, required=True, help='Path to the Terraform directory')
parser.add_argument('--exclude', nargs='+', default=[], help='List of environment variables to exclude')
parser.add_argument('--exclude_json', type=str, help='JSON string of directory-specific excluded variables')
args = parser.parse_args()

# Get environment variables from arguments
dockerfile_path = args.dockerfile_path
terraform_dir = args.terraform_dir

# Get environment variables from Dockerfile
with open(dockerfile_path, "r") as dockerfile:
    content = dockerfile.read()
    env_vars = re.findall(r"ENV\s+(\w+)", content)

# Convert exclude list to set
except_vars = set(args.exclude if args.exclude else [])

# Load directory-specific excluded variables, if provided
dir_specific_except_vars = {}
if args.exclude_json:
    dir_specific_except_vars = json.loads(args.exclude_json)

# Track missing variables and their corresponding directories
missing_vars = {var: [] for var in env_vars if var not in except_vars}

# Iterate over all ".tf" files
for root, dirs, files in os.walk(terraform_dir):
    tf_files = filter(lambda x: x.endswith('.tf'), files)
    for tf_file in tf_files:
        tf_file_path = os.path.join(root, tf_file)
        try:
            with open(tf_file_path, "r") as tf_file_content:
                content = tf_file_content.read()

            # Determine excluded variables for this directory
            current_except_vars = except_vars
            if root in dir_specific_except_vars:
                current_except_vars = current_except_vars.union(dir_specific_except_vars[root])

            # Check if each variable is used or missing in the .tf file
            for var in missing_vars.keys():
                if var not in current_except_vars and not re.findall(r'"\s*{}\s*"'.format(var), content):
                    # Get relative subdirectory path
                    rel_subdir = os.path.relpath(root, terraform_dir)
                    if rel_subdir not in missing_vars[var]:
                        missing_vars[var].append(rel_subdir)

        except FileNotFoundError:
            pass

# Log missing variables and their corresponding directories
if any(missing_vars.values()):
    logging.error("Missing environment variables in the Terraform files:")
    for var, dirs in missing_vars.items():
        if dirs:
            logging.error(f"Variable '{var}' is missing in directories: {', '.join(dirs)}\n")
    sys.exit(1)
else:
    logging.info("All variables defined in Dockerfile have been used in deployment or are exempted.")
    sys.exit(0)
