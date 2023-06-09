import os
import re
import sys

# Directory paths
DOCKERFILE_PATH = ""
TERRAFORM_DIR = ""

# Get environment variables from Dockerfile
with open(DOCKERFILE_PATH, 'r') as dockerfile:
    content = dockerfile.read()
    env_vars = re.findall(r'ENV\s+(\w+)', content)

# Track missing variables and their corresponding files
missing_vars = {}

# Iterate over env_vars.tf files
for root, _, files in os.walk(TERRAFORM_DIR):
    if "env_vars.tf" in files:
        env_vars_file_path = os.path.join(root, "env_vars.tf")
        except_file_path = os.path.join(root, "except.txt")
        except_vars = set()

        if os.path.exists(except_file_path):
            with open(except_file_path, 'r') as except_file:
                except_vars = set(except_file.read().splitlines())

        try:
            with open(env_vars_file_path, 'r') as env_vars_file:
                env_vars_content = env_vars_file.read()

            # Extract variable names from env_vars.tf
            variable_names = re.findall(r'name\s+=\s+"(\w+)"', env_vars_content)

            # Check if each variable is used or missing in except.txt
            for var in env_vars:
                if var not in variable_names and var not in except_vars:
                    if env_vars_file_path not in missing_vars:
                        missing_vars[env_vars_file_path] = []
                    missing_vars[env_vars_file_path].append(var)

        except FileNotFoundError:
            pass

# Display missing variables and their corresponding files
if missing_vars:
    print("Missing environment variables in the following Terraform files:")
    for file, vars in missing_vars.items():
        print(f"File: {file}")
        print(f"Missing Variables: {', '.join(vars)}\n")
    sys.exit(1)
else:
    print("All environment variables are either used or listed in except.txt.")
    sys.exit(0)
