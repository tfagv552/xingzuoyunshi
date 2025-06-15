#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HTML转图片工具打包脚本
使用PyInstaller将应用打包为可执行文件
"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """构建可执行文件"""
    print("🚀 开始打包HTML转图片工具...")
    
    # 确保在正确的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 清理之前的构建文件
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            print(f"🧹 清理文件夹: {folder}")
            shutil.rmtree(folder)
    
    # 删除旧的spec文件
    spec_file = 'html_to_image.spec'
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"🗑️ 删除旧的spec文件: {spec_file}")
    
    # PyInstaller命令参数
    cmd = [
        'pyinstaller',
        '--onefile',                    # 打包成单个文件
        '--windowed',                   # 无控制台窗口
        '--name=HTML转图片工具',         # 可执行文件名称
        '--icon=NONE',                  # 暂时不设置图标
        '--add-data=example.html;.',    # 包含示例文件
        '--hidden-import=selenium',     # 确保selenium被包含
        '--hidden-import=PIL',          # 确保PIL被包含
        '--hidden-import=webdriver_manager',  # 确保webdriver_manager被包含
        '--collect-all=selenium',       # 收集所有selenium相关文件
        '--collect-all=webdriver_manager',  # 收集所有webdriver_manager相关文件
        'html_to_image.py'             # 主脚本
    ]
    
    print("📦 执行打包命令...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 打包成功！")
        
        # 检查输出文件
        exe_path = os.path.join('dist', 'HTML转图片工具.exe')
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"📁 可执行文件位置: {exe_path}")
            print(f"📊 文件大小: {file_size:.1f} MB")
            
            # 创建发布文件夹
            release_dir = 'release'
            if not os.path.exists(release_dir):
                os.makedirs(release_dir)
            
            # 复制可执行文件到发布文件夹
            release_exe = os.path.join(release_dir, 'HTML转图片工具.exe')
            shutil.copy2(exe_path, release_exe)
            
            # 复制示例文件
            if os.path.exists('example.html'):
                shutil.copy2('example.html', os.path.join(release_dir, 'example.html'))
            
            # 创建使用说明
            readme_content = """# HTML转图片工具 - 使用说明

## 🎯 功能特性
- 批量将HTML文件转换为PNG/JPEG图片
- 支持自定义图片尺寸
- 现代化GUI界面
- 实时转换进度显示
- 自适应页面高度

## 🚀 使用方法
1. 双击运行 `HTML转图片工具.exe`
2. 选择要转换的HTML文件或文件夹
3. 设置输出目录和图片格式
4. 自定义图片尺寸（默认1920x1080）
5. 点击"开始转换"按钮

## 📝 注意事项
- 首次运行可能需要下载浏览器驱动，请确保网络连接正常
- 建议以管理员权限运行以避免权限问题
- 支持的HTML文件格式：.html, .htm
- 输出图片格式：PNG, JPEG

## 🔧 系统要求
- Windows 10/11
- 已安装Chrome或Edge浏览器
- 至少2GB可用内存

## 📞 技术支持
如遇问题，请检查：
1. 是否已安装Chrome或Edge浏览器
2. 网络连接是否正常
3. 是否有足够的磁盘空间
4. 防火墙是否阻止了程序运行
"""
            
            with open(os.path.join(release_dir, 'README.txt'), 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"📦 发布包已创建: {release_dir}/")
            print("🎉 打包完成！可以分发给用户使用了。")
            
        else:
            print("❌ 未找到生成的可执行文件")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"❌ 打包过程中发生错误: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = build_executable()
    if success:
        print("\n✨ 打包成功完成！")
        input("按回车键退出...")
    else:
        print("\n💥 打包失败！")
        input("按回车键退出...")
        sys.exit(1)