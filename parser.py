import re

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

def add_curly_braces(code):
    """Ensures that decision structures and loops have curly braces."""
    # Add curly braces to single-line if, else-if, else, for, while, and do-while blocks
    patterns = [
        r'(?<!\})\s*if\s*\(.*?\)\s*[^{;]\s*.*\n',  # if without braces
        r'(?<!\})\s*else\s*if\s*\(.*?\)\s*[^{;]\s*.*\n',  # else-if without braces
        r'(?<!\})\s*else\s*[^{;]\s*.*\n',  # else without braces
        r'(?<!\})\s*for\s*\(.*?\)\s*[^{;]\s*.*\n',  # for without braces
        r'(?<!\})\s*while\s*\(.*?\)\s*[^{;]\s*.*\n',  # while without braces
        r'(?<!\})\s*do\s*[^{;]\s*.*\n',  # do without braces
    ]
    
    # For each pattern, add the missing curly braces
    for pattern in patterns:
        matches = re.findall(pattern, code)
        for match in matches:
            # Add braces around the block
            fixed_block = re.sub(r'(.*\))\s*(.*)', r'\1 {\n\2\n}', match)
            code = code.replace(match, fixed_block)
    
    return code

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

# Example usage
file_path = 'input_program.java'
fix_java_code(file_path)