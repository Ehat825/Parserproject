import re
import argparse

def read_java_file(file_path):
    """Reads a Java file and returns the content as a string."""
    with open(file_path, 'r') as file:
        return file.read()

def write_output_file(output_path, original_code, updated_code, method_count):
    """Writes the output text file with the original and updated code and method count."""
    with open(output_path, 'w') as file:
        file.write("Original Java Program:\n")
        file.write(original_code)
        file.write("\n\nUpdated Java Program:\n")
        file.write(updated_code)
        file.write(f"\n\nNumber of methods: {method_count}\n")

def remove_comments_and_strings(code):
    """Removes comments and strings from the code to ensure they are not modified."""
    # Regex patterns for strings, single-line comments, and multi-line comments
    string_pattern = r'\"(\\.|[^"\\])*\"'  # matches strings like "abc" or escaped quotes
    single_line_comment_pattern = r'//.*'  # matches single-line comments
    multi_line_comment_pattern = r'/\*[\s\S]*?\*/'  # matches multi-line comments

    # Replace strings and comments with placeholders
    placeholders = []
    
    def replace_with_placeholder(match):
        """Replace matched strings and comments with a unique placeholder."""
        placeholders.append(match.group(0))
        return f"PLACEHOLDER_{len(placeholders) - 1}"

    # Replace strings and comments with placeholders
    code_no_comments_strings = re.sub(string_pattern, replace_with_placeholder, code)
    code_no_comments_strings = re.sub(single_line_comment_pattern, replace_with_placeholder, code_no_comments_strings)
    code_no_comments_strings = re.sub(multi_line_comment_pattern, replace_with_placeholder, code_no_comments_strings)

    return code_no_comments_strings, placeholders

def restore_comments_and_strings(code, placeholders):
    """Restores the original strings and comments into the code."""
    for i, placeholder in enumerate(placeholders):
        code = code.replace(f"PLACEHOLDER_{i}", placeholder)
    return code

def identify_control_structures(code):
    pattern_with_condition = r'''(^\s*)(if|else if|switch|while|for) *\([^\)]*\)\s*(?!\{)\s*\n(?:\1\s{4}.*\n)*'''
    pattern_without_condition = r'''(^\s*)(else|do)\s*(?!\{)\s*\n(?:\1\s{4}.*\n)*'''
    matches_with_condition = re.finditer(pattern_with_condition, code, re.MULTILINE)
    matches_without_condition = re.finditer(pattern_without_condition, code, re.MULTILINE)
    
    control_structures = []
    for match in matches_with_condition:
        control_structures.append(match.group(0))
    for match in matches_without_condition:
        control_structures.append(match.group(0))
    print (control_structures)
    return control_structures
def add_curly_braces(code):
    code = find_control_structures(code)
    
    # This will need to do a bit of recursion, we will use identify_control structures, and then add curly braces around each code block
    # Then, we will strip the first line of our control strucure, and call add_curly braces on the code stripped of the initial match to find nested statements.
    #     
def count_methods(code):
    """Counts the number of methods in the Java code."""
    method_pattern = r'\b(public|private|protected|static|\s)*[\w\<\>\[\]]+\s+[\w]+ *\([^)]*\) *\{'
    methods = re.findall(method_pattern, code)
    return len(methods)

def fix_java_code(file_path):
    """Fixes the input Java code and generates a new file with the results."""
    original_code = read_java_file(file_path)
    identify_control_structures(original_code)
    # Remove comments and strings
    #code_no_comments_strings, placeholders = remove_comments_and_strings(original_code)
    
    # Add curly braces where missing in decision structures and loops
   #updated_code = add_curly_braces(code_no_comments_strings)
    
    # Restore the comments and strings back into the updated code
    #updated_code = restore_comments_and_strings(updated_code, placeholders)
    
    # Count the number of methods in the updated code
    #method_count = count_methods(updated_code)
    
    # Write the output file
    #output_file_path = 'java_program_output.txt'
    #write_output_file(output_file_path, original_code, updated_code, method_count)
    
    #print(f"Processed file saved as {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fix Java code by adding curly braces and counting methods.')
    parser.add_argument('file_path', type=str, help='Path to the input Java file')
    args = parser.parse_args()
    
    fix_java_code(args.file_path)