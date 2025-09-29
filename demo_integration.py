#!/usr/bin/env python3
"""
Demo showing how SecurityPrompt integrates with the existing project.
This demonstrates the __repr__ functionality in a practical context.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from security_prompt import SecurityPrompt


def main():
    """Demo integration with security prompt analysis."""
    print("🔒 Security Prompt Analysis Integration Demo")
    print("=" * 55)
    
    # Load security prompts from data files
    all_prompts = []
    
    data_files = [
        "data/sec_rompts.txt",
        "data/security_prompts.jsonl.txt"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            prompts = SecurityPrompt.load_from_jsonl(file_path)
            all_prompts.extend(prompts)
            print(f"📁 Loaded {len(prompts)} prompts from {file_path}")
    
    print(f"\n📊 Total prompts loaded: {len(all_prompts)}")
    
    # Demonstrate __repr__ in different contexts
    print("\n🎯 Security Prompt Analysis:")
    print("-" * 30)
    
    # Group by threat type
    threat_analysis = {}
    for prompt in all_prompts:
        label = prompt.label
        if label not in threat_analysis:
            threat_analysis[label] = []
        threat_analysis[label].append(prompt)
    
    for label, prompts in sorted(threat_analysis.items()):
        print(f"\n🏷️  {label.upper()} ({len(prompts)} prompts):")
        
        # Show first few with repr for debugging/analysis
        for i, prompt in enumerate(prompts[:3], 1):
            print(f"   {i}. {repr(prompt)}")
        
        if len(prompts) > 3:
            print(f"   ... and {len(prompts) - 3} more {label} prompts")
    
    # Demonstrate filtering and analysis
    print(f"\n🔍 Threat Detection Summary:")
    total_threats = sum(1 for p in all_prompts if p.is_security_threat())
    print(f"   Total security threats: {total_threats}/{len(all_prompts)}")
    
    # Find unique patterns
    print(f"\n🧠 Pattern Analysis:")
    injection_patterns = [p for p in all_prompts if p.label == 'injection']
    if injection_patterns:
        print(f"   Injection prompts analysis:")
        for prompt in injection_patterns[:2]:
            print(f"     - {repr(prompt)}")
            
    # Demonstrate the power of __repr__ for debugging
    print(f"\n🐛 Debugging Example - Finding Specific Patterns:")
    rm_prompts = [p for p in all_prompts if 'rm -rf' in p.input]
    if rm_prompts:
        print(f"   Found {len(rm_prompts)} prompts containing 'rm -rf':")
        for prompt in rm_prompts:
            print(f"     - {repr(prompt)}")
    
    # Show how __repr__ helps with data validation
    print(f"\n✅ Data Validation using __repr__:")
    empty_prompts = [p for p in all_prompts if not p.input.strip()]
    if empty_prompts:
        print(f"   ⚠️  Found {len(empty_prompts)} empty prompts:")
        for prompt in empty_prompts:
            print(f"     - {repr(prompt)}")
    else:
        print(f"   ✅ All prompts have valid input text")
    
    # Demonstrate conversion capabilities
    print(f"\n🔄 Data Format Conversion Example:")
    sample_prompt = all_prompts[0] if all_prompts else None
    if sample_prompt:
        print(f"   Original: {repr(sample_prompt)}")
        print(f"   Dict:     {sample_prompt.to_dict()}")
        print(f"   String:   {str(sample_prompt)}")
        
        # Round-trip test
        reconstructed = SecurityPrompt.from_dict(sample_prompt.to_dict())
        print(f"   Round-trip successful: {sample_prompt == reconstructed}")


if __name__ == "__main__":
    main()