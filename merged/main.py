import addbreak
from parse.nesting import analyse_files1
from parse.uncommon import analyze_files2


def main():
    print("\n testcase1 \n")
    testcase_file = "tests/testcase1.py"
    results = analyse_files1(testcase_file); print(results)

    if results:
        addbreak.modify_file(testcase_file, results)
    else:
        print("No code issues found.")

    print("\n testcase2 \n")
    testcase_file = ["tests/testcase2.py"]
    results = analyze_files2(testcase_file); print(results)
    if results:
        addbreak.modify_file(testcase_file, results)
    else:
        print("No code issues found.")

if __name__ == "__main__":
    main()
   
    
