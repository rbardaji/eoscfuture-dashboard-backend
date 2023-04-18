# Creating a Python Virtual Environment Using venv

Python virtual environments provide isolated development environments, enabling you to manage project-specific dependencies separately from other projects. In this tutorial, you will learn how to create a virtual environment using the venv module in Python 3.

## Step 1: No Installation Required for venv

Since the venv module is included in Python 3, there's no need to install it separately.

## Step 2: Creating a Virtual Environment

First, create a directory for your project. Next, set up a virtual environment in the project directory with the following command:

```shell
python -m venv path/to/my_project
```

## Step 3: Activating the Virtual Environment

After creating the virtual environment, activate it using the command below:

```shell
source path/to/my_project/bin/activate
```

Step 4: Installing Dependencies

Now, you can install the required dependencies for your project. Use the pip command to install them from the requirements.txt file.

```shell
pip install -r docker/generic-api/requirements.txt
```

## Executing Code

To run the code, use the command line tool "uvicorn" and execute the command uvicorn `app.main:app --reload` in the root folder.

It is advised to test and debug the code locally on your computer before deploying it to a production environment.

## Running Tests

If you have made changes to the code, it's recommended to run the pytest tests to ensure that the modifications do not break any existing functionality. To run the tests, type the command `pytest` in the root directory of the repository.
