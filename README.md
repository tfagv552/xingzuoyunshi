<<<<<<< HEAD
# HTML转图片工具

一个简单易用的Python工具，可以将HTML文件转换为PNG或JPEG格式的图片。

## 🌟 功能特点

- ✅ 支持HTML文件转换为图片
- ✅ 支持PNG和JPEG两种输出格式
- ✅ 可自定义图片尺寸
- ✅ 自动适应页面高度
- ✅ 高质量渲染，支持CSS样式
- ✅ 简单易用的命令行界面
- ✅ 自动处理浏览器驱动安装

## 📋 系统要求

- Python 3.7 或更高版本
- Windows/macOS/Linux 操作系统
- 网络连接（首次运行时下载Chrome驱动）

## 🚀 安装步骤

### 1. 安装Python依赖

在项目目录下运行以下命令：

```bash
pip install -r requirements.txt
```

### 2. 确保Chrome浏览器已安装

工具使用Chrome浏览器进行HTML渲染，请确保您的系统已安装Chrome浏览器。

## 📖 使用方法

### 基本使用

1. 运行程序：
```bash
python html_to_image.py
```

2. 按照提示输入信息：
   - HTML文件路径
   - 输出图片路径
   - 图片尺寸（可选，默认1920x1080）

### 示例

```
=== HTML转图片工具 ===
支持格式: PNG, JPEG

请输入HTML文件路径: example.html
请输入输出图片路径 (例如: output.png 或 output.jpg): output.png
请输入图片宽度 (默认1920): 1920
请输入图片高度 (默认1080): 1080
```

## 📁 项目文件说明

- `html_to_image.py` - 主程序文件
- `requirements.txt` - Python依赖包列表
- `example.html` - 示例HTML文件
- `README.md` - 使用说明文档

## 🎯 支持的输出格式

### PNG格式
- 支持透明背景
- 无损压缩
- 适合包含透明元素的页面

### JPEG格式
- 较小的文件大小
- 有损压缩
- 透明背景会被转换为白色

## ⚙️ 高级配置

### 自定义图片质量（JPEG）

在代码中可以修改JPEG质量参数（1-100）：

```python
self.convert_png_to_jpeg(screenshot_path, output_path, quality=95)
```

### 自定义浏览器选项

可以在`setup_driver`方法中添加更多Chrome选项：

```python
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--allow-running-insecure-content')
```

## 🔧 故障排除

### 常见问题

1. **Chrome驱动下载失败**
   - 检查网络连接
   - 尝试手动下载ChromeDriver

2. **HTML文件加载失败**
   - 确保文件路径正确
   - 检查HTML文件语法是否正确

3. **图片生成失败**
   - 检查输出目录是否存在写入权限
   - 确保磁盘空间充足

### 错误日志

程序会在控制台输出详细的错误信息，请根据错误信息进行相应的处理。

## 📝 注意事项

1. 首次运行时会自动下载Chrome驱动，需要网络连接
2. 生成的图片大小取决于HTML内容的复杂程度
3. 建议在转换大型HTML文件时预留足够的系统内存
4. 某些动态效果可能需要增加等待时间

## 🤝 技术支持

如果您在使用过程中遇到问题，请检查：

1. Python版本是否符合要求
2. 所有依赖包是否正确安装
3. Chrome浏览器是否已安装
4. HTML文件是否可以在浏览器中正常打开

## 📄 许可证

本项目采用MIT许可证，您可以自由使用、修改和分发。

---

🎉 **开始使用吧！** 运行 `python html_to_image.py` 来转换您的第一个HTML文件！
