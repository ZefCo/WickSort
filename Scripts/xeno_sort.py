#!/usr/bin/env python3

import os
import re
from pathlib import Path
import csv

directory_root = Path(__file__).parent.absolute()
print(directory_root)
end_file = r'.bam'
csv_file = r'samplelist.csv'
sh_file = r'test.sh'
r_file = r'script.r'
human = r'(h|human)'
mouse = r'(m|mouse)'
filtered = 'Filtered_'
yes = r'(y|yes|ye|ys)'
no = r'(n|no)'
exit = r'(e|exit)'
setwd = r'/project/phgunaratne/\[working_directory\]'
filt_file_fold = r'\[filtered_file_folder\]'

print('''
This program assumes you know which file is for a human and which is for a
mouse. Please exit the program and determine which is which before proceeding.

Press e or type exit at anytime to exit
''')


def copy_file(old_path, new_dir, command='cp '):
    old_split = os.path.split(old_path)
    file_name = old_split[1]
    new_path = os.path.join(new_dir, file_name)
    if not os.path.isfile(new_path):
        syscom = command + old_path + ' ' + new_path
        os.system(syscom)
    return new_path


def creat_filterfolder(path, name):
    d_fold = os.path.dirname(path)
    filtered_folder = filtered + name
    f_fold = os.path.join(d_fold, filtered_folder)
    if not os.path.isdir(f_fold):
        Path(f_fold).mkdir(parents=True, exist_ok=True)
    return filtered_folder


def directory_walk(d_start):
    bam_dict = {}
    i = 0
    for root, dirs, files in os.walk(d_start):
        for name in files:
            if name.endswith(end_file):
                index = str(i)
                path = os.path.join(root, name)
                bam_dict[index] = {}
                bam_dict[index]['name'] = name
                bam_dict[index]['gene'] = False
                bam_dict[index]['path'] = path
                i += 1
            if re.match(csv_file, name):
                csv_main = os.path.join(root, name)
            if re.match(sh_file, name):
                sh_main = os.path.join(root, name)
            if re.match(r_file, name):
                r_main = os.path.join(root, name)
    return bam_dict, csv_main, sh_main, r_main


def double_check(subject, gene):
    print("\nIs this correct?")
    print('File Path: ' + subject)
    print('Genome: ' + gene)
    input_correct = input("y/n/e? ")
    exit_check(input_correct)
    if re.match(yes, input_correct, re.IGNORECASE):
        return True
    elif re.match(no, input_correct, re.IGNORECASE):
        return False


def exit_check(input):
    if re.match(exit, input, re.IGNORECASE):
        quit()


def folder_createnmove(**kwargs):
    for index in kwargs.keys():
        src = kwargs[index]['path']
        name = kwargs[index]['name']
        gene = kwargs[index]['gene']
        new_name = gene + name
        des_dir = os.path.join(directory_root, kwargs[index]['name'])
        des = os.path.join(des_dir, new_name)
        if not os.path.isdir(des_dir):
            Path(des_dir).mkdir(parents=True, exist_ok=True)
        os.rename(src, des)
        kwargs[index]['path'] = des
        f_path = creat_filterfolder(des, name)
        kwargs[index]['name'] = gene + name
        kwargs[index]['filtered'] = f_path


def human_v_mouse(*args, **kwargs):
    for index in kwargs:
        path = kwargs[index]['path']
        running = True
        while running:
            genome = set_gene(path)
            passed = double_check(path, genome)
            if passed:
                kwargs[index]['gene'] = genome
                running = False


def move_scirpts(**kwargs):
    for index in kwargs.keys():
        dir_name = os.path.split(kwargs[index]['path'])
        copy_file(sh_main, dir_name[0])
        new_csv_file = copy_file(csv_main, dir_name[0])
        if re.match(human, kwargs[index]['gene'], re.IGNORECASE):
            loc = (0, 0)
        elif re.match(mouse, kwargs[index]['gene'], re.IGNORECASE):
            loc = (0, 1)
        read_samplelist_csv(new_csv_file, kwargs[index]['path'], loc)
        read_script_r(r_main, dir_name[0], kwargs[index]['filtered'])


def print_check(thing):
    print(thing)
    print(type(thing))


def read_samplelist_csv(csv_path, append_message, location):
    file_read = csv.reader(open(csv_path))
    csv_list = list(file_read)
    csv_list[location[0]][location[1]] = append_message
    file_write = csv.writer(open(csv_path, 'w'))
    file_write.writerows(csv_list)


def read_script_r(r_path, des, f_fold):
    r_split = os.path.split(r_path)
    fin = open(r_path, 'r')
    fout = open(os.path.join(des, r_split[1]), 'w')
    for line in fin:
        if re.search(setwd, line):
            line = re.sub(setwd, des, line)
        if re.search(filt_file_fold, line):
            line = re.sub(filt_file_fold, f_fold, line)
        fout.write(line)


def read_test_sh():
    pass


def set_gene(subject):
    input_gene = input("\n[h]uman or [m]ouse?\n" + subject + '\n:')
    exit_check(input_gene)
    if re.match(human, input_gene, re.IGNORECASE):
        return 'Human'
    elif re.match(mouse, input_gene, re.IGNORECASE):
        return 'Mouse'


if __name__ in '__main__':
    core_files = directory_walk(directory_root)
    bam_main = core_files[0]
    csv_main = core_files[1]
    sh_main = core_files[2]
    r_main = core_files[3]
    human_v_mouse(**bam_main)
    folder_createnmove(**bam_main)
    move_scirpts(**bam_main)
