import argparse

from package.sqlpackageparser import SqlPackageParser
from mysqlrepository import MySqlRepository


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-p', '--path', required=True)

    args = parser.parse_args()
    package = SqlPackageParser.parse(args.path)
    for file in package.files:
        with open(file, 'r') as f:
            print(f'start execute sql at "{file}"')
            MySqlRepository.execute(package, f.read())
            print(f'execute sql at "{file}" successfully.')


if __name__ == "__main__":
    print('mfe started.')
    main()
    print('mfe completed')
