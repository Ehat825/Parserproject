import re
import argparse

# Add this at the beginning of your script
    
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

import re

def add_curly_braces(code):
    """Ensures that decision structures and loops have curly braces."""
    # Regex to match control structures without opening braces
    pattern = r'^( *)(if|else if|else|switch|while|do|for) *\([^\)]*\)\s*(?!\{)\s*$|^( *)do\s*$'
    
    def replace_block(match):
        indentation = match.group(1) or match.group(3)  # Get the correct indentation
        control_statement = match.group(0).strip()

        # Find the line immediately following the control statement
        following_lines = re.findall(r'^' + re.escape(indentation) + r' {4}[^\s].*$', code[match.end():], re.MULTILINE)
        if following_lines:
            # Capture the first statement following the control structure
            first_statement = following_lines[0]
            # Remove the original statement
            new_code_part = code[match.end():].replace(first_statement, '', 1).strip()

            # Create the block with the additional indentation and braces
            new_block = f"{control_statement} {{\n{first_statement}\n{indentation}}}"

            # Return the updated block without the duplicated unbracketed statement
            return f"{control_statement} {{\n{first_statement}\n{indentation}}}\n"
        return f"{control_statement} {{\n{indentation}}}\n"

    # Apply the replacement for all control structures (including 'do' loops)
    updated_code = re.sub(pattern, replace_block, code, flags=re.MULTILINE)

    # Handle 'else' statements separately since they can come without conditions
    else_pattern = r'^( *)(else)\s*(?!\{)\s*$'
    
    def replace_else(match):
        indentation = match.group(1)
        else_statement = match.group(0).strip()

        # Find the line immediately following the 'else' statement
        following_lines = re.findall(r'^' + re.escape(indentation) + r' {4}[^\s].*$', code[match.end():], re.MULTILINE)
        if following_lines:
            first_statement = following_lines[0]
            new_code_part = code[match.end():].replace(first_statement, '', 1).strip()
            new_block = f"{else_statement} {{\n{first_statement}\n{indentation}}}"
            return new_block + new_code_part
        return else_statement

    # Apply the replacement for 'else' blocks
    updated_code = re.sub(else_pattern, replace_else, updated_code, flags=re.MULTILINE)
    
    return updated_code


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
    updated_code = add_curly_braces(code_no_comments_strings)
    
    # Restore the comments and strings back into the updated code
    updated_code = restore_comments_and_strings(updated_code, placeholders)
    
    # Count the number of methods in the updated code
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

