#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML转图片工具 - GUI版本
支持批量将HTML文件转换为PNG和JPEG格式的图片
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import scrolledtext
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time
import glob

class HTMLToImageConverter:
    def __init__(self, log_callback=None):
        """初始化转换器"""
        self.driver = None
        self.log_callback = log_callback
        self.setup_driver()
    
    def log(self, message):
        """输出日志信息"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
    
    def setup_driver(self):
        """设置Chrome浏览器驱动"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 无头模式
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--force-device-scale-factor=1')
            
            self.log("正在初始化浏览器驱动...")
            
            # 尝试使用系统已安装的Chrome
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                self.log("✅ 使用系统Chrome浏览器初始化成功！")
                return
            except Exception as e1:
                self.log(f"⚠️  系统Chrome初始化失败，尝试自动下载驱动...")
            
            # 备用方案：自动下载ChromeDriver
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.log("✅ 自动下载ChromeDriver成功！")
                return
            except Exception as e2:
                self.log(f"⚠️  自动下载ChromeDriver失败，尝试Edge浏览器...")
                
            # 最后尝试：使用Edge浏览器
            try:
                from selenium.webdriver.edge.service import Service as EdgeService
                from selenium.webdriver.edge.options import Options as EdgeOptions
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                
                edge_options = EdgeOptions()
                edge_options.add_argument('--headless')
                edge_options.add_argument('--no-sandbox')
                edge_options.add_argument('--disable-dev-shm-usage')
                edge_options.add_argument('--disable-gpu')
                edge_options.add_argument('--window-size=1920,1080')
                edge_options.add_argument('--force-device-scale-factor=1')
                
                edge_service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=edge_service, options=edge_options)
                self.log("✅ Edge浏览器初始化成功！")
                return
            except Exception as e3:
                self.log(f"⚠️  Edge浏览器初始化失败: {e3}")
            
            raise Exception("所有浏览器驱动初始化都失败了")
            
        except Exception as e:
            error_msg = f"❌ 浏览器驱动初始化失败: {e}\n\n💡 解决建议:\n1. 确保已安装Chrome或Edge浏览器\n2. 检查网络连接（需要下载驱动）\n3. 尝试以管理员权限运行\n4. 检查防火墙设置"
            self.log(error_msg)
            raise Exception(error_msg)
    
    def convert_html_to_image(self, html_file_path, output_path, image_format='PNG', width=1920, height=1080):
        """
        将HTML文件转换为图片
        
        参数:
        html_file_path: HTML文件路径
        output_path: 输出图片路径
        image_format: 图片格式 ('PNG' 或 'JPEG')
        width: 图片宽度
        height: 图片高度
        """
        try:
            # 检查HTML文件是否存在
            if not os.path.exists(html_file_path):
                raise FileNotFoundError(f"HTML文件不存在: {html_file_path}")
            
            # 设置窗口大小
            self.driver.set_window_size(width, height)
            self.log(f"📐 设置窗口尺寸: {width}x{height}")
            
            # 加载HTML文件
            file_url = f"file:///{os.path.abspath(html_file_path).replace(os.sep, '/')}"
            self.log(f"📄 正在处理: {os.path.basename(html_file_path)}")
            self.driver.get(file_url)
            
            # 等待页面加载完成
            time.sleep(3)
            
            # 执行JavaScript确保页面完全加载
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # 获取页面的实际高度并调整窗口
            try:
                total_height = self.driver.execute_script(
                    "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
                    "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
                    "document.documentElement.offsetHeight);"
                )
                if total_height > height:
                    self.driver.set_window_size(width, total_height)
                    self.log(f"📏 自适应高度调整为: {width}x{total_height}")
                    time.sleep(2)
            except Exception:
                # 如果获取高度失败，使用默认高度
                pass
            
            # 截图
            self.log("📸 正在生成截图...")
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            if image_format.upper() == 'JPEG':
                # 先截图为PNG，然后转换为JPEG
                temp_png = output_path.replace('.jpg', '_temp.png').replace('.jpeg', '_temp.png')
                self.driver.save_screenshot(temp_png)
                self.convert_png_to_jpeg(temp_png, output_path)
                # 删除临时PNG文件
                if os.path.exists(temp_png):
                    os.remove(temp_png)
            else:
                # 直接保存为PNG
                if not output_path.lower().endswith('.png'):
                    output_path += '.png'
                self.driver.save_screenshot(output_path)
            
            self.log(f"✅ 转换完成: {os.path.basename(output_path)}")
            return True
            
        except Exception as e:
            self.log(f"❌ 转换失败 {os.path.basename(html_file_path)}: {str(e)}")
            return False
    
    def convert_png_to_jpeg(self, png_path, jpeg_path, quality=95):
        """
        将PNG图片转换为JPEG格式
        
        参数:
        png_path: PNG文件路径
        jpeg_path: JPEG输出路径
        quality: JPEG质量 (1-100)
        """
        try:
            with Image.open(png_path) as img:
                # 如果图片有透明通道，需要转换为RGB
                if img.mode in ('RGBA', 'LA', 'P'):
                    # 创建白色背景
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                img.save(jpeg_path, 'JPEG', quality=quality)
        except Exception as e:
            self.log(f"PNG转JPEG失败: {e}")
    
    def batch_convert(self, html_files, output_dir, image_format='PNG', width=1920, height=1080, progress_callback=None):
        """
        批量转换HTML文件
        
        参数:
        html_files: HTML文件列表
        output_dir: 输出目录
        image_format: 图片格式
        width: 图片宽度
        height: 图片高度
        progress_callback: 进度回调函数
        """
        success_count = 0
        total_count = len(html_files)
        
        self.log(f"🚀 开始批量转换，共 {total_count} 个文件")
        
        for i, html_file in enumerate(html_files, 1):
            self.log(f"\n📋 进度: {i}/{total_count}")
            
            # 生成输出文件名
            base_name = os.path.splitext(os.path.basename(html_file))[0]
            if image_format.upper() == 'JPEG':
                output_file = os.path.join(output_dir, f"{base_name}.jpg")
            else:
                output_file = os.path.join(output_dir, f"{base_name}.png")
            
            # 转换文件
            if self.convert_html_to_image(html_file, output_file, image_format, width, height):
                success_count += 1
            
            # 更新进度条
            if progress_callback:
                progress_callback(i)
        
        self.log(f"\n🎉 批量转换完成！成功: {success_count}/{total_count}")
        return success_count, total_count
    
    def close(self):
        """关闭浏览器驱动"""
        if self.driver:
            self.driver.quit()
            self.log("浏览器驱动已关闭")

class HTMLToImageGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HTML转图片工具 - 批量处理版")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置窗口图标和样式
        self.root.configure(bg='#f0f0f0')
        
        # 变量
        self.html_files = []
        self.output_dir = tk.StringVar()
        self.image_format = tk.StringVar(value="PNG")
        self.width = tk.StringVar(value="1920")
        self.height = tk.StringVar(value="1080")
        self.converter = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主标题
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = ttk.Label(title_frame, text="🎨 HTML转图片工具", 
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="批量将HTML文件转换为PNG/JPEG图片 (支持自定义尺寸)", 
                                  font=('Microsoft YaHei', 10))
        subtitle_label.pack()
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(self.root, text="📁 选择HTML文件", padding=10)
        file_frame.pack(fill='x', padx=20, pady=10)
        
        # 文件选择按钮
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text="选择HTML文件", command=self.select_files).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="选择文件夹", command=self.select_folder).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="清空列表", command=self.clear_files).pack(side='left', padx=5)
        
        # 文件列表
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill='both', expand=True, pady=5)
        
        self.file_listbox = tk.Listbox(list_frame, height=8, font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 输出设置区域
        output_frame = ttk.LabelFrame(self.root, text="⚙️ 输出设置", padding=10)
        output_frame.pack(fill='x', padx=20, pady=10)
        
        # 输出目录
        dir_frame = ttk.Frame(output_frame)
        dir_frame.pack(fill='x', pady=5)
        
        ttk.Label(dir_frame, text="输出目录:").pack(side='left')
        ttk.Entry(dir_frame, textvariable=self.output_dir, width=50).pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(dir_frame, text="浏览", command=self.select_output_dir).pack(side='right')
        
        # 图片格式
        format_frame = ttk.Frame(output_frame)
        format_frame.pack(fill='x', pady=5)
        
        ttk.Label(format_frame, text="图片格式:").pack(side='left')
        ttk.Radiobutton(format_frame, text="PNG", variable=self.image_format, value="PNG").pack(side='left', padx=10)
        ttk.Radiobutton(format_frame, text="JPEG", variable=self.image_format, value="JPEG").pack(side='left', padx=10)
        
        # 图片尺寸
        size_frame = ttk.Frame(output_frame)
        size_frame.pack(fill='x', pady=5)
        
        ttk.Label(size_frame, text="图片尺寸:").pack(side='left')
        ttk.Label(size_frame, text="宽度:").pack(side='left', padx=(20, 5))
        width_entry = ttk.Entry(size_frame, textvariable=self.width, width=8)
        width_entry.pack(side='left', padx=5)
        ttk.Label(size_frame, text="高度:").pack(side='left', padx=(10, 5))
        height_entry = ttk.Entry(size_frame, textvariable=self.height, width=8)
        height_entry.pack(side='left', padx=5)
        ttk.Label(size_frame, text="像素").pack(side='left', padx=(5, 0))
        
        # 转换按钮
        convert_frame = ttk.Frame(self.root)
        convert_frame.pack(fill='x', padx=20, pady=10)
        
        self.convert_btn = ttk.Button(convert_frame, text="🚀 开始转换", command=self.start_conversion)
        self.convert_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(convert_frame, text="⏹️ 停止转换", command=self.stop_conversion, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        # 进度条
        self.progress = ttk.Progressbar(convert_frame, mode='determinate')
        self.progress.pack(side='right', fill='x', expand=True, padx=10)
        
        # 日志区域
        log_frame = ttk.LabelFrame(self.root, text="📋 转换日志", padding=10)
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken')
        status_bar.pack(fill='x', side='bottom')
        
    def log_message(self, message):
        """添加日志消息"""
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.root.update_idletasks()
        
    def select_files(self):
        """选择HTML文件"""
        files = filedialog.askopenfilenames(
            title="选择HTML文件",
            filetypes=[("HTML文件", "*.html *.htm"), ("所有文件", "*.*")]
        )
        
        for file in files:
            if file not in self.html_files:
                self.html_files.append(file)
                self.file_listbox.insert('end', os.path.basename(file))
        
        self.update_status()
        
    def select_folder(self):
        """选择包含HTML文件的文件夹"""
        folder = filedialog.askdirectory(title="选择包含HTML文件的文件夹")
        if folder:
            html_files = glob.glob(os.path.join(folder, "*.html")) + glob.glob(os.path.join(folder, "*.htm"))
            
            for file in html_files:
                if file not in self.html_files:
                    self.html_files.append(file)
                    self.file_listbox.insert('end', os.path.basename(file))
            
            self.update_status()
            
    def clear_files(self):
        """清空文件列表"""
        self.html_files.clear()
        self.file_listbox.delete(0, 'end')
        self.update_status()
        
    def select_output_dir(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir.set(directory)
            
    def update_status(self):
        """更新状态栏"""
        count = len(self.html_files)
        if count == 0:
            self.status_var.set("就绪 - 请选择HTML文件")
        else:
            self.status_var.set(f"已选择 {count} 个HTML文件")
            
    def start_conversion(self):
        """开始转换"""
        if not self.html_files:
            messagebox.showwarning("警告", "请先选择HTML文件！")
            return
            
        if not self.output_dir.get():
            messagebox.showwarning("警告", "请选择输出目录！")
            return
            
        # 验证尺寸输入
        try:
            width = int(self.width.get())
            height = int(self.height.get())
            if width <= 0 or height <= 0:
                raise ValueError("尺寸必须大于0")
            if width > 10000 or height > 10000:
                raise ValueError("尺寸不能超过10000像素")
        except ValueError as e:
            messagebox.showerror("错误", f"图片尺寸输入无效：{e}\n请输入有效的数字（1-10000）")
            return
            
        # 禁用转换按钮，启用停止按钮
        self.convert_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        
        # 清空日志
        self.log_text.delete(1.0, 'end')
        
        # 在新线程中执行转换
        self.conversion_thread = threading.Thread(target=self.run_conversion)
        self.conversion_thread.daemon = True
        self.conversion_thread.start()
        
    def run_conversion(self):
        """执行转换任务"""
        try:
            # 创建转换器
            self.converter = HTMLToImageConverter(log_callback=self.log_message)
            
            # 设置进度条
            self.progress.config(maximum=len(self.html_files), value=0)
            
            # 获取尺寸参数
            width = int(self.width.get())
            height = int(self.height.get())
            
            # 批量转换
            success_count, total_count = self.converter.batch_convert(
                self.html_files, 
                self.output_dir.get(), 
                self.image_format.get(),
                width,
                height,
                progress_callback=lambda i: self.progress.config(value=i)
            )
            
            # 显示结果
            if success_count == total_count:
                messagebox.showinfo("完成", f"转换完成！\n成功转换 {success_count} 个文件")
            else:
                messagebox.showwarning("部分完成", f"转换完成！\n成功: {success_count}/{total_count}")
                
        except Exception as e:
            messagebox.showerror("错误", f"转换过程中发生错误:\n{str(e)}")
            
        finally:
            # 关闭转换器
            if self.converter:
                self.converter.close()
                
            # 恢复按钮状态
            self.convert_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.progress.config(value=0)
            
    def stop_conversion(self):
        """停止转换"""
        if self.converter:
            self.converter.close()
        self.log_message("⏹️ 用户停止了转换")
        
    def run(self):
        """运行GUI"""
        self.log_message("🎉 HTML转图片工具已启动！")
        self.log_message("📝 使用说明:")
        self.log_message("1. 选择要转换的HTML文件或文件夹")
        self.log_message("2. 选择输出目录")
        self.log_message("3. 选择图片格式 (PNG/JPEG)")
        self.log_message("4. 设置图片尺寸 (宽度x高度)")
        self.log_message("5. 点击'开始转换'")
        self.log_message("6. 支持自适应高度调整")
        self.log_message("")
        
        self.root.mainloop()

def main():
    """主函数"""
    try:
        app = HTMLToImageGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("启动错误", f"程序启动失败:\n{str(e)}")

if __name__ == "__main__":
    main()