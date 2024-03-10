# import analyser
import addbreak
from parse.nesting import analyse_files

def main():
    testcase_file = "tests/testcase1.py"
    results = analyse_files(testcase_file)
    print(results)    
    if results:
        addbreak.modify_file(testcase_file, results)
    else:
        print("No code issues found.")

if __name__ == "__main__":
    main()
