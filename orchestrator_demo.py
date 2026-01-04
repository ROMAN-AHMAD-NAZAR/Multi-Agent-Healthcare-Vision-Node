# ============================================================
# 🤖 MEDICAL MULTI-AGENT ORCHESTRATOR
# ============================================================
# This script demonstrates how the Vision Agent Node integrates
# into a larger Multi-Agent System managed by an LLM Orchestrator.
#
# Architecture:
#   User Request → Orchestrator → Vision Agent → JSON Response → Report
# ============================================================

import json
import time
from datetime import datetime

# --- 1. MOCK VISION AGENT NODE (The "Plug" for your Notebook) ---
# In production, you would import this: 
# from Vision_Agent_2_5D_Attention import run_vision_agent

def call_vision_node(image_path):
    """
    Simulates calling the Vision Agent Node.
    In production, this would execute the actual model inference.
    """
    print(f"\n[System] 📡 Connecting to Vision Agent Node...")
    print(f"[System] 📤 Sending payload: {image_path}")
    
    # Simulate processing time (the 'thinking' phase)
    time.sleep(2) 
    
    # This is the exact JSON format your Notebook outputs
    vision_response = {
        "agent_id": "vision_expert_01",
        "agent_type": "2.5D_Attention_UNet",
        "timestamp": datetime.now().isoformat(),
        "diagnosis": "Glioma",
        "confidence_score": 0.94,
        "stability_check": "PASSED",
        "stability_score": 0.9812,
        "tumor_size_cm": 2.45,
        "tumor_location": "Temporal Lobe (Approximated)",
        "explanation_path": "./outputs/gradcam_heatmap.png",
        "model_version": "v1.0.0"
    }
    
    print(f"[System] 📥 Received structured data from Vision Node.")
    return vision_response


# --- 2. MOCK VALIDATION AGENT (Neo4j Knowledge Graph) ---
def call_validation_agent(diagnosis):
    """
    Simulates the Validation Agent that cross-references
    diagnosis with medical knowledge graphs.
    """
    print(f"\n[System] 🔍 Querying Validation Agent (Neo4j)...")
    time.sleep(1)
    
    # Simulated knowledge graph lookup
    knowledge_base = {
        "Glioma": {
            "severity": "High",
            "common_treatments": ["Surgery", "Radiation Therapy", "Chemotherapy"],
            "survival_rate": "Variable (depends on grade)",
            "icd_code": "C71.9"
        },
        "Meningioma": {
            "severity": "Low to Moderate",
            "common_treatments": ["Observation", "Surgery", "Radiation"],
            "survival_rate": "Generally favorable",
            "icd_code": "D32.9"
        },
        "No Tumor": {
            "severity": "None",
            "common_treatments": ["None required"],
            "survival_rate": "N/A",
            "icd_code": "N/A"
        }
    }
    
    return knowledge_base.get(diagnosis, {"severity": "Unknown"})


# --- 3. THE ORCHESTRATOR (The "Brain") ---
class MedicalOrchestrator:
    """
    Central orchestrator that manages the multi-agent workflow.
    In production, this would be powered by an LLM (GPT-4, Claude, etc.)
    """
    
    def __init__(self):
        self.system_prompt = """You are a helpful medical assistant. 
        Use specialized tools for precise diagnosis. 
        Always validate findings with knowledge graphs."""
        self.conversation_history = []
    
    def process_request(self, user_query, image_path=None):
        """
        Main entry point for processing user requests.
        Implements routing logic to determine which agents to invoke.
        """
        print("=" * 60)
        print(f"🔹 USER: {user_query}")
        print("=" * 60)
        
        # LOGIC 1: ROUTING (Deciding what to do)
        if image_path:
            print("\n[Orchestrator] 🧠 Intent detected: Medical Image Analysis")
            print("[Orchestrator] 🛠️  Routing to: VISION_AGENT_NODE")
            
            # Step 1: Call Vision Agent
            vision_data = call_vision_node(image_path)
            
            # Step 2: Validate with Knowledge Graph
            print("\n[Orchestrator] 🛠️  Routing to: VALIDATION_AGENT")
            validation_data = call_validation_agent(vision_data["diagnosis"])
            
            # Step 3: Synthesize final response
            return self.synthesize_response(vision_data, validation_data)
        else:
            return "[Orchestrator] ⚠️ Please provide an MRI image for analysis."

    def synthesize_response(self, vision_data, validation_data):
        """
        Combines outputs from multiple agents into a coherent report.
        This simulates how an LLM would generate natural language from structured data.
        """
        print("\n[Orchestrator] 📝 Synthesizing Final Report...")
        time.sleep(1)
        
        # Build the clinical report
        confidence_pct = vision_data['confidence_score'] * 100
        stability_status = "✅ Stable" if vision_data['stability_check'] == "PASSED" else "⚠️ Unstable"
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          🏥 AUTOMATED PRELIMINARY DIAGNOSTIC REPORT          ║
╠══════════════════════════════════════════════════════════════╣
║  Date: {vision_data['timestamp'][:19]}                          
║  Agent: {vision_data['agent_id']} ({vision_data['model_version']})              
╠══════════════════════════════════════════════════════════════╣
║                      PRIMARY FINDING                         ║
╠══════════════════════════════════════════════════════════════╣
║  Diagnosis: {vision_data['diagnosis'].upper()}
║  Location:  {vision_data['tumor_location']}
║  Size:      {vision_data['tumor_size_cm']} cm
╠══════════════════════════════════════════════════════════════╣
║                      AI CONFIDENCE                           ║
╠══════════════════════════════════════════════════════════════╣
║  Confidence Score:  {confidence_pct:.1f}%
║  Stability Check:   {stability_status}
║  Stability Score:   {vision_data['stability_score']}
╠══════════════════════════════════════════════════════════════╣
║                 KNOWLEDGE GRAPH VALIDATION                   ║
╠══════════════════════════════════════════════════════════════╣
║  Severity Level:    {validation_data['severity']}
║  ICD-10 Code:       {validation_data.get('icd_code', 'N/A')}
║  Common Treatments: {', '.join(validation_data.get('common_treatments', ['N/A']))}
╠══════════════════════════════════════════════════════════════╣
║                      NEXT STEPS                              ║
╠══════════════════════════════════════════════════════════════╣
║  1. Review XAI Saliency Map: {vision_data['explanation_path']}
║  2. Consult with specialist for confirmation
║  3. Schedule follow-up imaging if required
╚══════════════════════════════════════════════════════════════╝

⚠️ DISCLAIMER: This is an AI-assisted preliminary analysis.
   Final diagnosis must be confirmed by a qualified physician.
"""
        return report


# --- 4. INTERACTIVE CLI DEMO ---
def run_interactive_demo():
    """
    Interactive demonstration mode for presenting to stakeholders.
    """
    print("\n" + "="*60)
    print("   🤖 MEDICAL MULTI-AGENT SYSTEM - INTERACTIVE DEMO")
    print("="*60)
    print("\nThis demo simulates how the Vision Agent integrates")
    print("into a larger healthcare AI pipeline.\n")
    
    orchestrator = MedicalOrchestrator()
    
    while True:
        print("\n" + "-"*40)
        print("OPTIONS:")
        print("  [1] Analyze sample MRI scan")
        print("  [2] View system architecture")
        print("  [3] Exit")
        print("-"*40)
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            user_query = "Can you analyze this brain MRI for any anomalies?"
            test_image = "./data/test/patient_scan_001.jpg"
            
            report = orchestrator.process_request(user_query, test_image)
            print(report)
            
        elif choice == "2":
            print("""
    ┌─────────────────────────────────────────────────────────┐
    │              MULTI-AGENT SYSTEM ARCHITECTURE            │
    └─────────────────────────────────────────────────────────┘
    
         ┌──────────────┐
         │  User Input  │
         │  (MRI Scan)  │
         └──────┬───────┘
                │
                ▼
    ┌───────────────────────┐
    │     ORCHESTRATOR      │  ◄── LLM-Powered Decision Maker
    │   (This Script)       │
    └───────────┬───────────┘
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────────┐
│   VISION    │   │   VALIDATION    │
│   AGENT     │   │     AGENT       │
│ (Notebook)  │   │   (Neo4j KG)    │
└──────┬──────┘   └────────┬────────┘
       │                   │
       │    JSON Payloads  │
       └─────────┬─────────┘
                 │
                 ▼
         ┌──────────────┐
         │   CLINICAL   │
         │    REPORT    │
         └──────────────┘
            """)
            
        elif choice == "3":
            print("\n👋 Exiting Multi-Agent System Demo. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please select 1, 2, or 3.")


# --- 5. RUN THE SIMULATION ---
if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🧠 MULTI-AGENT HEALTHCARE VISION SYSTEM                 ║
    ║                                                           ║
    ║   Demonstrating Integration of:                           ║
    ║   • Vision Agent Node (2.5D Attention U-Net)              ║
    ║   • Validation Agent (Knowledge Graph)                    ║
    ║   • LLM Orchestrator (Central Manager)                    ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Run simple demo first
    print("--- RUNNING AUTOMATED DEMO ---\n")
    
    bot = MedicalOrchestrator()
    
    # Scenario: A doctor uploads a scan
    user_query = "Can you check this MRI for any anomalies?"
    test_image = "./data/test/scan_04.jpg"
    
    final_output = bot.process_request(user_query, test_image)
    print(final_output)
    
    # Ask if user wants interactive mode
    print("\n" + "="*60)
    response = input("Would you like to enter interactive mode? (y/n): ").strip().lower()
    if response == 'y':
        run_interactive_demo()
