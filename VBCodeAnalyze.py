import re
from sys import argv
from pathlib import Path
import os

def vb_analyze(filepath):
    print('Code matrix of ' + filepath)
    file = open(filepath, 'r')
    inside_func = False
    line_count = 0
    for line in file.readlines():
        if re.search('^\s*$', line) or re.search("\s*'.*", line):
            #skip comment or blank line
            continue
        if inside_func:
            line_count += 1

        sub_match_groups = re.search("End\s+Sub", line)
        func_match_groups = re.search("End\s+Function", line)
        
        if sub_match_groups != None or func_match_groups != None:
            yield [func_name, line_count]
            inside_func = False
            line_count =0
            continue

        sub_match_groups = re.search("Sub\s+(.*)", line)
        func_match_groups = re.search("Function\s+(.*)", line)
        if sub_match_groups != None or func_match_groups != None:
            
            func_name = sub_match_groups[1] if sub_match_groups != None else func_match_groups[1]
            inside_func = True
        

if __name__ == "__main__":
    projDir = argv[1]
    for filename in Path(projDir).glob('**/*.vb'):
        filepath = os.path.join(os.path.abspath(projDir), filename)
        print(filepath)
        for func_matrix in vb_analyze(filepath):
            print(func_matrix)