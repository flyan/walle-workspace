#!/usr/bin/env python3
"""
测试OpenClaw配置的所有模型可用性
"""

import json
import subprocess
import time
from datetime import datetime

def test_model(model_name, alias=None):
    """测试单个模型的可用性"""
    print(f"测试模型: {model_name}" + (f" (别名: {alias})" if alias else ""))
    
    try:
        # 使用session_status测试模型
        cmd = ['openclaw', 'session_status', '--model', model_name]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"  ✅ 可用 - 响应时间: {elapsed:.2f}秒")
            return True, elapsed
        else:
            print(f"  ❌ 不可用 - 错误: {result.stderr[:100]}")
            return False, elapsed
            
    except subprocess.TimeoutExpired:
        print(f"  ⏱️  超时 (10秒)")
        return False, 10
    except Exception as e:
        print(f"  ❌ 错误: {str(e)[:100]}")
        return False, 0

def main():
    print("=" * 60)
    print("OpenClaw 模型可用性测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 从配置文件读取模型列表
    config_path = r'C:\Users\flyan\.openclaw\openclaw.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 获取主要模型和备用模型
    primary_model = config['agents']['defaults']['model']['primary']
    fallback_models = config['agents']['defaults']['model']['fallbacks']
    model_aliases = config['agents']['defaults']['models']
    
    print(f"\n📊 主要模型: {primary_model}")
    print(f"📊 备用模型: {len(fallback_models)}个")
    
    results = []
    
    # 测试主要模型
    print(f"\n🔍 测试主要模型:")
    available, response_time = test_model(primary_model)
    results.append({
        'model': primary_model,
        'alias': 'haiku',
        'type': 'primary',
        'available': available,
        'response_time': response_time
    })
    
    # 测试所有备用模型
    print(f"\n🔍 测试备用模型:")
    for model in fallback_models:
        # 查找别名
        alias = None
        for model_key, model_info in model_aliases.items():
            if model_key == model and 'alias' in model_info:
                alias = model_info['alias']
                break
        
        available, response_time = test_model(model, alias)
        results.append({
            'model': model,
            'alias': alias,
            'type': 'fallback',
            'available': available,
            'response_time': response_time
        })
    
    # 测试所有配置的模型（包括有别名的）
    print(f"\n🔍 测试所有配置模型:")
    for model_key, model_info in model_aliases.items():
        if model_key not in [r['model'] for r in results]:
            alias = model_info.get('alias')
            available, response_time = test_model(model_key, alias)
            results.append({
                'model': model_key,
                'alias': alias,
                'type': 'configured',
                'available': available,
                'response_time': response_time
            })
    
    # 生成报告
    print(f"\n" + "=" * 60)
    print("📋 模型可用性报告")
    print("=" * 60)
    
    # 统计
    total = len(results)
    available_count = sum(1 for r in results if r['available'])
    unavailable_count = total - available_count
    
    print(f"\n📊 统计:")
    print(f"  总共测试: {total}个模型")
    print(f"  可用模型: {available_count}个")
    print(f"  不可用模型: {unavailable_count}个")
    
    # 可用模型列表
    print(f"\n✅ 可用模型:")
    available_models = [r for r in results if r['available']]
    available_models.sort(key=lambda x: x['response_time'])
    
    for i, model in enumerate(available_models, 1):
        alias_str = f" ({model['alias']})" if model['alias'] else ""
        print(f"  {i:2d}. {model['model']}{alias_str}")
        print(f"     类型: {model['type']}, 响应时间: {model['response_time']:.2f}秒")
    
    # 不可用模型列表
    if unavailable_count > 0:
        print(f"\n❌ 不可用模型:")
        unavailable_models = [r for r in results if not r['available']]
        
        for i, model in enumerate(unavailable_models, 1):
            alias_str = f" ({model['alias']})" if model['alias'] else ""
            print(f"  {i:2d}. {model['model']}{alias_str}")
            print(f"     类型: {model['type']}")
    
    # 推荐使用
    print(f"\n💡 推荐使用:")
    if available_models:
        fastest = available_models[0]
        alias_str = f" ({fastest['alias']})" if fastest['alias'] else ""
        print(f"  最快模型: {fastest['model']}{alias_str} - {fastest['response_time']:.2f}秒")
        
        # 推荐稳定模型
        stable_models = [m for m in available_models if m['type'] in ['primary', 'fallback']]
        if stable_models:
            stable = stable_models[0]
            alias_str = f" ({stable['alias']})" if stable['alias'] else ""
            print(f"  稳定模型: {stable['model']}{alias_str} - {stable['response_time']:.2f}秒")
    
    # 保存结果
    report_path = r'C:\Users\flyan\.openclaw\workspace\model_availability_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# OpenClaw 模型可用性测试报告\n")
        f.write(f"## 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"## 📊 统计概览\n")
        f.write(f"- **总共测试**: {total}个模型\n")
        f.write(f"- **可用模型**: {available_count}个\n")
        f.write(f"- **不可用模型**: {unavailable_count}个\n\n")
        
        f.write(f"## ✅ 可用模型列表\n")
        for model in available_models:
            alias_str = f" ({model['alias']})" if model['alias'] else ""
            f.write(f"1. **{model['model']}**{alias_str}\n")
            f.write(f"   - 类型: {model['type']}\n")
            f.write(f"   - 响应时间: {model['response_time']:.2f}秒\n\n")
        
        if unavailable_count > 0:
            f.write(f"## ❌ 不可用模型列表\n")
            for model in unavailable_models:
                alias_str = f" ({model['alias']})" if model['alias'] else ""
                f.write(f"1. **{model['model']}**{alias_str}\n")
                f.write(f"   - 类型: {model['type']}\n\n")
        
        f.write(f"## 💡 使用建议\n")
        if available_models:
            fastest = available_models[0]
            alias_str = f" ({fastest['alias']})" if fastest['alias'] else ""
            f.write(f"- **最快模型**: {fastest['model']}{alias_str} (响应时间: {fastest['response_time']:.2f}秒)\n")
        
        f.write(f"\n---\n")
        f.write(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    print(f"\n📄 详细报告已保存至: {report_path}")
    
    return results

if __name__ == '__main__':
    main()