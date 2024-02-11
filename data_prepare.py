import os
import shutil

def copy_html_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file == "html.txt":
                source_path = os.path.join(root, file)
                folder_name = os.path.basename(root)
                destination_file = os.path.join(destination_folder, folder_name+"_html.txt")
                shutil.copy(source_path, destination_file)

#in here to prepare data you have to export zip files in the same folder with data_prepare
source_folder = "phish_sample_30k"
destination_folder = "Phishing"
copy_html_files(source_folder, destination_folder)
source_folder = "benign_25k"
destination_folder = "Legitimate"
copy_html_files(source_folder, destination_folder)
source_folder="misleading"
copy_html_files(source_folder, destination_folder)