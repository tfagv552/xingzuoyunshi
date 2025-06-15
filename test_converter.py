#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化测试脚本
用于测试HTML转图片功能
"""

import os
import sys
from html_to_image import HTMLToImageConverter

def test_conversion():
    """测试HTML转图片功能"""
    print("=== HTML转图片功能测试 ===")
    print()
    
    # 测试文件路径
    html_file = "example.html"
    png_output = "test_output.png"
    jpg_output = "test_output.jpg"
    
    # 检查示例HTML文件是否存在
    if not os.path.exists(html_file):
        print(f"❌ 错误: 找不到示例HTML文件 {html_file}")
        return False
    
    print(f"✅ 找到示例HTML文件: {html_file}")
    
    # 创建转换器
    try:
        converter = HTMLToImageConverter()
        print("✅ 浏览器驱动初始化成功")
    except Exception as e:
        print(f"❌ 浏览器驱动初始化失败: {e}")
        return False
    
    success_count = 0
    total_tests = 2
    
    try:
        # 测试1: 转换为PNG
        print("\n📝 测试1: HTML转PNG")
        if converter.convert_html_to_image(html_file, png_output, 'PNG', 1200, 800):
            if os.path.exists(png_output):
                file_size = os.path.getsize(png_output)
                print(f"✅ PNG转换成功! 文件大小: {file_size} 字节")
                success_count += 1
            else:
                print("❌ PNG文件未生成")
        else:
            print("❌ PNG转换失败")
        
        # 测试2: 转换为JPEG
        print("\n📝 测试2: HTML转JPEG")
        if converter.convert_html_to_image(html_file, jpg_output, 'JPEG', 1200, 800):
            if os.path.exists(jpg_output):
                file_size = os.path.getsize(jpg_output)
                print(f"✅ JPEG转换成功! 文件大小: {file_size} 字节")
                success_count += 1
            else:
                print("❌ JPEG文件未生成")
        else:
            print("❌ JPEG转换失败")
    
    finally:
        # 关闭浏览器
        converter.close()
    
    # 测试结果
    print("\n" + "="*50)
    print(f"测试完成! 成功: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 所有测试通过! HTML转图片工具工作正常!")
        return True
    else:
        print("⚠️  部分测试失败，请检查错误信息")
        return False

def main():
    """主函数"""
    try:
        success = test_conversion()
        
        print("\n📁 生成的文件:")
        for filename in ["test_output.png", "test_output.jpg"]:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"  - {filename} ({size} 字节)")
        
        if success:
            print("\n✨ 测试完成! 您可以查看生成的图片文件。")
            print("\n🚀 现在可以运行 'python html_to_image.py' 开始使用工具!")
        else:
            print("\n❌ 测试失败，请检查环境配置。")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")

if __name__ == "__main__":
    main()