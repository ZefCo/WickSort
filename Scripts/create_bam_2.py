import os
from pathlib import Path

# generate folder path
# generate bam files

# if os.path.isdir(destination_directory):
#     os.rename(original_path, destination_path)
# else:
#     Path(destination_directory).mkdir(parents=True, exist_ok=True)
#     os.rename(original_path, destination_path)

directory_path_root = r'/home/ethan/Documents/Wick/Files_Folder'
file_end = '.bam'

# interface = True
# while interface:
#     print("Directory Root is: " + directory_path_root)
#     directory_path_input = input("path to directory: ")
#     interface = False

creating = True
files_to_make = 2


def create_bams():
    for h in range(files_to_make):
        # index = str(i + 1)
        # file = []
        top_fol = 'Toh_Folder_%d' % (h+1)
        file = 'BAM_File_%d' % (h+1)
        # file.append('h_BAM_File_%d' % (i+1))
        bam_top_fold = os.path.join(directory_path_root, top_fol)
        bam_bot_fold = os.path.join(bam_top_fold, file)
        bam_file_path = os.path.join(
            bam_bot_fold, file + file_end)
        # print(bam_file_path)
        # bam_folder_path = os.path.join(directory_path_root, file)
        Path(bam_top_fold).mkdir(parents=True, exist_ok=True)
        Path(bam_bot_fold).mkdir(parents=True, exist_ok=True)
        # Path(bam_top_fold).mkdir(parents=True, exist_ok=True)
        # print(bam_file_path)
        # print(index + 1)
        file = open(bam_file_path, 'w+')
        file.close()
    for m in range(files_to_make):
        # index = str(i + 1)
        # file = []
        top_fol = 'Tom_Folder_%d' % (m+1)
        file = 'BAM_File_%d' % (m+1)
        # file.append('h_BAM_File_%d' % (i+1))
        bam_top_fold = os.path.join(directory_path_root, top_fol)
        bam_bot_fold = os.path.join(bam_top_fold, file)
        bam_file_path = os.path.join(
            bam_bot_fold, file + file_end)
        # print(bam_file_path)
        # bam_folder_path = os.path.join(directory_path_root, file)
        Path(bam_top_fold).mkdir(parents=True, exist_ok=True)
        Path(bam_bot_fold).mkdir(parents=True, exist_ok=True)
        # Path(bam_top_fold).mkdir(parents=True, exist_ok=True)
        # print(bam_file_path)
        # print(index + 1)
        file = open(bam_file_path, 'w+')
        file.close()


while creating:
    if os.path.isdir(directory_path_root):
        creating = False
        create_bams()
    else:
        Path(directory_path_root).mkdir(parents=True, exist_ok=True)
