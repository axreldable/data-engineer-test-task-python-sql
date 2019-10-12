def read_file(file_path: str):
    with open(file_path) as file:
        return file.read().strip()
