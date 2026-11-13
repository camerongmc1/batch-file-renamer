from pathlib import Path

def main():
    while True:
        user_input = input("What is the file path to the folder? ")

        path = Path(user_input)

        if not path.exists():
            print("Path provided could not be found. Please provide correct path.")
        elif not path.is_dir():
            print("Path provided if a file, not a directory. Please provide a path to a directory.")
        else:
            break


    files = [file for file in path.iterdir() if file.is_file()]

    if not files:
        print("Directory provided contains no files.")


def add_prefix(files, prefix):
    new_files = []
    for file_path in files:
        new_file_path = file_path.parent / f"{prefix}{file_path.name}"
        new_files.append(new_file_path)

    return new_files


def add_suffix(files, suffix):
    new_files = []
    for file_path in files:
        stem = file_path.stem
        extension = file_path.suffix

        new_file_path = file_path.parent / f"{stem}{suffix}{extension}"
        new_files.append(new_file_path)

    return new_files


def replace_text(files, old_text, new_text):
    new_files = []
    for file_path in files:

        stem = file_path.stem
        extension = file_path.suffix

        new_stem = stem.replace(old_text, new_text)

        new_file_path = file_path.parent / f"{new_stem}{extension}"
        new_files.append(new_file_path)

    return new_files


def lowercase(files):
    new_files = []
    for file_path in files:
        new_file_path = file_path.parent / file_path.name.lower()
        new_files.append(new_file_path)

    return new_files


def uppercase(files):
    new_files = []
    for file_path in files:
        new_file_path = file_path.parent / file_path.name.upper()
        new_files.append(new_file_path)

    return new_files


def sequential_numbering(files, base, seperator, digits, start):
    new_files = []
    i = int(start)
    for file_path in sorted(files):
        new_file_path = file_path.parent / f"{base}{seperator}{i:0{int(digits)}}{file_path.suffix}"
        new_files.append(new_file_path)
        i += 1

    return new_files


if __name__ == '__main__':
    main()