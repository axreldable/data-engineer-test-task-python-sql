def read_lines_from_file(file_path: str) -> list:
    """
    Utility method for reading lines from the file.

    :param file_path: a path to the file
    :return: file's lines
    """
    result_lines = []

    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            result_lines.append(line.strip())

        return result_lines
