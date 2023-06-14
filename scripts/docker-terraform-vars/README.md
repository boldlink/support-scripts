# Environment Variables Validation Script

This script is designed to validate environment variables of terraform ECS code by using the `Dockerfile` as the reference.

Developers often struggle to ensure that all environment variables defined in a Dockerfile are used in the Terraform files. 

This script is designed to solve this problem by validating the environment variables defined in a Dockerfile against those used in Terraform files. 

Additionally, it also provides an exception mechanism through an `--exclude` argument, where variables that are defined in the Dockerfile but not required during deployment can be listed.

**NOTE:** It only validates environment variables defined in the Dockerfile with `ENV` and not those defined in the Terraform files.

**NOTE:** The script will NOT validate environment variables values. It will only validate the names of the variables.

This validation script plays a crucial role in ensuring the integrity and consistency of environment variables throughout the application lifecycle. 

## Ideal Use Case

This validation ideally will be implemented as a step in a CI/CD pipeline, where it will be executed before the deployment of the application, see example [here](./examples/github_actions/validate_env_vars.yml).

If any discrepancies or missing variables are detected, the script will immediately trigger a workflow failure, prompting for necessary corrections. 

## Requirements

* Python 3.11 or higher.

## Prerequisites and Assumptions

For the successful execution of this script, the following conditions must be met:

- **Common Dockerfile**: There should be a common Dockerfile located at a specific location. This location should be provided when running the workflow as **`DOCKERFILE_PATH`** or `--dockerfile_path` argument.

- **Terraform Configuration**: There should be a directory containing Terraform configuration files (`*.tf`). This directory might consist of various subdirectories. 

The location of the directory containing the Terraform configurations should be provided via the **`TERRAFORM_DIR`** variable in the workflow or `--terraform_dir` argument.

### Script Arguments
The script requires the following arguments for its execution:

1. **`--dockerfile_path`**: The path to the Dockerfile containing the environment variables to be validated. This argument is mandatory. It is referred to as **`DOCKERFILE_PATH`** within the example workflow section below in `Usage Example`.

2. **`--terraform_dir`**: The path to the directory containing Terraform configurations and environment variables to be validated. This argument is mandatory and is referred to as **`TERRAFORM_DIR`** within the example workflow section below in `Usage Example`.

3. **`--exclude`**: This is an optional argument containing a list of variables to exclude from validation. In the example section below, this is provided by the environment variable called  **`EXCLUDED_VARS`**. It is provided in the format `--exclude VAR1 VAR2 VAR3 VAR4 ...and so on`

### Running the script manually
The script can be run with the following command on the linux terminal:

```console
python support-scripts/scripts/docker-terraform-vars/variables_validate.py --dockerfile_path <dockerfile_path_here> --terraform_dir <terraform_dir_here> --exclude VAR1 VAR2 VAR3 VAR4...
```

### Script Output
1. **When a variable is defined in Dockerfile and not used nor exempted**

- When there are missing variables which have been defined in Dockerfile and which have not been used nor exempted using `--exclude` argument, the script will give the following output

#### Example of error output
```
[Error]: Missing environment variables in the following Terraform files:
File: ./terraform/file_name.tf
Missing Variables: VAR1

```

- When used in a github workflow, the following is the output when there is a missing variable:

```console
Run python $GITHUB_WORKSPACE/support-scripts/scripts/docker-terraform-vars/variables_validate.py --dockerfile_path ./Dockerfile --terraform_dir ./terraform/ --exclude VAR3 VAR2 VAR4
[Error]: Missing environment variables in the following Terraform files:
File: ./terraform/file_name.tf
Missing Variables: VAR1

Error: Process completed with exit code 1.
```

- You will get the following output on the linux terminal when there is a missing variable:
```
[Error]: Missing environment variables in the following Terraform files:
File: ./terraform/file_name.tf
Missing Variables: VAR1

Error: Process completed with exit code 1.
```

2. **When all variables defined in Dockerfile have been used or exempted**

- When variables defined in Dockerfile have been used or exempted using the `--exclude` argument, the following is the output on the linux terminal

```
[Info]: All variables defined in Dockerfile have been used in deployment or are exempted.
```

- When used in a github workflow, the following is the output when variables are used in deployment or have been exempted.

```console
Run python $GITHUB_WORKSPACE/support-scripts/scripts/docker-terraform-vars/variables_validate.py --dockerfile_path ./Dockerfile --terraform_dir ./terraform/ --exclude VAR3 VAR2 VAR4 VAR1
[Info]: All variables defined in Dockerfile have been used in deployment or are exempted.
```

## Usage Example in Github Workflow

See example [here](./examples/github_actions/validate_env_vars.yml) for usage in github workflow.
