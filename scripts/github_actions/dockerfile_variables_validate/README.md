# Environment Variables Validation Action
The Environment Variables Validation Action is a robust GitHub composite action designed to validate environment variables. It cross-verifies variables defined in a Dockerfile against those used in Terraform files. Additionally, it also provides an exception mechanism through an `except.txt` file, where variables that are defined in the Dockerfile but not required during deployment can be listed.

This validation action plays a crucial role in ensuring the integrity and consistency of environment variables throughout the application lifecycle. If any discrepancies or missing variables are detected, the action will immediately trigger a workflow failure, prompting for necessary corrections. The underlying mechanism for execution is Python 3.11.

## Prerequisites and Assumptions
For the successful execution of this action, the following conditions must be met:

- **Common Dockerfile**: There should be a common Dockerfile located at a specific location. This location should be provided when running the workflow as **`DOCKERFILE_PATH`**.

- **Terraform Configuration**: There should be a directory containing Terraform configuration files (`*.tf`). This directory might consist of various subdirectories, and it is expected that some of these subdirectories will contain `env_vars.tf` files.

- **`Exception List`**: For each directory containing an `env_vars.tf` file, an `except.txt` file should be present. This text file should list any variables that are defined in the Dockerfile but not required during deployment.
The location of the directory containing the Terraform configurations should be provided via the **`TERRAFORM_DIR`** variable in the workflow.

### Inputs
The action requires the following inputs for its execution:

1. **`dockerfile_path`**: The path to the Dockerfile containing the environment variables to be validated. This input is mandatory. It is referred to as **`DOCKERFILE_PATH`** within the workflow.

2. **`terraform_dir`**: The path to the directory containing Terraform configurations and environment variables to be validated. This input is mandatory and is referred to as **`TERRAFORM_DIR`** within the workflow.

3. **`except_file_name`**: The path to the excemption/exception list file. This input is mandatory and is referred to as **`EXCEPT_FILE_NAME`**

### Usage Example
To include the Environment Variables Validation Action in your workflow, add it as a step in your workflow file.
```yaml
name: Validate Environment Variables

on:
  push:
    branches:
      - 'feature/*'
      - 'features/*'
      - 'release/*'
      - 'releases/*'

env:
  DOCKERFILE_PATH: "<path-to-your-dockerfile>"
  TERRAFORM_DIR: "<path-to-your-terraform-directory>"
  EXCEPT_FILE_NAME: "<path-to-your-exception/exemption-file>"
  
jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3
        
      - name: Run Environment Variables Validation
        uses: boldlink/support-scripts/scripts/github_actions/dockerfile_variables_validate/examples@main
        with:
          dockerfile_path: ${{ env.DOCKERFILE_PATH }}
          terraform_dir: ${{ env.TERRAFORM_DIR }}
          except_file_name: ${{ env.EXCEPT_FILE_NAME }}
```

Please ensure that `<path-to-your-dockerfile>` and `<path-to-your-terraform-directory>` are replaced with the actual paths to your Dockerfile and Terraform directory, respectively.
