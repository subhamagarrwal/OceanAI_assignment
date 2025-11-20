import json
from pathlib import Path
from datetime import datetime
from core.code_gen import generate_selenium_script

class AutonomousQAAgent:
    def __init__(self, rag_engine, output_dir="generated_tests"):
        self.rag_engine = rag_engine
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_test_plan(self, requirement: str) -> dict:
        print("\n🔍 Step 1: Generating Test Plan...")
        response_json = self.rag_engine.query(f"Generate test scenarios for: {requirement}")
        try:
            test_plan = json.loads(response_json)
            print(f"✅ Generated {len(test_plan.get('test_cases', []))} test cases")
            return test_plan
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            return {"error": "Failed to parse test plan", "raw": response_json}
    
    def generate_selenium_code(self, test_case: dict) -> str:
        print(f"\n🤖 Step 2: Generating Selenium code for TC: {test_case.get('id', 'Unknown')}")
        code = generate_selenium_script(json.dumps(test_case, indent=2))
        return code
    
    def save_artifacts(self, test_plan: dict, codes: dict, requirement: str):
        print("\n💾 Step 3: Saving artifacts...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        plan_file = self.output_dir / f"test_plan_{timestamp}.json"
        with open(plan_file, "w") as f:
            json.dump(test_plan, f, indent=2)
            
        for tc_id, code in codes.items():
            code_file = self.output_dir / f"test_{tc_id}_{timestamp}.py"
            with open(code_file, "w") as f:
                f.write(code)
                
        summary = {
            "requirement": requirement,
            "timestamp": timestamp,
            "test_count": len(codes),
            "test_plan_file": str(plan_file),
            "code_files": [str(self.output_dir / f"test_{tc_id}_{timestamp}.py") for tc_id in codes.keys()]
        }
        
        summary_file = self.output_dir / f"summary_{timestamp}.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)
            
        return summary
    
    def run(self, requirement: str, generate_all_tests=True):
        print("="*60)
        print("🚀 AUTONOMOUS QA AGENT - STARTING")
        print("="*60)
        print(f"📝 Requirement: {requirement}\n")
        
        test_plan = self.generate_test_plan(requirement)
        if "error" in test_plan:
            return test_plan
        
        codes = {}
        test_cases = test_plan.get("test_cases", [])
        if not generate_all_tests:
            test_cases = test_cases[:1]
        
        for tc in test_cases:
            tc_id = tc.get("id", "unknown")
            try:
                code = self.generate_selenium_code(tc)
                codes[tc_id] = code
            except Exception as e:
                print(f"❌ Failed to generate code for {tc_id}: {e}")
                codes[tc_id] = f"# ERROR: {e}"
        
        summary = self.save_artifacts(test_plan, codes, requirement)
        print("\n" + "="*60)
        print("✅ AUTONOMOUS QA AGENT - COMPLETED")
        print("="*60)
        return {"test_plan": test_plan, "codes": codes, "summary": summary}
