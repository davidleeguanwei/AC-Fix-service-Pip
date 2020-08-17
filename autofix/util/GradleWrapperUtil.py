import re
import os
import sys
import datetime
import subprocess
from autofix.util.FileUtil import readFileContent, readFileContentByLine
from autofix.util.FileSystemUtil import removePath, renameFile, createDir, copyFile
from autofix.util.OSUtil import cd
from autofix.util.version.GradleVersion import GradleVersion


def findWrapperScript(base: str) -> str:
    """Return a string

    :param base: directory to search
    :return: possible file path of gradle wrapper script
    """
    for file in ['gradlew', 'gradlew.bat', 'gradle', 'gradle.bat']:
        path = os.path.join(base, file)
        if os.path.exists(path) and os.path.isfile(path):
            return path
    return ''


def findWrapperJar(base: str) -> str:
    """Return a string

    :param base: directory to search
    :return: possible file path of gradle wrapper jar
    """
    pattern = re.compile(r'CLASSPATH[ \t]*=[ \t]*(.+)')
    content = readFileContent(findWrapperScript(base))
    m = pattern.search(content)
    path = re.sub(r'\\', '/', m.group(1)) if m is not None else './gradle/wrapper/gradle-wrapper.jar'
    return '' if '/' not in path else os.path.join(base, path.split('/', 1)[1])


def findWrapperProperties(base: str) -> str:
    """Return a string

    :param base: directory to search
    :return: possible file path of gradle wrapper properties
    """
    return re.sub(r'\.jar$', '.properties', findWrapperJar(base))


def wrapGradle(base: str, version: str) -> str:
    """Return a string

    Wrapping steps:
    1. Remove or rename files in order to safely wrap the project
    2. Execute Gradle wrapper command
    3. Get current Gradle wrapper home (Make sure Gradle zip is downloaded)
    4. Recover the renamed files

    :param base: project directory to wrap
    :param version: Gradle version
    :return: path to the wrapped Gradle home, empty string if failed
    """
    gradle_dir = os.path.join(base, 'gradle')
    wrapper_dir = os.path.join(base, 'gradle/wrapper')
    build_kts_file = os.path.join(base, 'build.gradle.kts')
    build_file = os.path.join(base, 'build.gradle')
    settings_file = os.path.join(base, 'settings.gradle')
    property_file = os.path.join(base, 'gradle.properties')
    buildsrc_dir = os.path.join(base, 'buildSrc')
    ext = '-{}.tmp'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    home = ''

    # Step 1
    if os.path.exists(gradle_dir) and not os.path.isdir(gradle_dir):
        if not removePath(gradle_dir):
            return ''
    if os.path.exists(wrapper_dir) and not os.path.isdir(wrapper_dir):
        if not removePath(wrapper_dir):
            return ''
    if os.path.exists(build_kts_file) and os.path.isfile(build_kts_file):
        pat = re.compile(r'^[ \t]*rootProject.buildFileName[ \t]*=[ \t]*[\'"]build.gradle.kts[\'"][ \t]*$')
        content = [line for line in readFileContentByLine(settings_file) if pat.fullmatch(line.strip()) is None]
        with open(settings_file, 'w') as f:
            f.write(''.join(content))
        if not removePath(build_kts_file):
            return ''
    if os.path.exists(build_file) and os.path.isfile(build_file):
        if not renameFile(build_file, build_file + ext):
            return ''
    if os.path.exists(settings_file) and os.path.isfile(settings_file):
        if not renameFile(settings_file, settings_file + ext):
            return ''
    if os.path.exists(property_file) and os.path.isfile(property_file):
        if not renameFile(property_file, property_file + ext):
            return ''
    if os.path.exists(buildsrc_dir) and os.path.isdir(buildsrc_dir):
        if not renameFile(buildsrc_dir, buildsrc_dir + ext):
            return ''

    # Step 2
    if GradleVersion(version) <= GradleVersion('0.8'):
        if not oldGradleWrapper(base, version):
            return ''
    else:
        with cd(base):
            cmd = ['gradle', 'wrapper', '--gradle-version', version]
            p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            p.communicate()
            if p.poll() != 0:
                return ''

    # Step 3
    with cd(base):
        with open(build_file, 'w') as f:
            if GradleVersion(version) <= GradleVersion('0.7'):
                f.write('task printHome { doLast { println build.gradleHomeDir } }')
            else:
                f.write('task printHome { doLast { println gradle.gradleHomeDir } }')
        cmd = ['./gradlew', 'printHome']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        out = p.communicate()[0].decode().split('\n')
        paths = [line for line in out if os.path.exists(line)]
        home = home if len(paths) == 0 else paths[-1]
        if p.poll() != 0 or len(home) == 0 or not removePath(build_file):
            return ''

    # Step 4
    if os.path.exists(build_file + ext):
        if not renameFile(build_file + ext, build_file):
            return ''
    if os.path.exists(settings_file + ext):
        if not renameFile(settings_file + ext, settings_file):
            return ''
    if os.path.exists(property_file + ext):
        if not renameFile(property_file + ext, property_file):
            return ''
    if os.path.exists(buildsrc_dir + ext):
        if not renameFile(buildsrc_dir + ext, buildsrc_dir):
            return ''

    return home


def oldGradleWrapper(base: str, version: str) -> bool:
    """Return a boolean

    :param base: project directory to wrap
    :param version: Gradle version
    :return: whether the wrapping of old Gradle wrapper succeed
    """
    files = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'OldGradleWrapperFile/{}'.format(version))
    src_s = os.path.join(files, 'gradlew')
    src_j = os.path.join(files, 'gradle-wrapper.jar')
    src_p = os.path.join(files, 'gradle-wrapper.properties')
    dst_s = os.path.join(base, 'gradlew')
    dst_j = os.path.join(base, 'gradle/wrapper/gradle-wrapper.jar')
    dst_p = os.path.join(base, 'gradle/wrapper/gradle-wrapper.properties')
    if not createDir(os.path.join(base, 'gradle/wrapper')):
        return False
    if not copyFile(src_s, dst_s) or not copyFile(src_j, dst_j) or not copyFile(src_p, dst_p):
        return False
    return True


if __name__ == '__main__':
    exit()
