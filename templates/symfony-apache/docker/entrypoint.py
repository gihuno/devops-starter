import os
import sys
import boto3
import subprocess

def header(title):
    print("")
    print("#################")
    print(title)
    print("#################")
    print("")

def success():
    print("  - Success.")

def get_environment_variable(environment_variable, exit_if_null = True, default_value = None):
    value = os.getenv(environment_variable)

    if value is None:
        if exit_if_null is True:
            sys.exit("The environment variable : '" + environment_variable + "' wasn't declared. The program cannot continue.")
        else:
            return default_value

    return value

s3 = boto3.resource("s3")
ssm = boto3.client('ssm')

#
# Validating the required parameters
#
header("Required environment variables")
virtualhost_config_file = get_environment_variable("VIRTUALHOST_CONFIG_FILE")
virtualhost_directory_path = get_environment_variable("VIRTUALHOST_DIRECTORY_PATH")
app_env = get_environment_variable("APP_ENV")
debug_mode = get_environment_variable("DEBUG_MODE", False, False) == "true"
clear_cache_on_startup = get_environment_variable("SYMFONY_CLEAR_CACHE_ON_STARTUP", False, False) == "true"
update_directory_permissions = get_environment_variable("SYMFONY_UPDATE_DIRECTORY_PERMISSIONS", False, False) == "true"

print("VIRTUALHOST_CONFIG_FILE: " + virtualhost_config_file)
print("VIRTUALHOST_DIRECTORY_PATH: " + virtualhost_directory_path)
print("APP_ENV: " + app_env)
print("DEBUG_MODE: " + str(debug_mode))
print("SYMFONY_CLEAR_CACHE_ON_STARTUP: " + str(clear_cache_on_startup))
print("SYMFONY_UPDATE_DIRECTORY_PERMISSIONS: " + str(update_directory_permissions))

#
# Output the container specifications
#
header("Container Specifications")

print("- Memory")
subprocess.call(["free", "-m"])
success()

print("- Space Left on disk")
subprocess.call(["df", "-h"])
success()

#
# Load the SSM Environment variables into environment variables
#
header("Loading the SSM environment variables")

for key in list(os.environ):
    if key.startswith("SSM_SECURE"):
        configuration_key = key[len("SSM_SECURE")+1:]
        ssm_key = get_environment_variable(key, False, None)
        print("- Found the environment variable '" + key + "', will be resolved and decrypted from SSM and be available as the environment variable: '" + configuration_key + "'.")

        parameter_value = ssm.get_parameter(Name=ssm_key, WithDecryption=True)['Parameter']['Value']

        os.environ[configuration_key] = parameter_value
    elif key.startswith("SSM"):
        configuration_key = key[len("SSM")+1:]
        ssm_key = get_environment_variable(key, False, None)
        print("- Found the environment variable '" + key + "', will be resolved from SSM and be available as the environment variable: '" + configuration_key + "'.")

        parameter_value = ssm.get_parameter(Name=ssm_key, WithDecryption=True)['Parameter']['Value']

        os.environ[configuration_key] = parameter_value

success()

#
# Adding the environment variables to the virtualhost configuration file
#
header("Adding the environment variables to file: '" + virtualhost_config_file + "'")

# Building the string in the Apache format to set the environment variables
apache_environment_variables = ""

for param in os.environ.keys():
    apache_environment_variables = apache_environment_variables + "    SetEnv " + param + " " + os.environ[param] + "\n"

with open(virtualhost_config_file) as f:
    updated_virtualhost_conf = f.read()
    updated_virtualhost_conf = updated_virtualhost_conf.replace('# {DOCKER_APACHE_ENVIRONMENTS}', apache_environment_variables)

    with open(virtualhost_config_file, "w") as w:
        w.write(updated_virtualhost_conf)

success()

# Output the content of the config file
if debug_mode:
    print("- Output the content of '" + virtualhost_config_file + "', DEBUG_MODE activated.")
    with open(virtualhost_config_file) as f:
        print(" - Content of the '" + virtualhost_config_file + "'")
        print(f.read())

success()

#
# Kickstart the Symfony website
#

header("Kickstart the Symfony website")

if clear_cache_on_startup is True:
    print("- Initializing the Cache")
    subprocess.call([virtualhost_directory_path + "/bin/console", "cache:warmup", "--env=" + app_env])
    success()
else:
    print("- We are not executing cache:warmup.")

if update_directory_permissions is True:
    print("- Update the permissions of directory: '" + virtualhost_directory_path + "'")
    os.system("chmod -R 770 " + virtualhost_directory_path)
    os.system("chown -R :www-data " + virtualhost_directory_path)
    os.system("chmod 774 " + virtualhost_directory_path + "/public/.htaccess")
    success()
else:
    print("- Not updating the permissions")

print("")
print("------------------------------------------------------------------")
print(" Starting Apache in Foreground mode with apachectl -D FOREGROUND")
print("------------------------------------------------------------------")
print("")

print("- Starting Apache in the foreground")
os.system("apachectl -D FOREGROUND")
