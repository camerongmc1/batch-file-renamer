from pathlib import Path

def main():
    while True:
        user_input = input("What is the file path to the folder? ")

        path = Path(user_input)

        if not path.exists():
            print("Path provided could not be found. Please provide correct path.")
        elif not path.is_dir():
            print("Path provided is a file, not a directory. Please provide a path to a directory.")
        else:
            break


    files = [file for file in path.iterdir() if file.is_file()]

    if not files:
        print("Directory provided contains no files.")
        return

    operations = select_operations()

    new_files = apply_operations(files, operations)

    for file_path in new_files:
        print(file_path.name)


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


def sequential_numbering(files, base, separator, digits, start):
    new_files = []
    i = int(start)
    for file_path in sorted(files):
        new_file_path = file_path.parent / f"{base}{separator}{i:0{int(digits)}}{file_path.suffix}"
        new_files.append(new_file_path)
        i += 1

    return new_files


def select_operations():
    operations = []
    while True:
        print("Please select which operation you would like to apply to the filenames:")
        print("1. Add prefix")
        print("2. Add suffix")
        print("3. Replace text")
        print("4. Convert to lowercase")
        print("5. Convert to uppercase")
        print("6. Sequential numbering")
        print("0. Finish selecting operations")

        user_input = input("Select an operation (eg. 1): ")

        if user_input == "0":
            break
        elif user_input == "1":
            prefix = input("Provide prefix: ")
            operations.append((add_prefix, prefix))
        elif user_input == "2":
            suffix = input("Provide suffix: ")
            operations.append((add_suffix, suffix))
        elif user_input == "3":
            old_text = input("Provide text to replace: ")
            new_text = input("Provide text that will replace the old text: ")
            operations.append((replace_text, old_text, new_text))
        elif user_input == "4":
            operations.append((lowercase,))
        elif user_input == "5":
            operations.append((uppercase,))
        elif user_input == "6":
            base = input("Provide base text: ")
            separator = input("Provide separator: ")
            digits = input("Provide number of digits for numbering: ")
            start = input("Provide starting number for sequence: ")
            operations.append((sequential_numbering, base, separator, digits, start))
        else:
            print("Please provide a valid selection (eg. 1, 2, 3, 4, 5, 6, or 0 if you are finished)")

    return operations


def apply_operations(files, operations):
    for operation in operations:
        function = operation[0]
        parameters = operation[1:]

        files = function(files, *parameters)

    return files


if __name__ == '__main__':
    main()