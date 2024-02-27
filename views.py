from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .serializers import CreateDockerImageSerializer
from django.templatetags.static import static
import subprocess
import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
apps_json_file_path = os.path.join(base_dir, 'apps.json')
container_file_path = os.path.join(base_dir, 'images/custom/Containerfile')



# FUNCTION TO CONVERT BASE64
def ConvertToBASE64(input_file_path, output_file_path):
    try:
        base64_command = f"export {output_file_path}=$(base64 -w 0 {input_file_path})"
        base64_output = subprocess.Popen(
            base64_command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = base64_output.communicate()

        if stdout:
            print(stdout.decode())

        if stderr:
            print(stderr.decode())

        print("File Has Been Successfully Converted to BASE64")

    except Exception as e:
        print(f"Error Converting File to BASE64 : {e}")


# FUNCTION TO DOCKER BUILD
def DockerBuild(base64_json_file, container_file_path, repo_name_and_tag):
    try:
        docker_build_command = f"""docker build \
                                        --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe \
                                        --build-arg=FRAPPE_BRANCH=version-15 \
                                        --build-arg=PYTHON_VERSION=3.11.6 \
                                        --build-arg=NODE_VERSION=18.18.2 \
                                        --build-arg=APPS_JSON_BASE64=${base64_json_file} \
                                        --tag={repo_name_and_tag} \
                                        --file={container_file_path} ."""
        docker_command_output = subprocess.Popen(
            docker_build_command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = docker_command_output.communicate()

        if stdout:
            print(stdout)

        if stderr:
            print(stderr)

        print("The Docker File Has Been Created Successfully")

    except Exception as e:
        print(f"Error While Create Docker image : {e}")


# FUNCTION TO LOGIN TO DOCKER
def LoginToDocker(username, password):
    try:

        docker_login_command = f"""docker logout
                                            docker login -u {username} -p {password}"""

        login_command_output = subprocess.Popen(
            docker_login_command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = login_command_output.communicate()

        if stdout:
            print(stdout)

        if stderr:
            print(stderr)

        print("Login Successful")

    except Exception as e:
        print(f"Error in Login : {e}")


# FUNCTION TO PUSH IMAGE TO DOCKER
def PushImageToDocker(repo_name_and_tag):
    try:
        docker_push_command = f"docker push {repo_name_and_tag}"

        push_command_output = subprocess.Popen(
            docker_push_command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = push_command_output.communicate()

        if stdout:
            print(stdout)

        if stderr:
            print(stderr)

        print("The Image is Successfully Pushed to Docker Repository")

    except Exception as e:
        print(f"There is an error while pushing to docker repository : {e}")


# Create your views here.
class CreateDockerImage(View):
    def get(self, request):

        ConvertToBASE64(apps_json_file_path, "APPS_JSON_BASE64")
        DockerBuild("APPS_JSON_BASE64", container_file_path, "karanwebisoft/uctest:1.0.0")
        LoginToDocker("karanwebisoft", "dckr_pat_eYQUrthdbh3Zd75oCYybYvzh6sY")
        PushImageToDocker("karanwebisoft/uctest:1.0.0")

        return render(request, "test.html", {"data": "Some data"})


class APICreaateDockerImage(APIView):
    def post(self, request):
        serializer = CreateDockerImageSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data["data"]
            result=""

            if data:
                try:
                    ConvertToBASE64(apps_json_file_path, "APPS_JSON_BASE64")
                    DockerBuild("APPS_JSON_BASE64", container_file_path, "karanwebisoft/uctest:1.0.0")
                    LoginToDocker("karanwebisoft", "dckr_pat_eYQUrthdbh3Zd75oCYybYvzh6sY")
                    PushImageToDocker("karanwebisoft/uctest:1.0.0")

                    result = f"Image Is Successfully Pushed"

                except Exception as e:
                    result = f"Error While Creatig Image {e}"

            else:
                result="Please Enter Data"

            return Response({"result": result}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
