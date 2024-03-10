import analyser
import addbreak

def main():
    testcase_file = "tests/testcase1.py"
    check1 = "parse/nesting.py"

    # Call analyser
    results = analyser.analyse_files(testcase_file, check1)
    
    # Call addbreak
    if results:
        addbreak.modify_file(testcase_file, results)
    else:
        print("No code issues found.")

if __name__ == "__main__":
    main()
