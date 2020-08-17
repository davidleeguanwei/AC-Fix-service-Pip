import csv
import os
import re
import sys


log_filename_pattern = re.compile(r'Execution\d{14}-(\d+)\.log')
project_name_pattern = re.compile(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]\[INFO \] Project name: (.+)')
error_classification = re.compile(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]\[INFO \] Type:\t([.\d]+)')
fixing_scheme_result = re.compile(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]\[INFO \] Python Auto Fixing Scheme (succeed|failed) to fix project (.+)\.')
error_reason_comment = re.compile(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]\[ERROR\] (.+)')


error_reason_dict = {
	'Failed to pip install the project.': 1,
	'Failed to interpret the project.': 2,
	'Time limit exceeded.': 3,
	'No proper strategy can be applied, cannot be fixed.': 4,
	'Same classification as last one, strategy applied had no effect.': 5,
    "Cannot find source code of project's dependency.": 6,
	"Cannot fix SyntaxError due to file path not found.": 7,
	'Not recognized error log, cannot be fixed.': 9
}

log_list = sorted([file for file in os.listdir(sys.argv[1]) if log_filename_pattern.fullmatch(file) is not None])
record_list= [['index', 'name', 'result', 'reason', 'type']]

for log in log_list:
	index = log_filename_pattern.fullmatch(log).group(1)
	name = str()
	types = list()
	result = bool()
	reason = list()
	with open(os.path.join(sys.argv[1], log), 'r') as src:
		for line in src:
			if project_name_pattern.fullmatch(line.strip()) is not None:
				name = project_name_pattern.fullmatch(line.strip()).group(1)
			elif error_classification.fullmatch(line.strip()) is not None:
				types.append(error_classification.fullmatch(line.strip()).group(1))
			elif fixing_scheme_result.fullmatch(line.strip()) is not None:
				result = True if fixing_scheme_result.fullmatch(line.strip()).group(1) == 'succeed' else False
			elif error_reason_comment.fullmatch(line.strip()) is not None:
				reason.append(error_reason_dict.get(error_reason_comment.fullmatch(line.strip()).group(1), '0'))
	record_list.append([index, name, 1 if result else 0, '-' if len(reason) == 0 else reason[-1], '-' if len(types) == 0 else ' > '.join(types)])

with open(os.path.join(sys.argv[1], 'analysis.csv'), 'w') as dst:
	writer = csv.writer(dst)
	writer.writerows(record_list)
