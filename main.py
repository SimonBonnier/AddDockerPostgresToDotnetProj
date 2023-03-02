import sys
import os
import shutil

connection_string_section = """
"ConnectionStrings": {
    "PlayTogetherDB": "Host=localhost;Database=playtogetherdb;Username=postgres;Password=postgres;Port=50000"
  },
"""

def run(args: list[str]):
    project_path = args[0]
    try:
        framework = args[1]
    except:
        framework = 'net6.0'

    project_name = get_sln_file_name(project_path=project_path)

    current_path = os.path.dirname(os.path.abspath(__file__))
    print(current_path)

    setup_database_project(current_path=current_path, project_path=project_path, project_name=project_name, framework=framework)

    # TODO: Update README.MD

def get_sln_file_name(project_path: str):
    files = os.listdir(project_path)
    for f in files:
        if f.endswith(".sln"):
            return f.replace(".sln", "")    
    raise Exception("No sln file found")

def setup_database_project(current_path: str, project_path: str, project_name: str, framework: str):
    os.chdir(project_path)
    
    database_project_name: str = f'{project_name}.Database'
    os.system(f'dotnet new console --framework "{framework}" -o {database_project_name}')
    
    database_proj_path: str = os.path.join(project_path, database_project_name)
    os.system(f"dotnet sln add {database_proj_path}")
    
    os.chdir(database_proj_path)
    os.system("dotnet add package dbup-postgresql")
    
    os.chdir(project_path)

    default_class_path = os.path.join(database_proj_path, "Program.cs")
    os.remove(default_class_path)

    template_folder = os.path.join(current_path, "templates")
    add_template_files(database_proj_path=database_proj_path, project_path=project_path, template_folder=template_folder)
    try_append_section_to_readme(project_path=project_path, template_folder=template_folder)

    replace_placeholders_in_template_files(project_path=project_path, project_name=project_name)

def add_template_files(database_proj_path: str, project_path: str, template_folder: str):
    for file_name in os.listdir(template_folder):
        if file_name == "readme.txt":
            continue
        source = os.path.join(template_folder, file_name)
        
        if file_name != "Program.cs":
            destination = os.path.join(project_path, file_name)
        else:
            destination = os.path.join(database_proj_path, file_name)

        if os.path.isfile(source):
            shutil.copy(source, destination)

def replace_placeholders_in_template_files(project_path: str, project_name: str):
    replace_in_file(os.path.join(project_path, "rebuild-db.ps1"), "{PROJECT_NAME_LOWER_CASE}", project_name.lower())
    replace_in_file(os.path.join(project_path, "rebuild-db.ps1"), "{PROJECT_NAME}", project_name)
    replace_in_file(os.path.join(project_path, "update-db.ps1"), "{PROJECT_NAME_LOWER_CASE}", project_name.lower())
    replace_in_file(os.path.join(project_path, "update-db.ps1"), "{PROJECT_NAME}", project_name)

def replace_in_file(file_path: str, to_replace: str, replace_with: str):
    with open(file_path, 'r') as file :
        filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(to_replace, replace_with)

        # Write the file out again
        with open(file_path, 'w') as file:
            file.write(filedata)

def try_append_section_to_readme(project_path: str, template_folder: str):
    project_files = os.listdir(project_path)
    readme_file = [f for f in project_files if f.lower() == "readme.md"]
    if len(readme_file) > 0:
        template_text = ""
        with open(os.path.join(template_folder, 'readme.txt')) as template_file:
            template_text = template_file.read()
        with open(readme_file[0], 'a') as file:
            file.write(f"\n{template_text}")

if __name__ == '__main__':
    if len(sys.argv[1:]) < 1:
        print('need to provide project path')

    run(sys.argv[1:])

# Test path: C:\Users\Simon\source\python\add-docker-postgresdb-support-for-dotnet-project\Test