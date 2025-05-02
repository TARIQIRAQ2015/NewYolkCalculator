import re

def fix_try_blocks(input_file, output_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all try blocks without corresponding except blocks
    pattern = r'try:(?![^\n]*?except)(?:(?!try:|except:|finally:).)*?(?=try:|except:|finally:|$)'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    # Fix each incomplete try block by adding an except clause
    fixed_content = content
    for match in matches:
        try_block = match.group(0)
        if "except" not in try_block.split("\n")[-1]:
            indentation = re.match(r'^(\s*)', try_block).group(1)
            fixed_try_block = try_block + f'\n{indentation}except Exception as e:\n{indentation}    st.error(f"An error occurred: {{e}}")'
            fixed_content = fixed_content.replace(try_block, fixed_try_block)
    
    # Write the fixed content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fixed file saved to {output_file}")

if __name__ == "__main__":
    fix_try_blocks("app.py", "app_fixed_syntax.py") 