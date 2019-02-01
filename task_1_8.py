import argparse
import re


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    print(args.file)

    regex = re.compile("struct [A-Za-z][A-Za-z0-9_]* [*][A-Za-z][A-Za-z0-9_]*")

    output_file = open("task_1_8_result.txt", "w+")

    with open(args.file, "r") as file:
        for line in file:
            matches = regex.findall(line)
            print(matches)
            if matches:
                for match in matches:
                    tokenized_match = match.split()
                    tokenized_match[1] = tokenized_match[1] + '_new'
                    tokenized_match[2] = tokenized_match[2] + '_new'
                    output_file.write(' '.join(tokenized_match) + "\n")
