import addbreak
from parse.nesting import analyse_files1
from parse.uncommon import analyse_files2
from parse.argument_number_checker import analyse_files3

def main():
    testcase_file = "tests/testcase1.py"
    results = analyse_files1(testcase_file)
    if results: addbreak.modify_file(testcase_file, results)
    else: print("No code issues found.")

    testcase_file = ["tests/testcase2.py"]
    results = analyse_files2(testcase_file)
    if results: addbreak.modify_file(testcase_file, results)
    else: print("No code issues found.")


if __name__ == "__main__":
    main()
   