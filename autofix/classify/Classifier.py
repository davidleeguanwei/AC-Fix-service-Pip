import re
import json
from autofix.classify.Classification import Classification
from autofix.util.Singleton import Singleton
from autofix.util.FileUtil import readFileContent
from autofix.util.FileSystemUtil import fileWithExtension


class Classifier(metaclass=Singleton):
    def __init__(self):
        self._types = list()
        for file in sorted(fileWithExtension('autofix/classify/pattern', 'json')):
            with open(file) as src:
                self._types.append(json.load(src))
                for pattern in self._types[-1]['Pattern']:
                    pattern['regex'] = re.compile(pattern['regex'])

    def classify(self, path: str) -> Classification:
        content = readFileContent(path)
        for obj in self._types:
            classification = Classifier.matchPattern(content, obj)
            if classification is not None:
                return classification
        return Classification('9', 'cannot_be_fixed', tuple(), tuple())

    @staticmethod
    def matchPattern(content: str, error: dict) -> Classification or None:
        for pattern in error['Pattern']:
            m = pattern['regex'].search(content)
            if m is None:
                continue
            for apply in pattern['apply']:
                if not Classifier.matchGroup(m.groups(), apply['group']):
                    continue
                return Classification(error['Type'], error['Strategy'], m.groups(),
                                      Classifier.matchParam(m.groups(), apply['param']))
        return None

    @staticmethod
    def matchGroup(extract: tuple, group: list) -> bool:
        for i in range(len(group)):
            if i >= len(extract):
                return False
            if re.fullmatch(group[i], '' if extract[i] is None else extract[i]) is None:
                return False
        return True

    @staticmethod
    def matchParam(extract: tuple, param: list) -> tuple:
        args = list()
        pattern = re.compile(r'\[GROUP-([0-9]+)]')
        for arg in param:
            m = pattern.search(arg)
            if m is not None:
                group = extract[int(m.group(1)) - 1]
                args.append(arg.replace('[GROUP-{}]'.format(m.group(1)), '' if group is None else group))
            else:
                args.append(arg)
        return tuple(args)


if __name__ == '__main__':
    exit()
