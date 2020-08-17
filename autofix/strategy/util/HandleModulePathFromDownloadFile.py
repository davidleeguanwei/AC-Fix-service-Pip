import re
import os
from autofix.util.FileSystemUtil import fileWithName

py3_module_name = {"urlparse": "urllib.parse"}
py3_submodule_of_module_name = {"urlencode": "urllib.parse"}

def handleModulePathFromDownloadFile(project, path, module, submodule):
	module = module + ".py"
	module_path_list = fileWithName(project.name, module)
	module = module.replace(".py", "")
	submodule = '' if submodule is None else submodule
	file_name = path.rsplit('/', 1)[1]
	file_path_list = fileWithName(project.name, file_name)
	if len(module_path_list) != 1 or len(file_path_list) == 0:
		env_ver = project.defaultPythonVersion if project.currentPythonVersion is None else project.currentPythonVersion
		print(str(env_ver))
		if ("3" not in str(env_ver)):
			return False
		if (module not in py3_module_name) and (submodule not in py3_submodule_of_module_name):
			return False

	if len(module_path_list) == 1:
		module_path = module_path_list[0].replace(".py", "")
		module_path = module_path.replace("/", ".")
		module_path = module_path.replace(project.name + ".", "", 1)
	elif module in py3_module_name:
		module_path = py3_module_name[module]
	elif submodule in py3_submodule_of_module_name:
		module_path = py3_submodule_of_module_name[submodule]

	for i in range(len(file_path_list)):
		file_path_list[i] = file_path_list[i].rsplit('/', 1)[0] + '/'

	for file_path in file_path_list:
		file = open(file_path + file_name, 'r', encoding='utf-8', errors='ignore')
		fixed_file = open(file_path + "fix", 'w')
		line_num = 0
		flag = False
		for line in file:
			if line.find(str("from " + module + " ")) != -1:
				print("+++++++")
				print(line)
				line = line.replace(str(module), str(module_path), 1)
			elif line.find(str("import " + module + "\n")) != -1:
				line = line.replace(str(module), str(module_path), 1)
				flag = True
			elif flag == True:
				if line.find(str(module)) != -1:
					line = line.replace(str(module), str(module_path))
			fixed_file.write(line)
		file.close()
		fixed_file.close()
		cmd = "rm "+file_path + file_name
		os.system(cmd)
		os.rename(file_path + "fix", file_path + file_name)
		
	return True


if __name__ == "__main__":
		exit()
