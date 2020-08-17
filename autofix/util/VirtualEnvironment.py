import os, signal
import subprocess
import psutil
import time
from autofix.util.Config import Config
from autofix.util.LoggingUtil import Logger


class VirtualEnvironment:

    def __init__(self):
        pass

    def createVirtualenv(self, env_ver, env_name):
        os.system("virtualenv "+"--python=python"+str(env_ver)+" "+env_name)

    def deleteVirtualenv(self, env_name):
        os.system("rm -rf "+env_name)

    def executeIn(self, command):

        status = None
        log = None

        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as p:
            try:
                output, log = p.communicate(timeout=600)
                status = "SUCCESS" if p.poll() == 0 else "INSTALLED_FAILED"
            except subprocess.TimeoutExpired:
                p.kill()
                #p.communicate()
                log = "exceed time limit".encode('utf-8')
                status = "EXCEED_TIME_LIMIT"
                
        return status, log

    def pipUpgrade(self, env_name):
        os.system("./"+env_name+"/bin/python -m pip install --upgrade pip")

    def pipDownload(self, env_ver, env_name, repo):
        cmd = ". "+env_name+"/bin/activate && pip download --build . "+repo+" --no-clean --no-deps"
        self.executeIn(cmd)
        os.system("rm *.tar.gz")
        os.system("rm *.whl")

    def pipInstall(self, env_ver, env_name, repo, log_path):
        file_path = log_path + "/error_"+repo
        if os.path.isdir(repo):
            repo = repo + "/"
        cmd = ". "+env_name+"/bin/activate && "+"pip install "+repo
        status, log = self.executeIn(cmd)
        if status != "SUCCESS":
            pip_log_file = open(file_path, "w+")
            pip_log_file.write("pip install failed Output: \n{}\n".format(log.decode("utf-8")))
            pip_log_file.close()


        return status

    def pipGitInstall(self, env_ver, env_name, git_repo, log_path):
        repo = env_name.replace("test_env_", "")
        file_path = log_path + "/error_"+repo
        cmd = ". "+env_name+"/bin/activate && "+"pip install git+"+git_repo
        status, log = self.executeIn(cmd)
        if status != "SUCCESS":
            pip_log_file = open(file_path, "w+")
            pip_log_file.write("pip install failed Output: \n{}\n".format(log.decode("utf-8")))
            pip_log_file.close()

        return status

    def compileall(self, env_ver, env_name, repo, log_path):
        file_path = log_path + "/error_"+repo
        pwd = "./"+env_name+"/lib/python"+str(env_ver)+"/site-packages"
        python_home = Config().get('PYTHON_HOME', 'PYTHON_'+str(env_ver)+'_HOME')
        os.system(python_home + " --version")

        cmd = python_home + " -m compileall " + pwd
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as exc:
            interpret_log_file = open(file_path, "w+")
            interpret_log_file.write("compile all failed Output: \n{}\n".format(exc.output.decode('utf-8')))
            interpret_log_file.close()
            return "COMPILED_FAILED"


        return "SUCCESS"
