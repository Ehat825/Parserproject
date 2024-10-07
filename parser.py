import re
import argparse

def read_java_file(file_path):
    """Reads a Java file and returns the content as a string."""
    with open(file_path, 'r') as file:
        return file.read()
def get_indentation(line):
    """Returns the indentation of a line."""
    return len(re.match(r'^\s*', line).group(0))
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

def line_by_line(Code):
    lines = Code.split("\n")
    updated_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        if re.search(r'(^\s*)(do)\s*$', line):
            level = get_indentation(line) + 4
            indent = " " * level
            line = line + " {"
            updated_lines.append(line)
            i += 1
            while i < len(lines):
                next_line = lines[i]
                nestLevel = get_indentation(next_line)
                if nestLevel < level:
                    updated_lines.append(indent + "}")
                    updated_lines.append(next_line)
                    break
                updated_lines.append(next_line)
                i += 1


        elif re.search(r'(^\s*)(if|else if|while|for|switch) *\([^\)]*\)\s*(?!\{)\s*$', line):
            level = get_indentation(line) + 4
            indent = " " * (level)
            line = line + " {"
            updated_lines.append(line)
            i += 1
            while i < len(lines):
                next_line = lines[i]
                nestLevel = get_indentation(next_line)
                if nestLevel <level or next_line.strip() == "":
                    updated_lines.append(indent + "}")
                    i -= 1 
                    break
                updated_lines.append(next_line)
                i += 1
        elif re.search(r'(^\s*)(else)\s*(?!\{)\s*$', line):
            level = get_indentation(line) +1
            indent = " " * (level)
            line = line + " {"
            updated_lines.append(line)
            i += 1
            while i < len(lines):
                next_line = lines[i]
                nestLevel = get_indentation(next_line)
                if nestLevel <level or next_line.strip() == "":
                    updated_lines.append(indent + "}")
                    break

                updated_lines.append(next_line)
                i += 1
        else:
            updated_lines.append(line)
        i += 1

    return "\n".join(updated_lines)



def count_methods(code):
    """Counts the number of methods in the Java code."""
    method_pattern = r'\b(public|private|protected|static|\s)*[\w\<\>\[\]]+\s+[\w]+ *\([^)]*\) *\{'
    methods = re.findall(method_pattern, code)
    return len(methods)

def fix_java_code(file_path):
    """Fixes the input Java code and generates a new file with the results."""
    original_code = read_java_file(file_path)
    # Remove comments and strings
    code_no_comments_strings, placeholders = remove_comments_and_strings(original_code)
    
    # Add curly braces where missing in decision structures and loops
    updated_code = line_by_line(code_no_comments_strings)
    
    # Restore the comments and strings back into the updated code
    updated_code = restore_comments_and_strings(updated_code, placeholders)
    
     #Count the number of methods in the updated code
    method_count = count_methods(updated_code)
    # Write the output file
    output_file_path = 'java_program_output.txt'
    write_output_file(output_file_path, original_code, updated_code, method_count)
    
    print(f"Processed file saved as {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fix Java code by adding curly braces and counting methods.')
    parser.add_argument('file_path', type=str, help='Path to the input Java file')
    args = parser.parse_args()
    
    fix_java_code(args.file_path)
