import boto3
import subprocess
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('--should-skip-s3-retrieval', help='This parameter specifies whether this script should execute at all or not.', type=bool, default=False)
parser.add_argument('--s3-bucket', help='This parameter specifies the S3 Bucket to retrieve the zip file from', type=str)
parser.add_argument('--s3-artifact-key', help='This parameter specifies the artifact key in the S3 bucket', type=str)
parser.add_argument('--virtualhost-directory-path', help='This parameter specifies the directory path of the virtualhost where the S3 artifact will be extracted to', type=str)


args=parser.parse_args()

def header(title):
    print("")
    print("#################")
    print(title)
    print("#################")
    print("")

def success():
    print("  - Success.")

s3 = boto3.resource("s3")

#
# Validating the required parameters
#
header("Required environment variables")

should_skip_s3_retrieval = args.should_skip_s3_retrieval
s3_bucket = args.s3_bucket
s3_artifact_key = args.s3_artifact_key
virtualhost_directory_path = args.virtualhost_directory_path

print("SHOULD_SKIP_S3_RETRIEVAL: " + str(should_skip_s3_retrieval))
print("S3_BUCKET: " + s3_bucket)
print("S3_ARTIFACT_KEY: " + s3_artifact_key)
print("VIRTUALHOST_DIRECTORY_PATH: " + virtualhost_directory_path)

#
# Download and unzip from S3
#

header("Download and unzip from S3")

if should_skip_s3_retrieval:
    print("- Skipping S3 retrieval")
    sys.exit()

print("- Retrieve the file from S3")
s3.Bucket(s3_bucket).download_file(s3_artifact_key, "/tmp/deployment.zip")
success()

print("- Unzipping the content")
subprocess.call(["unzip", "-o", "-q", "/tmp/deployment.zip", "-d", "/tmp/deployment/"])
success()

print("- Copying the files to '" + virtualhost_directory_path + "'")
subprocess.call(["cp", "-R", "/tmp/deployment/", virtualhost_directory_path])
success()
