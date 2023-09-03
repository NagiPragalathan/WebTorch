import os, re, json, ast
import importlib.metadata as metadata

def get_imported_modules(file_path):
    """
    Retrieves a set of imported modules from a given Python source file.

    This function reads the content of the provided Python source file, parses it using the 'ast' module,
    and extracts imported modules using the 'Import' and 'ImportFrom' nodes. It returns a set containing
    the names of imported modules.

    Args:
        file_path (str): The path to the Python source file.

    Returns:
        set: A set containing the names of imported modules.
    """
    with open(file_path, "r") as file:
        content = file.read()

    # Parse the Python source code
    tree = ast.parse(content)

    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if node.module:
                    imported_modules.add(f"{node.module}.{alias.name}")
                else:
                    imported_modules.add(alias.name)

    return imported_modules

def find_imported_modules(root_dir):
    """
    Finds and returns a list of imported modules across Python files within a directory.

    This function recursively traverses through the provided root directory, identifying all
    Python files (with the ".py" extension) and extracting imported modules using the
    'get_imported_modules()' function. The resulting list contains the names of all imported
    modules found in the specified directory.

    Args:
        root_dir (str): The root directory to search for Python files.

    Returns:
        list: A list of imported module names across the Python files within the directory.
    """
    out = []
    imported_modules = set()
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                imported_modules.update(get_imported_modules(file_path))
    for module in imported_modules:
        out.append(module)
    return out
        
def get_modules_version(module_datas):        
    """
    Retrieves version information for a list of modules.

    This function takes a list of module data, where each data item is in the form of
    'module_name.submodule'. It uses the 'importlib.metadata' module to fetch the version
    information of each module and creates a dictionary with module names as keys and
    corresponding version numbers as values.

    Args:
        module_datas (list): A list of module data in the format 'module_name.submodule'.

    Returns:
        dict: A dictionary containing module names as keys and their version numbers as values.
    """
    module_versions = {}
    for name in module_datas:
        module_name = name.split(".")[0]
        try:
            # Use importlib.metadata to get the version information
            version = metadata.version(module_name)
            module_versions[module_name] = version
        except metadata.PackageNotFoundError:
            pass
    return module_versions

def shortcut_version(root_dir):
    """
    Retrieves version information for imported modules within a directory.

    This function combines the functionality of 'find_imported_modules()' and 'get_modules_version()'
    to quickly retrieve version information for all imported modules within a specified directory.

    Args:
        root_dir (str): The root directory to search for imported modules.

    Returns:
        dict: A dictionary containing module names as keys and their version numbers as values.
    """
    imported_modules = find_imported_modules(root_dir)
    versions = get_modules_version(imported_modules)
    return versions

def create_req(path):
    with open(os.path.join(os.getcwd(),'requirements.txt'), 'w') as file:
        for package, version in shortcut_version(path).items():
            file.write(f"{package}=={version}\n")
            
            
import os
import black

def format_python_file(input_file_path):
    """
    Format a Python file using the Black code formatter.

    Args:
        input_file_path (str): The path to the Python file to be formatted.

    Returns:
        str: The formatted Python code.
    """
    try:
        with open(input_file_path, "r") as file:
            input_code = file.read()
        formatted_code = black.format_str(input_code, mode=black.FileMode())
        return formatted_code
    except Exception as e:
        return str(e)

def format_all_python_files_in_directory(directory_path, output_directory=None):
    """
    Format all Python files in a directory using the Black code formatter.

    Args:
        directory_path (str): The path to the directory containing Python files.
        output_directory (str, optional): The path to the output directory to store formatted files.
            If None, the original files will be overwritten. Defaults to None.

    Returns:
        None
    """
    if not output_directory:
        output_directory = os.getcwd()
    if output_directory and not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory_path):
        if filename.endswith(".py"):
            input_file_path = os.path.join(directory_path, filename)
            formatted_code = format_python_file(input_file_path)

            if output_directory:
                output_file_path = os.path.join(output_directory, filename)
                with open(output_file_path, "w") as file:
                    file.write(formatted_code)
            else:
                with open(input_file_path, "w") as file:
                    file.write(formatted_code)