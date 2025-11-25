import re
import ast
import json
from llm.groq_client import client
from config.settings import MODEL_CODE

def validate_python_code(code: str) -> tuple[bool, str]:
    try:
        ast.parse(code)
        return True, "Valid"
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} at line {e.lineno}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def is_json_response(text: str) -> bool:
    """Check if the response is JSON instead of code."""
    text = text.strip()
    if text.startswith('{') or text.startswith('test_case'):
        try:
            json.loads(text)
            return True
        except:
            pass
    return False

def generate_selenium_script(test_case_json, html_content="", rag_context="", max_retries=3):
    prompt_base = f"""
You are a Senior Python Selenium Expert. Your task is to generate a robust, production-ready Selenium WebDriver script.

### INPUT DATA
<html_content>
{html_content[:4000]}... (truncated if too long)
</html_content>

<documentation>
{rag_context}
</documentation>

<test_case>
{test_case_json}
</test_case>

### STRICT REQUIREMENTS
1. **Imports**: Import `selenium`, `webdriver_manager`, `pytest` (if needed), and standard libraries.
2. **Setup**: Use `ChromeDriverManager` to install and setup the Chrome driver.
3. **Logic**: Implement ALL steps defined in the `<test_case>`.
4. **Selectors**: Analyze the `<html_content>` to find the MOST RELIABLE selectors (ID > Name > CSS Class > XPath).
5. **Waits**: NEVER use `time.sleep()`. Use `WebDriverWait` with `expected_conditions` for all interactions.
6. **Assertions**: Include `assert` statements to verify the `expected_result`.
7. **Cleanup**: Use a `try-finally` block to ensure `driver.quit()` is always called.
8. **Output**: Return ONLY valid Python code. No Markdown, no backticks, no explanations.

### CODING GUIDELINES
- **Think Step-by-Step**: Before writing the code, plan the selectors and logic in comments.
- **Error Handling**: Handle potential `TimeoutException` or `NoSuchElementException` gracefully if needed.
- **Local File Handling**: If the URL is not provided, assume the file is at `file:///path/to/checkout.html` but allow it to be easily changed.

### EXPECTED OUTPUT FORMAT
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Plan:
# 1. Setup Chrome Driver
# 2. Navigate to page
# 3. [Step 1] ...
# 4. [Step 2] ...

def run_test():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        # ... implementation ...
        pass
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
```
"""

    for attempt in range(max_retries):
        print(f"\\n Attempt {attempt + 1}/{max_retries}")
        
        response = client.chat.completions.create(
            model=MODEL_CODE,
            messages=[{"role": "user", "content": prompt_base}],
            temperature=0.1, # Lower temperature for more deterministic code
            max_completion_tokens=2048
        )
        
        raw_content = response.choices[0].message.content
        
        # Clean response
        clean_content = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()
        clean_content = clean_content.replace("```python", "").replace("```", "").strip()
        
        # Check if response is JSON instead of code
        if is_json_response(clean_content):
            print(" LLM returned JSON instead of code. Retrying with stricter prompt...")
            prompt_base = f"""
CRITICAL ERROR: You returned JSON. I need PYTHON CODE.

<task>
Generate a Selenium Python script for this test case.
</task>

<test_case>
{test_case_json}
</test_case>

<requirements>
- Output ONLY Python code.
- Start with imports.
- NO JSON.
</requirements>
"""
            continue
        
        is_valid, error_msg = validate_python_code(clean_content)
        
        if is_valid:
            print("Code validation passed!")
            return clean_content
        else:
            print(f"Validation failed: {error_msg}")
            if attempt < max_retries - 1:
                prompt_base = f"""
The previous code had a syntax error:
<error>
{error_msg}
</error>

Please fix the code for this test case:
<test_case>
{test_case_json}
</test_case>

Return ONLY the fixed Python code.
"""
    
    print("Max retries reached.Try a better prompt or check test details.")
    return clean_content
