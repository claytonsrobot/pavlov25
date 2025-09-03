from pavlov3d import filemanagement as fm
import os
print(f"os.getcwd() = {os.getcwd()}")
os.chdir("projects")
def create_directory_with_strucuture(option):
    # should copy existing files from stock library folder
    project_dir_name_str = str(input("Project directory name: "))
    if project_dir_name_str == "":
        project_dir_name_str = "test-20"
    else:
        pass
    fm.populate_new_project_dir(project_dir_name_str,option)
    
if __name__ == "__main__":
    option = str(input("Option (empty, sample): "))
    create_directory_with_strucuture(option)
