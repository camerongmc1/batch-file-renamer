from pathlib import Path
import tempfile


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


    files = sorted([file for file in path.iterdir() if file.is_file()])

    if not files:
        print("Directory provided contains no files.")
        return

    while True:
        operations = select_operations()

        if not operations:
            return

        file_changes = apply_operations(files, operations)

        duplicate_paths = find_duplicate_paths(file_changes)
        existing_path_conflicts = find_existing_path_conflicts(file_changes)

        if duplicate_paths or existing_path_conflicts:
            if duplicate_paths:
                print("The following filenames have duplicates:")
                for path in duplicate_paths:
                    print(path.name)
           
            if existing_path_conflicts:
                print("The following filenames already exist and will cause a conflict:")
                for path in existing_path_conflicts:
                    print(path.name)

            try_again = ask_retry()
            if not try_again:
                return
        else:
            confirmation = preview_changes(file_changes)
            if not confirmation:
                continue
            else:
                break

    rename_files(file_changes)


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
    for file_path in files:
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
    original_files = files.copy()

    for operation in operations:
        function = operation[0]
        parameters = operation[1:]

        files = function(files, *parameters)

    file_changes = list(zip(original_files, files))

    return file_changes


def find_duplicate_paths(file_changes):
    proposed_paths = set()
    duplicate_paths = []

    for file_change in file_changes:
        if file_change[1] not in proposed_paths:
            proposed_paths.add(file_change[1])
        else:
            if file_change[1] not in duplicate_paths:
                duplicate_paths.append(file_change[1])

    return duplicate_paths


def find_existing_path_conflicts(file_changes):
    original_paths = {original for original, proposed in file_changes}
    conflicts = []

    for file_change in file_changes:
        proposed_path = file_change[1]

        if proposed_path.exists() and proposed_path != file_change[0]:

            if proposed_path not in original_paths:
                if proposed_path not in conflicts:
                    conflicts.append(proposed_path)

            else:
                for other_change in file_changes:
                    if other_change[0] == proposed_path:
                        if other_change[0] == other_change[1]:
                            if proposed_path not in conflicts:
                                conflicts.append(proposed_path)

    return conflicts


def ask_retry():
    while True:
        try_again = input("Would you like to try a different set of operations? (y/n): ").strip().lower()
        if try_again in ("y", "yes"):
            return True
        elif try_again in ("n", "no"):
            return False
        else:
            print("Please enter valid response (yes or no)")


def preview_changes(file_changes):
    print(f"{'Original filename':<30}", end="")
    print(f"New filename")
    print("-" * 60)
    for file_change in file_changes:
        print(f"{file_change[0].name:<30}", end="")
        print(f"{file_change[1].name}")
    while True:
        confirmation = input("Would you like to carry on with these changes? (y/n): ").strip().lower()
        if confirmation in ("y", "yes"):
            return True
        elif confirmation in ("n", "no"):
            return False
        else:
            print("Please enter a valid input (yes or no)")


def rename_files(file_changes):    
    changing_files = [file_change for file_change in file_changes if file_change[0] != file_change[1]]

    if not changing_files:
        print("No files to change.")
        return

    temp_dir_path = Path(tempfile.mkdtemp(dir=changing_files[0][0].parent))

    new_paths = []
    for original, proposed in changing_files:
        temp_file_path = temp_dir_path / original.name
        original.rename(temp_file_path)

        new_paths.append((temp_file_path, proposed))

    for temp_path, proposed in new_paths:
        temp_path.rename(proposed)

    temp_dir_path.rmdir()
    
    print("Files renamed successfully.")


if __name__ == '__main__':
    main()