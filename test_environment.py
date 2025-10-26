#!/usr/bin/env python3
import sys
import subprocess
import importlib.util

def check_package(package_name, import_name=None):
    """检查包是否可导入"""
    if import_name is None:
        import_name = package_name
    
    try:
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            return False, f"未找到模块 {import_name}"
        else:
            # 尝试获取版本
            mod = importlib.import_module(import_name)
            version = getattr(mod, '__version__', '未知版本')
            return True, f"{package_name} ({version})"
    except ImportError as e:
        return False, f"导入失败: {e}"

def main():
    print("🔍 检查量化开发环境...")
    print("=" * 50)
    
    # 检查Python版本
    print(f"🐍 Python版本: {sys.version}")
    
    # 检查核心库
    core_packages = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("backtrader", "backtrader"),
        ("akshare", "akshare"),
        ("yfinance", "yfinance"),
        ("matplotlib", "matplotlib"),
        ("TA-Lib", "talib"),
    ]
    
    all_good = True
    for pkg_name, import_name in core_packages:
        success, message = check_package(pkg_name, import_name)
        status = "✅" if success else "❌"
        print(f"{status} {pkg_name}: {message}")
        if not success:
            all_good = False
    
    # 测试数据获取
    print("\n📊 测试数据获取功能...")
    try:
        import yfinance as yf
        data = yf.download('AAPL', period='1d', progress=False)
        if not data.empty:
            print("✅ yfinance数据获取测试成功")
        else:
            print("❌ yfinance返回空数据")
            all_good = False
    except Exception as e:
        print(f"❌ 数据获取测试失败: {e}")
        all_good = False
    
    # 测试回测框架
    print("\n⚡ 测试回测框架...")
    try:
        import backtrader as bt
        print("✅ Backtrader导入成功")
    except Exception as e:
        print(f"❌ Backtrader导入失败: {e}")
        all_good = False
    
    print("=" * 50)
    if all_good:
        print("🎉 环境配置完成！可以开始量化开发了。")
    else:
        print("⚠️  环境存在一些问题，请检查上述错误信息。")

if __name__ == "__main__":
    main()