import os
import json
import subprocess
import time
import re
from pathlib import Path
try:
    from google import genai
except ImportError:
    print("google-genai not installed.")
    exit(1)

client = genai.Client()
MODEL = "gemini-2.5-flash"
MAX_DEBUG_RETRIES = 3

class AutoResearcher:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.project_name = self.project_dir.name
        self.history_file = self.project_dir / "research_history.json"
        self.load_history()

    def load_history(self):
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = {"attempted_ideas": []}

    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def get_baseline_code(self):
        # Find the main python file in the project directory to use as a baseline
        py_files = list(self.project_dir.glob("*.py"))
        if not py_files:
            return None, "No python baseline found."
        
        # Prefer a file named 'baseline.py' or 'minimal_example.py', else just take the first one
        baseline_file = next((f for f in py_files if "minimal" in f.name or "baseline" in f.name), py_files[0])
        with open(baseline_file, 'r') as f:
            return baseline_file.name, f.read()

    def generate_ideas(self, baseline_code):
        print(f"\n[Phase 1] Generating research ideas for {self.project_name}...")
        prompt = f"""
        You are an elite AI Hardware Accelerator Architect.
        Review the following baseline PyTorch implementation for a hardware/algorithm optimization.
        
        Baseline Code:
        ```python
        {baseline_code}
        ```
        
        Previous ideas we have already tried (DO NOT SUGGEST THESE):
        {self.history['attempted_ideas']}
        
        Propose exactly ONE novel, highly specific mathematical or architectural modification to improve this code.
        Focus on memory compression, compute throughput, or quantization techniques relevant to modern LLMs/Accelerators (like Qwen, Llama).
        
        Output format:
        IDEA_NAME: <short name>
        DESCRIPTION: <1 paragraph detailed explanation of the math/architecture>
        """
        response = client.models.generate_content(model=MODEL, contents=prompt)
        text = response.text
        
        # Parse the output
        try:
            name = re.search(r"IDEA_NAME:\s*(.+)", text).group(1).strip()
            desc = re.search(r"DESCRIPTION:\s*(.+)", text, re.DOTALL).group(1).strip()
            return name, desc
        except:
            print("Failed to parse LLM idea output.")
            return "Fallback Idea", text

    def implement_code(self, baseline_code, idea_name, idea_desc):
        print(f"\n[Phase 2] Writing PyTorch implementation for: {idea_name}")
        prompt = f"""
        You are an elite PyTorch engineer. Modify the baseline code to implement the following novel architectural idea.
        
        Idea: {idea_name}
        Description: {idea_desc}
        
        Baseline Code:
        ```python
        {baseline_code}
        ```
        
        Return ONLY the raw python code. Do not use markdown code blocks like ```python. Just the raw text of the script.
        Ensure it prints evaluation metrics (like accuracy, memory size, or latency) to stdout so we can measure success.
        """
        response = client.models.generate_content(model=MODEL, contents=prompt)
        # Strip markdown if the LLM ignores the instruction
        code = response.text.replace("```python", "").replace("```", "").strip()
        return code

    def execute_and_debug(self, code_string, idea_name):
        print(f"\n[Phase 3] Sandboxed Execution & Auto-Debugging...")
        
        # Create a unique filename for this experiment
        safe_name = idea_name.lower().replace(" ", "_").replace("/", "")
        exp_file = self.project_dir / f"exp_{safe_name}.py"
        
        retries = 0
        current_code = code_string
        
        while retries <= MAX_DEBUG_RETRIES:
            with open(exp_file, 'w') as f:
                f.write(current_code)
                
            print(f"  -> Run attempt {retries + 1}/{MAX_DEBUG_RETRIES + 1}...")
            # Execute in a subprocess with a strict 2-minute timeout to prevent infinite loops/OOM hangs
            try:
                result = subprocess.run(
                    ["python", str(exp_file)], 
                    capture_output=True, 
                    text=True, 
                    timeout=120
                )
            except subprocess.TimeoutExpired:
                print("  -> [FATAL] Script timed out after 120s. Killing experiment.")
                return False, "Timeout Error", ""

            if result.returncode == 0:
                print("  -> [SUCCESS] Code executed flawlessly.")
                return True, result.stdout, str(exp_file)
            else:
                error_log = result.stderr.strip()
                print(f"  -> [ERROR] Execution failed. Passing traceback to LLM for auto-fix.")
                
                if retries == MAX_DEBUG_RETRIES:
                    print("  -> [FATAL] Max debug retries reached. Abandoning idea.")
                    return False, error_log, str(exp_file)
                
                # Auto-Debug Prompt
                debug_prompt = f"""
                The following PyTorch code crashed during execution.
                
                Code:
                {current_code}
                
                Error Traceback:
                {error_log}
                
                Fix the bug and return ONLY the completely corrected raw Python code. No markdown, no explanations.
                """
                response = client.models.generate_content(model=MODEL, contents=debug_prompt)
                current_code = response.text.replace("```python", "").replace("```", "").strip()
                retries += 1

    def write_report(self, idea_name, idea_desc, execution_output, exp_file):
        print(f"\n[Phase 4] Generating Academic Report...")
        prompt = f"""
        Act as an AI Hardware Architect publishing a short research paper.
        You proposed the following idea: {idea_name}
        Description: {idea_desc}
        
        The code was executed successfully. Here is the stdout result (metrics, accuracy, memory):
        {execution_output}
        
        Write a highly technical, concise Markdown report summarizing:
        1. The Architectural Hypothesis (What did we change from the baseline?)
        2. The Implementation (Briefly explain the math/PyTorch changes)
        3. Empirical Results (Analyze the stdout metrics above. Did it work? Did accuracy drop? Did memory footprint shrink?)
        4. Conclusion (Is this viable for Edge AI / Apple Silicon deployment?)
        """
        response = client.models.generate_content(model=MODEL, contents=prompt)
        report_content = response.text
        
        date_str = time.strftime("%Y-%m-%d")
        report_file = self.project_dir / f"report_{date_str}_{idea_name.lower().replace(' ', '_')}.md"
        
        with open(report_file, 'w') as f:
            f.write(report_content)
            
        print(f"  -> Report saved to: {report_file}")
        return str(report_file)

    def run(self):
        baseline_name, baseline_code = self.get_baseline_code()
        if not baseline_name:
            print(baseline_code)
            return

        print(f"Found baseline: {baseline_name}")
        
        # 1. Idea
        idea_name, idea_desc = self.generate_ideas(baseline_code)
        print(f"  -> Selected Idea: {idea_name}")
        self.history["attempted_ideas"].append(idea_name)
        self.save_history()

        # 2. Code
        new_code = self.implement_code(baseline_code, idea_name, idea_desc)
        
        # 3. Execute & Debug
        success, output, exp_file = self.execute_and_debug(new_code, idea_name)
        
        if success:
            # 4. Report
            report_file = self.write_report(idea_name, idea_desc, output, exp_file)
            print(f"\n[AUTO-RESEARCH COMPLETE] Successfully prototyped and analyzed: {idea_name}")
            return report_file, exp_file
        else:
            print(f"\n[AUTO-RESEARCH FAILED] Could not execute {idea_name} after {MAX_DEBUG_RETRIES} debug attempts.")
            return None, None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python research_loop.py <path_to_project_dir>")
        sys.exit(1)
        
    target_dir = sys.argv[1]
    researcher = AutoResearcher(target_dir)
    researcher.run()
