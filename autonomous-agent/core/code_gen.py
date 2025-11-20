import re
import ast
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

def generate_selenium_script(test_case_json, max_retries=3):
    prompt_base = f"""
You are a Python Selenium Expert.
Generate a COMPLETE, EXECUTABLE Selenium script for this test case.

TEST CASE:
{test_case_json}

REQUIREMENTS:
- Use webdriver_manager for ChromeDriver
- Include all necessary imports
- Add proper error handling
- Use explicit waits (WebDriverWait)
- Add comments explaining each step
- Close the driver at the end

Return ONLY executable Python code, no markdown formatting.
"""

    for attempt in range(max_retries):
        print(f"\n🔄 Attempt {attempt + 1}/{max_retries}")
        
        response = client.chat.completions.create(
            model=MODEL_CODE,
            messages=[{"role": "user", "content": prompt_base}],
            temperature=0.2,
            max_completion_tokens=2048
        )
        
        raw_content = response.choices[0].message.content
        
        # Clean response
        clean_content = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL).strip()
        clean_content = clean_content.replace("```python", "").replace("```", "").strip()
        
        is_valid, error_msg = validate_python_code(clean_content)
        
        if is_valid:
            print("✅ Code validation passed!")
            return clean_content
        else:
            print(f"❌ Validation failed: {error_msg}")
            if attempt < max_retries - 1:
                prompt_base = f"""
The previous code had this error:
{error_msg}
Please fix it.
TEST CASE:
{test_case_json}
Return ONLY executable Python code.
"""
    
    print("⚠️ Max retries reached.")
    return clean_content
