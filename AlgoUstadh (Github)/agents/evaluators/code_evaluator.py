import subprocess
import tempfile
import os
import json
import time
from groq import Groq

class CodeEvaluator:
    """Evaluates user code solutions for correctness and efficiency"""
    
    def __init__(self):
        # Use Groq API instead of OpenAI/Ollama
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY", "your-groq-api-key")  # Get from environment or set a default
        )
        self.model = "llama3-70b-8192"  # Groq's Llama 3 model
        
        # Timeout for code execution (in seconds)
        self.timeout = 5
    
    def evaluate(self, problem_id, code, language='python'):
        """Evaluate a user's solution to a problem"""
        if language != 'python':
            return {"error": "Currently only Python solutions are supported"}
        
        # Get test cases for the problem
        test_cases = self._get_test_cases(problem_id)
        
        # Prepare the code for execution
        prepared_code = self._prepare_code(code, test_cases)
        
        # Execute the code and get results
        execution_results = self._execute_code(prepared_code)
        
        # If execution failed, return the error
        if 'error' in execution_results:
            return execution_results
        
        # Analyze the code quality and efficiency
        code_analysis = self._analyze_code(problem_id, code, execution_results)
        
        # Combine results
        return {
            "passed": execution_results["passed"],
            "total_tests": execution_results["total_tests"],
            "execution_time": execution_results["execution_time"],
            "test_results": execution_results["test_results"],
            "code_analysis": code_analysis
        }
    
    def _get_test_cases(self, problem_id):
        """Get test cases for a specific problem"""
        # In a real implementation, this would fetch from database
        # For this example, we'll use some hardcoded test cases
        test_cases = {
            # Array problems
            "arrays_1": [
                {"input": "[1, 2, 3, 4, 5]", "expected": "15"},
                {"input": "[]", "expected": "0"},
                {"input": "[10]", "expected": "10"}
            ],
            # Linked List problems
            "linked_lists_1": [
                {"input": "1->2->3->4->5", "expected": "5->4->3->2->1"},
                {"input": "1", "expected": "1"},
                {"input": "", "expected": ""}
            ],
            # Default test cases if problem not found
            "default": [
                {"input": "test_input", "expected": "test_output"}
            ]
        }
        
        return test_cases.get(problem_id, test_cases["default"])
    
    def _prepare_code(self, code, test_cases):
        """Prepare the user code for execution with test cases"""
        # Wrap the user code in a class/function for testing
        prepared_code = f"""
import time
import sys
import json

# User solution
{code}

# Test execution
def run_tests():
    test_results = []
    start_time = time.time()
    
    # Assuming the user defined a function called 'solution'
    # Modify this according to your expected function name and signature
    test_cases = {json.dumps(test_cases)}
    
    for i, test in enumerate(test_cases):
        try:
            # Parse input based on the problem type
            # This is a simplification - you'd need proper parsing based on the problem
            input_data = eval(test["input"]) if test["input"] else None
            expected = eval(test["expected"]) if test["expected"] else None
            
            # Call the user's solution
            if input_data is None:
                result = solution()
            elif isinstance(input_data, list):
                result = solution(input_data)
            else:
                result = solution(input_data)
            
            # Check if result matches expected output
            passed = result == expected
            
            test_results.append({
                "test_number": i + 1,
                "input": test["input"],
                "expected": test["expected"],
                "actual": str(result),
                "passed": passed
            })
        except Exception as e:
            test_results.append({
                "test_number": i + 1,
                "input": test["input"],
                "expected": test["expected"],
                "actual": str(e),
                "passed": False,
                "error": str(e)
            })
    
    execution_time = time.time() - start_time
    
    # Count passed tests
    passed_tests = sum(1 for t in test_results if t["passed"])
    
    return {{
        "passed": passed_tests,
        "total_tests": len(test_cases),
        "execution_time": execution_time,
        "test_results": test_results
    }}

# Execute tests and print results
print(json.dumps(run_tests()))
"""
        return prepared_code
    
    def _execute_code(self, code):
        """Execute the prepared code and return results"""
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
            temp_name = temp.name
            temp.write(code.encode('utf-8'))
        
        try:
            # Execute code with timeout
            start_time = time.time()
            result = subprocess.run(
                ['python', temp_name],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            execution_time = time.time() - start_time
            
            # Parse the output
            if result.returncode != 0:
                return {
                    "error": f"Execution failed: {result.stderr}",
                    "passed": 0,
                    "total_tests": 0,
                    "execution_time": execution_time,
                    "test_results": []
                }
            
            # Try to parse JSON output
            try:
                output = json.loads(result.stdout)
                return output
            except json.JSONDecodeError:
                return {
                    "error": f"Failed to parse results: {result.stdout}",
                    "passed": 0,
                    "total_tests": 0,
                    "execution_time": execution_time,
                    "test_results": []
                }
                
        except subprocess.TimeoutExpired:
            return {
                "error": "Code execution timed out",
                "passed": 0,
                "total_tests": 0,
                "execution_time": self.timeout,
                "test_results": []
            }
        finally:
            # Clean up temporary file
            if os.path.exists(temp_name):
                os.unlink(temp_name)
    
    def _analyze_code(self, problem_id, code, execution_results):
        """Analyze the code quality and efficiency"""
        # If code didn't pass all tests, skip detailed analysis
        if execution_results["passed"] < execution_results["total_tests"]:
            return {
                "time_complexity": "N/A - Solution incorrect",
                "space_complexity": "N/A - Solution incorrect",
                "code_quality": "N/A - Solution incorrect",
                "improvement_suggestions": "Focus on fixing correctness issues before optimizing."
            }
        
        # Use AI to analyze the code
        prompt = f"""
        You are an expert Python code reviewer specializing in data structures and algorithms.
        
        Analyze the following solution to problem ID '{problem_id}':
        
        ```python
        {code}
        ```
        
        Execution info:
        - Passed {execution_results["passed"]} out of {execution_results["total_tests"]} tests
        - Execution time: {execution_results["execution_time"]:.6f} seconds
        
        Provide a JSON analysis with these fields:
        1. time_complexity: Big O notation and explanation
        2. space_complexity: Big O notation and explanation
        3. code_quality: Score from 1-10 with brief reasoning
        4. improvement_suggestions: 2-3 specific ways to improve the code
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            # Parse and return the JSON response
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            # Fallback if AI analysis fails
            return {
                "time_complexity": "Analysis unavailable",
                "space_complexity": "Analysis unavailable",
                "code_quality": "Analysis unavailable",
                "improvement_suggestions": "Analysis unavailable",
                "error": str(e)
            }