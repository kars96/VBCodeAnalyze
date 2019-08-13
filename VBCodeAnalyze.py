import re
from sys import argv
from pathlib import Path
import os


def read_file(filename):
    file = open(filepath, 'r')
    return list(file.readlines())

def vb_rm_blklines_comments(content_arr):
    new_contents = []
    for line in content_arr:
        if re.search('^\s*$', line) or re.search("\s*'.*", line):
            #skip comment or blank line
            continue
        new_contents.append(line)
    
    return new_contents

def vb_code_count(content_arr):
    return len(content_arr)

def vb_func_sun_defs(content_arr):
    func_sub_arr = []
    for line in content_arr:
        sub_match_groups = re.search("Sub\s+(.*)", line)
        func_match_groups = re.search("Function\s+(.*)", line)

        if not re.match("\s*End", line) and (sub_match_groups != None or func_match_groups != None):
            func_sub_name = sub_match_groups[1] if sub_match_groups != None else func_match_groups[1]
            print(sub_match_groups, func_match_groups)
            func_sub_arr.append(func_sub_name)

    return func_sub_arr

def vb_func_sub_analyze(content_arr):
    inside_func = False
    line_count = 0
    for line in content_arr:
        if inside_func:
            
            sub_match_groups = re.match("\s*End\s+Sub", line)
            func_match_groups = re.match("\s*End\s+Function", line)
            
            if sub_match_groups != None or func_match_groups != None:
                yield [func_name, line_count]
                inside_func = False
                line_count =0
                continue
            
            line_count += 1

        sub_match_groups = re.search("Sub\s+(.*)", line)
        func_match_groups = re.search("Function\s+(.*)", line)
        if sub_match_groups != None or func_match_groups != None:
            
            func_name = sub_match_groups[1] if sub_match_groups != None else func_match_groups[1]
            inside_func = True
        

if __name__ == "__main__":
    projDir = argv[1] if len(argv)>1 else '.'
    for filename in Path(projDir).glob('**/*.vb'):
        filepath = os.path.join(os.path.abspath(projDir), filename)
        print(filepath)
        content_arr = read_file(filepath)
        content_wo_comments = vb_rm_blklines_comments(content_arr)
        total_lines = vb_code_count(content_wo_comments)
        fun_sub_arr = vb_func_sun_defs(content_wo_comments)
        print("Lines count " + str(total_lines))
        print("Functions count "+ str(len(fun_sub_arr)))
        for func_matrix in vb_func_sub_analyze(content_wo_comments):
            print(func_matrix)