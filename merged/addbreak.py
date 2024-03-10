import debugpy

def modify_file(testcase_file, results):
    with open(testcase_file, 'r+') as file:
        lines = file.readlines()

        modified = False
        for line_number, error_message in results:
            if "server.debugpy.breakpoint()" not in lines[line_number - 1]:
                # Add "server.debugpy.breakpoint()" with the error message as a comment
                lines[line_number - 1] += f"     server.debugpy.breakpoint()  # {error_message}\n"
                modified = True

        if modified:
            # Go to the beginning of the file to overwrite its contents
            file.seek(0)
            
            # Write modified lines to the file
            file.writelines(lines)
            
            # Truncate any remaining content after writing
            file.truncate()
            
            debugpy.listen(("localhost", 5678))
            print("Modifications completed.")
        else:
            print("No modifications needed.")
