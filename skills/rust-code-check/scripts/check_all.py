#!/usr/bin/env python3
"""
Rust代码质量检查脚本
运行所有代码质量检查工具：格式化、lint、安全审计
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """运行命令并返回是否成功"""
    print(f"\n{'='*60}")
    print(f"运行: {description}")
    print(f"命令: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✓ {description} 通过")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} 失败 (退出码: {e.returncode})")
        return False
    except FileNotFoundError:
        print(f"✗ 找不到命令: {cmd[0]}")
        return False


def main():
    """主函数"""
    # 检查是否在Rust项目目录中
    if not Path("Cargo.toml").exists():
        print("错误: 未找到 Cargo.toml，请在Rust项目根目录运行此脚本")
        sys.exit(1)
    
    results = []
    
    # 1. 格式化检查
    results.append(run_command(
        ["cargo", "fmt", "--", "--check"],
        "代码格式化检查 (rustfmt)"
    ))
    
    # 2. Clippy检查
    results.append(run_command(
        ["cargo", "clippy", "--all-targets", "--all-features", "--", "-D", "warnings"],
        "Clippy静态分析"
    ))
    
    # 3. 类型检查
    results.append(run_command(
        ["cargo", "check", "--all-targets"],
        "类型检查"
    ))
    
    # 4. 测试
    results.append(run_command(
        ["cargo", "test"],
        "运行测试"
    ))
    
    # 5. 安全审计 (可选)
    print(f"\n{'='*60}")
    print("运行: 安全审计 (cargo audit)")
    print('='*60)
    try:
        subprocess.run(["cargo", "audit"], check=True)
        print("✓ 安全审计通过")
        results.append(True)
    except subprocess.CalledProcessError:
        print("⚠ 发现安全漏洞，请检查")
        results.append(False)
    except FileNotFoundError:
        print("⚠ 未安装 cargo-audit，跳过安全审计")
        print("  安装命令: cargo install cargo-audit")
    
    # 总结
    print(f"\n{'='*60}")
    print("检查结果总结")
    print('='*60)
    
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"总计: {total} 项检查")
    print(f"通过: {passed} 项")
    print(f"失败: {failed} 项")
    
    if all(results):
        print("\n✓ 所有检查通过!")
        sys.exit(0)
    else:
        print("\n✗ 部分检查失败，请修复上述问题")
        sys.exit(1)


if __name__ == "__main__":
    main()
