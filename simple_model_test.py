#!/usr/bin/env python3
"""
Simple model availability test for OpenClaw
"""

import json
import subprocess
import time
from datetime import datetime

def test_model(model_name):
    """Test if a model is available"""
    print(f"Testing model: {model_name}")
    
    try:
        # Test with a simple command
        cmd = ['openclaw', 'session_status', '--model', model_name]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print(f"  SUCCESS: Model {model_name} is available")
            return True
        else:
            print(f"  FAILED: Model {model_name} is not available")
            print(f"    Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: Model {model_name} test timed out")
        return False
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False

def main():
    print("OpenClaw Model Availability Test")
    print("=" * 50)
    print(f"Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load configuration
    config_path = r'C:\Users\flyan\.openclaw\openclaw.json'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return
    
    # Get model lists
    primary_model = config['agents']['defaults']['model']['primary']
    fallback_models = config['agents']['defaults']['model']['fallbacks']
    model_aliases = config['agents']['defaults']['models']
    
    print(f"Primary model: {primary_model}")
    print(f"Number of fallback models: {len(fallback_models)}")
    print(f"Number of configured models: {len(model_aliases)}")
    print()
    
    # Test models
    all_models = [primary_model] + fallback_models + list(model_aliases.keys())
    # Remove duplicates while preserving order
    seen = set()
    unique_models = []
    for model in all_models:
        if model not in seen:
            seen.add(model)
            unique_models.append(model)
    
    print(f"Testing {len(unique_models)} unique models...")
    print()
    
    available_models = []
    unavailable_models = []
    
    for i, model in enumerate(unique_models, 1):
        print(f"[{i}/{len(unique_models)}] ", end="")
        if test_model(model):
            available_models.append(model)
        else:
            unavailable_models.append(model)
        print()
    
    # Summary
    print("=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Total models tested: {len(unique_models)}")
    print(f"Available models: {len(available_models)}")
    print(f"Unavailable models: {len(unavailable_models)}")
    print()
    
    if available_models:
        print("AVAILABLE MODELS:")
        for i, model in enumerate(available_models, 1):
            print(f"  {i}. {model}")
        print()
    
    if unavailable_models:
        print("UNAVAILABLE MODELS:")
        for i, model in enumerate(unavailable_models, 1):
            print(f"  {i}. {model}")
        print()
    
    # Save report
    report_lines = [
        "OpenClaw Model Availability Test Report",
        "=" * 50,
        f"Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Total models tested: {len(unique_models)}",
        f"Available models: {len(available_models)}",
        f"Unavailable models: {len(unavailable_models)}",
        "",
    ]
    
    if available_models:
        report_lines.extend([
            "AVAILABLE MODELS:",
            * [f"  {i}. {model}" for i, model in enumerate(available_models, 1)],
            ""
        ])
    
    if unavailable_models:
        report_lines.extend([
            "UNAVAILABLE MODELS:",
            * [f"  {i}. {model}" for i, model in enumerate(unavailable_models, 1)],
            ""
        ])
    
    report_lines.extend([
        "RECOMMENDATIONS:",
        "1. Use available models for your tasks",
        "2. Check API keys for unavailable models",
        "3. Consider network connectivity issues",
        "",
        f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ])
    
    report_path = r'C:\Users\flyan\.openclaw\workspace\model_test_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Detailed report saved to: {report_path}")

if __name__ == '__main__':
    main()