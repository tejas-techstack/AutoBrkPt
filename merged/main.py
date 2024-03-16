import addbreak
from parse.nesting import analyse_files1
from parse.uncommon import analyse_files2
from parse.argument_number_checker import analyse_files3

def main():
    testcase_file = "tests/testcase1.py"
    results = analyse_files1(testcase_file); 
    if results: addbreak.modify_file(testcase_file, results)

    testcase_file = ["tests/testcase2.py"]
    results = analyse_files2(testcase_file);
    if results: addbreak.modify_file(testcase_file, results)

    # testcase_file = ["tests/testcase3.py"]
    # results = analyse_files3(testcase_file); print(results)
    # if results: addbreak.modify_file(testcase_file, results)

import function_complexity

if __name__ == "__main__":
    main()
   