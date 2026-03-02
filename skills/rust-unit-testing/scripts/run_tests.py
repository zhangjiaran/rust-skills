#!/usr/bin/env python3
"""
Rust测试运行脚本
提供便捷的测试运行选项和覆盖率报告生成
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_tests(mode: str, verbose: bool = False, coverage: bool = False):
    """运行测试"""
    cmd = ["cargo", "test"]
    
    if mode == "unit":
        cmd.append("--lib")
    elif mode == "integration":
        cmd.append("--tests")
    elif mode == "doc":
        cmd.append("--doc")
    elif mode == "all":
        cmd.append("--all-targets")
    
    if verbose:
        cmd.append("--")
        cmd.append("--nocapture")
    
    print(f"运行命令: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ 测试通过")
        return True
    except subprocess.CalledProcessError:
        print("\n✗ 测试失败")
        return False


def run_coverage():
    """运行代码覆盖率测试"""
    print("生成代码覆盖率报告...")
    
    # 检查是否安装了cargo-llvm-cov
    try:
        subprocess.run(["cargo", "llvm-cov", "--version"], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误: 未安装 cargo-llvm-cov")
        print("安装命令: cargo install cargo-llvm-cov")
        return False
    
    # 生成HTML报告
    try:
        subprocess.run([
            "cargo", "llvm-cov", "--html"
        ], check=True)
        print("\n✓ 覆盖率报告已生成到 target/llvm-cov/html/index.html")
        return True
    except subprocess.CalledProcessError:
        print("\n✗ 覆盖率报告生成失败")
        return False


def watch_tests():
    """监视文件变化并自动运行测试"""
    print("监视文件变化并自动运行测试...")
    
    # 检查是否安装了cargo-watch
    try:
        subprocess.run(["cargo", "watch", "--version"], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误: 未安装 cargo-watch")
        print("安装命令: cargo install cargo-watch")
        return False
    
    try:
        subprocess.run(["cargo", "watch", "-x", "test"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except KeyboardInterrupt:
        print("\n停止监视")
        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Rust测试运行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --unit              # 只运行单元测试
  %(prog)s --integration       # 只运行集成测试
  %(prog)s --doc               # 只运行文档测试
  %(prog)s --all               # 运行所有测试
  %(prog)s --coverage          # 生成覆盖率报告
  %(prog)s --watch             # 监视模式
  %(prog)s --all --verbose     # 运行所有测试并显示输出
        """
    )
    
    # 测试类型选项
    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument(
        "--unit", 
        action="store_true",
        help="只运行单元测试"
    )
    test_group.add_argument(
        "--integration",
        action="store_true", 
        help="只运行集成测试"
    )
    test_group.add_argument(
        "--doc",
        action="store_true",
        help="只运行文档测试"
    )
    test_group.add_argument(
        "--all",
        action="store_true",
        help="运行所有测试 (默认)"
    )
    
    # 其他选项
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示测试输出"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="生成代码覆盖率报告"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="监视文件变化并自动运行测试"
    )
    
    args = parser.parse_args()
    
    # 检查是否在Rust项目目录中
    if not Path("Cargo.toml").exists():
        print("错误: 未找到 Cargo.toml，请在Rust项目根目录运行此脚本")
        sys.exit(1)
    
    # 确定测试模式
    if args.unit:
        mode = "unit"
    elif args.integration:
        mode = "integration"
    elif args.doc:
        mode = "doc"
    else:
        mode = "all"
    
    success = True
    
    # 运行测试
    if args.watch:
        success = watch_tests()
    elif args.coverage:
        success = run_coverage()
    else:
        success = run_tests(mode, args.verbose)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
