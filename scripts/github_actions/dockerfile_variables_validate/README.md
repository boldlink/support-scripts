# Environment Variables Validation Script
The Environment Variables Validation script is a robust way designed to validate environment variables. It cross-verifies variables defined in a Dockerfile against those used in Terraform files. Additionally, it also provides an exception mechanism through an `--exclude` argument, where variables that are defined in the Dockerfile but not required during deployment can be listed.

This validation script plays a crucial role in ensuring the integrity and consistency of environment variables throughout the application lifecycle. If any discrepancies or missing variables are detected, the script will immediately trigger a workflow failure, prompting for necessary corrections. The underlying mechanism for execution is Python 3.11.

## Prerequisites and Assumptions
For the successful execution of this script, the following conditions must be met:

- **Common Dockerfile**: There should be a common Dockerfile located at a specific location. This location should be provided when running the workflow as **`DOCKERFILE_PATH`**.

- **Terraform Configuration**: There should be a directory containing Terraform configuration files (`*.tf`). This directory might consist of various subdirectories, and it is expected that some of these subdirectories will contain `env_vars.tf` files. The location of the directory containing the Terraform configurations should be provided via the **`TERRAFORM_DIR`** variable in the workflow.

### Script Arguments
The script requires the following arguments for its execution:

1. **`--dockerfile_path`**: The path to the Dockerfile containing the environment variables to be validated. This argument is mandatory. It is referred to as **`DOCKERFILE_PATH`** within the example workflow section below in `Usage Example`.

2. **`--terraform_dir`**: The path to the directory containing Terraform configurations and environment variables to be validated. This argument is mandatory and is referred to as **`TERRAFORM_DIR`** within the example workflow section below in `Usage Example`.

3. **`--exclude`**: This is an optional argument containing a list of variables to exclude from validation. In the example section below, this is provided by the environment variable called  **`EXCLUDED_VARS`**. It is provided in the format `--exclude VAR1 VAR2 VAR3 VAR4 ...and so on`

### Running the script manually
The script can be run with the following command on the linux terminal:
```
python support-scripts/scripts/github_actions/dockerfile_variables_validate/variables_validate.py --dockerfile_path <dockerfile_path_here> --terraform_dir <terraform_dir_here> --exclude VAR1 VAR2 VAR3 VAR4...
```

### Usage Example
To include the Environment Variables Validation script in your workflow, add it as a step in your workflow file as shown below.
```yaml
name: env variables validate

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
  EXCLUDED_VARS: USER UID APP_HOME
  
jobs:
  test-workflow:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout current repository
        uses: actions/checkout@v3
      
      - name: Checkout Script Repository
        uses: actions/checkout@v3
        with:
          repository: 'boldlink/support-scripts'
          ref: 'main'
          path: 'support-scripts'
          
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
                    
      - name: Validate variables
        run: python $GITHUB_WORKSPACE/support-scripts/scripts/github_actions/dockerfile_variables_validate/variables_validate.py --dockerfile_path ${{ env.DOCKERFILE_PATH }} --terraform_dir ${{ env.TERRAFORM_DIR }} --exclude ${{ env.EXCLUDED_VARS }}
```

Please ensure that `<path-to-your-dockerfile>` and `<path-to-your-terraform-directory>` are replaced with the actual paths to your Dockerfile and Terraform directory, respectively.
