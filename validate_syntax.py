import py_compile
import sys

def validate_syntax(file_path):
    try:
        py_compile.compile(file_path, doraise=True)
        print(f"✅ {file_path} has valid syntax")
        return True
    except py_compile.PyCompileError as e:
        print(f"❌ Syntax error in {file_path}:")
        print(f"   Line {e.lineno}: {e.msg}")
        return False

if __name__ == "__main__":
    validate_syntax("app.py") 