from difflib import unified_diff

def colorize_line(line, color_code):
    return f"\033[{color_code}m{line}\033[0m"

def find_and_print_differences(actual_output, expected_output):
    lines_actual = actual_output.splitlines()
    lines_expected = expected_output.splitlines()

    max_len = max(len(lines_actual), len(lines_expected))
    
    print("Line   | Actual Output        | Expected Output")
    print("-------|----------------------|---------------------")

    for i, (line_actual, line_expected) in enumerate(zip(lines_actual + [''] * (max_len - len(lines_actual)), lines_expected + [''] * (max_len - len(lines_expected))), 1):
        if line_actual != line_expected:
            line_actual_colored = colorize_line(line_actual, '91')  # ANSI code for red text
            line_expected_colored = colorize_line(line_expected, '92')  # ANSI code for green text
            print(f"{i:<7}| {line_actual_colored.ljust(29)} | {line_expected_colored}")
        else:
            print(f"{i:<7}| {line_actual.ljust(20)} | {line_expected}")

if __name__=="__main__":
# Example usage:
    actual_output = """Line 1
Line 2
Line 3"""

    expected_output = """Line 1
Modified Line 2
Line 3"""

    find_and_print_differences(actual_output, expected_output)
