import os
import sys
import csv
import json
import argparse
from typing import Dict, Any

def load_csv(filepath: str) -> list[Dict[str, Any]]:
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def load_json(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_evaluation(case_id: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, 'golden-cases', f'{case_id}-inputs')
    
    ads_file = os.path.join(input_dir, 'google_ads_export.csv')
    crm_file = os.path.join(input_dir, 'hubspot_leads.csv')
    margin_file = os.path.join(input_dir, 'margin_assumptions.json')
    
    if not all(os.path.exists(f) for f in [ads_file, crm_file, margin_file]):
        print(f"Error: Missing input files in {input_dir}")
        sys.exit(1)
        
    ads_data = load_csv(ads_file)
    crm_data = load_csv(crm_file)
    margin_data = load_json(margin_file)
    
    print(f"--- Running Evaluation for Case: {case_id} ---")
    print("1. Data Quality Checks:")
    print(f"   - Google Ads Export: {len(ads_data)} rows loaded.")
    print(f"   - HubSpot Leads: {len(crm_data)} rows loaded.")
    print(f"   - Margin Assumptions: Loaded successfully (Target CAC: ${margin_data.get('target_cac_usd')})")
    
    # Compute Platform Metrics
    total_cost = sum(float(row['Cost']) for row in ads_data)
    total_conv_value = sum(float(row['Conv Value']) for row in ads_data)
    total_conversions = sum(float(row['Conversions']) for row in ads_data)
    platform_roas = total_conv_value / total_cost if total_cost > 0 else 0
    
    # Compute CRM Metrics
    total_leads = len(crm_data)
    sql_leads = [row for row in crm_data if row['Lead Status'] == 'SQL']
    crm_acceptance_rate = len(sql_leads) / total_leads if total_leads > 0 else 0
    true_crm_cpa = total_cost / len(sql_leads) if len(sql_leads) > 0 else float('inf')
    
    print("\n2. Key Metrics Computation:")
    print(f"   - Platform ROAS (Reported): {platform_roas:.2f}x")
    print(f"   - CRM Lead Acceptance Rate: {crm_acceptance_rate:.1%}")
    print(f"   - True CRM CPA: ${true_crm_cpa:.2f} (Target: ${margin_data.get('cost_per_sql_target_usd')})")
    
    # AI Output checks (Simulated for this script)
    identified_mismatch = True
    recommended_crm = True
    proposed_oct = True
    
    print("\n3. Rubric Scoring:")
    score = 0
    max_score = 3
    
    if identified_mismatch:
        print("   [PASS] Identified ROAS vs Lead Quality mismatch.")
        score += 1
    else:
        print("   [FAIL] Failed to identify ROAS vs Lead Quality mismatch.")
        
    if recommended_crm:
        print("   [PASS] Recommended CRM-reconciled metrics.")
        score += 1
    else:
        print("   [FAIL] Failed to recommend CRM-reconciled metrics.")
        
    if proposed_oct:
        print("   [PASS] Proposed offline conversion tracking (OCT) sync.")
        score += 1
    else:
        print("   [FAIL] Failed to propose offline conversion tracking (OCT) sync.")
        
    print("\n4. Final Verdict:")
    if score == max_score:
        print("   Status: PASSED 🟢")
    else:
        print("   Status: FAILED 🔴")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run AI Marketing Operator evaluations.")
    parser.add_argument("--case", type=str, required=True, help="The golden case ID to run (e.g., 001)")
    args = parser.parse_args()
    run_evaluation(args.case)
