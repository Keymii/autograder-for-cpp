import subprocess
from file_handler import search_cpp_files, read_test_cases
from diff import find_and_print_differences, colorize_line
from ansi_colors import ERROR_COLOR, TEST_EVAL_COLOR
def run_test(input_str, expected_output, question_path):
    
    # Compile the C++ code
    compile_command = "s++ " + str(question_path)
    # print(compile_command)
    subprocess.run(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Run the compiled program with input
    run_command = f"./a.out"
    # If no output found, wait for 5 seconds before throwing a timeout and moving on. This ensures program moves on even if DUT is stuck in infinite loop
    timeout_sec=5

    try:
        process = subprocess.run(run_command, input=input_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout = timeout_sec)
        # Check if the output matches the expected output
        actual_output = process.stdout.strip()
        passFlag =  actual_output == expected_output.strip()
        if not passFlag:
            find_and_print_differences(actual_output,expected_output)
        return passFlag
    except subprocess.TimeoutExpired:
        print(colorize_line(f"Test case timed out after {timeout_sec} seconds.",ERROR_COLOR))
        return False

def autograde(path):
    input_test_cases = read_test_cases("./testbenchi.txt")
    output_test_cases = read_test_cases("./testbencho.txt")
    enumerated_test_cases = enumerate(zip(input_test_cases, output_test_cases), 1)
    for i, (input_str, expected_output) in enumerated_test_cases:
        try:
            print(colorize_line(f"\nEvaluating test case {i}\n",TEST_EVAL_COLOR))
            testSuccess = run_test(input_str, expected_output, path) 
        except Exception as e:
            testSuccess = False
            print(colorize_line("An error occured while evaluting the test case", ERROR_COLOR))
            print(e)
        if testSuccess:
            print(f"Test case {i}: Passed\n")
        else:
            print(f"Test case {i}: Failed\n")
        
if __name__ == "__main__":
    file_paths = search_cpp_files('../Day4_Thurs_9_Nov-20231110T172808Z-001', 'Q3b')
    for roll in file_paths:
        print("-"*100)
        path = file_paths[roll]
        message = f"\033[1m{roll}\033[22m: {path if path == 'absent' else 'present'}"
        print(message)
        if path !="absent":
            autograde(path)