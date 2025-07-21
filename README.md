# MiniZipper

一个Python库，用于创建zip文件，支持标准zip和密码加密zip，确保生成的zip文件可以在Windows、macOS、Linux等所有平台上正常解压。

## 特性

- ✅ **跨平台兼容**：生成的zip文件在所有主流操作系统上都能正常解压
- ✅ **多种加密算法**：支持5种不同的加密算法选择
- ✅ **简单易用**：简洁的API，几行代码即可创建加密zip
- ✅ **无外部依赖**：仅使用Python标准库，无需安装额外包
- ✅ **命令行工具**：提供便捷的命令行界面
- ✅ **批量处理**：支持单个文件、目录或批量文件压缩

## 支持的加密算法

| 算法 | 标识符 | 描述 | 安全性 |
|------|--------|------|--------|
| XOR | `xor` | 简单XOR加密（默认） | 基础 |
| HMAC-SHA256 | `hmac_sha256` | 基于HMAC-SHA256的加密 | 高 |
| AES-Like | `aes_like` | 类AES多轮加密 | 中高 |
| Double XOR | `double_xor` | 双重XOR加密 | 中 |
| Custom Hash | `custom_hash` | 多哈希算法组合加密 | 中高 |

## 安装

```bash
pip install minizipper
```

或者从源码安装：

```bash
git clone https://github.com/a1401358759/minizipper.git
cd minizipper
pip install -e .
```

## 快速开始

### 基本用法

```python
from minizipper import SecureZipper, EncryptionAlgorithm

# 创建zipper实例
zipper = SecureZipper()

# 创建标准zip文件
zipper.create_zip("my_file.txt", "output.zip")

# 创建加密zip文件（使用默认XOR算法）
zipper.setpassword("mypassword123")
zipper.create_zip("my_file.txt", "encrypted.zip")

# 使用特定加密算法
zipper.setpassword("mypassword123", EncryptionAlgorithm.HMAC_SHA256)
zipper.create_zip("my_file.txt", "secure.zip")
```

### 压缩目录

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# 压缩整个目录
zipper.create_zip("my_directory", "archive.zip")

# 包含隐藏文件
zipper.create_zip("my_directory", "archive.zip", include_hidden=True)
```

### 批量文件压缩

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# 压缩多个文件
files = ["file1.txt", "file2.txt", "file3.txt"]
zipper.create_zip_from_files(files, "multiple_files.zip")

# 指定基础目录
zipper.create_zip_from_files(files, "multiple_files.zip", base_dir="/path/to/base")
```

### 解压文件

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# 解压标准zip文件
zipper.extract_zip("archive.zip", "extracted_folder")

# 解压加密zip文件
zipper.setpassword("mypassword123")
zipper.extract_zip("encrypted.zip", "extracted_folder")
```

## 命令行工具

### 基本用法

```bash
# 压缩单个文件
python -m minizipper.cli -s my_file.txt -o output.zip

# 压缩目录
python -m minizipper.cli -s my_directory -o archive.zip

# 压缩多个文件
python -m minizipper.cli -f file1.txt file2.txt file3.txt -o multiple.zip
```

### 加密功能

```bash
# 使用默认算法（XOR）加密
python -m minizipper.cli -s my_file.txt -o encrypted.zip --password mypass123

# 使用特定算法加密
python -m minizipper.cli -s my_file.txt -o secure.zip --password mypass123 --algorithm hmac_sha256

# 查看所有可用算法
python -m minizipper.cli --list-algorithms
```

### 解压功能

```bash
# 解压标准zip文件
python -m minizipper.cli -o archive.zip --extract extracted_folder

# 解压加密zip文件
python -m minizipper.cli -o encrypted.zip --extract extracted_folder --password mypass123
```

### 高级选项

```bash
# 包含隐藏文件
python -m minizipper.cli -s my_directory -o archive.zip --include-hidden

# 设置压缩级别
python -m minizipper.cli -s my_file.txt -o output.zip --compression-level 9

# 测试zip文件
python -m minizipper.cli -s my_file.txt -o test.zip --test

# 详细输出
python -m minizipper.cli -s my_file.txt -o output.zip -v
```

## API 参考

### SecureZipper 类

#### 构造函数

```python
SecureZipper(compression_level: int = 6)
```

- `compression_level`: 压缩级别 (0-9)，默认为6

#### 上下文管理器支持

SecureZipper 支持上下文管理器，可以使用 `with` 语句：

```python
# 使用上下文管理器（推荐）
with SecureZipper() as zipper:
    zipper.setpassword("mypassword123", EncryptionAlgorithm.HMAC_SHA256)
    zipper.create_zip("source_folder", "encrypted.zip")
    # 自动清理敏感数据

# 传统方式
zipper = SecureZipper()
zipper.setpassword("mypassword123")
zipper.create_zip("source_folder", "encrypted.zip")
# 需要手动清理
```

**上下文管理器的优势：**
- 自动清理敏感数据（密码、算法设置）
- 异常处理和日志记录
- 更清晰的代码结构
- 资源管理

#### 主要方法

##### setpassword()

```python
setpassword(password: str, algorithm: EncryptionAlgorithm = EncryptionAlgorithm.XOR)
```

设置加密密码和算法。

- `password`: 加密密码，如果为None或空字符串则禁用加密
- `algorithm`: 加密算法，默认为XOR

##### create_zip()

```python
create_zip(
    source_path: Union[str, Path],
    output_path: Union[str, Path],
    include_hidden: bool = False
) -> str
```

创建zip文件。

- `source_path`: 要压缩的文件或目录路径
- `output_path`: 输出的zip文件路径
- `include_hidden`: 是否包含隐藏文件
- 返回: 创建的zip文件路径

##### create_zip_from_files()

```python
create_zip_from_files(
    file_paths: List[Union[str, Path]],
    output_path: Union[str, Path],
    base_dir: Optional[Union[str, Path]] = None
) -> str
```

从多个文件创建zip文件。

- `file_paths`: 要压缩的文件路径列表
- `output_path`: 输出的zip文件路径
- `base_dir`: 基础目录，用于计算相对路径
- 返回: 创建的zip文件路径

##### extract_zip()

```python
extract_zip(
    zip_path: Union[str, Path],
    extract_path: Union[str, Path]
) -> bool
```

解压zip文件。

- `zip_path`: zip文件路径
- `extract_path`: 解压目标路径
- 返回: 是否解压成功

##### test_zip_extraction()

```python
test_zip_extraction(zip_path: Union[str, Path]) -> bool
```

测试zip文件是否可以正常解压。

- `zip_path`: zip文件路径
- 返回: 是否可以正常解压

### EncryptionAlgorithm 枚举

```python
class EncryptionAlgorithm(Enum):
    XOR = "xor"                    # 简单XOR加密（默认）
    HMAC_SHA256 = "hmac_sha256"    # HMAC-SHA256加密
    AES_LIKE = "aes_like"          # 类AES加密（使用标准库模拟）
    DOUBLE_XOR = "double_xor"      # 双重XOR加密
    CUSTOM_HASH = "custom_hash"    # 自定义哈希加密
```

## 加密算法详解

### 1. XOR (xor)
- **原理**: 简单的异或加密
- **特点**: 速度快，安全性基础
- **适用场景**: 快速加密，对安全性要求不高的场景

### 2. HMAC-SHA256 (hmac_sha256)
- **原理**: 基于HMAC-SHA256的加密，使用随机盐值
- **特点**: 安全性高，每次加密结果不同
- **适用场景**: 高安全性要求的场景

### 3. AES-Like (aes_like)
- **原理**: 模拟AES的多轮加密过程
- **特点**: 中等安全性，使用多轮密钥
- **适用场景**: 平衡安全性和性能的场景

### 4. Double XOR (double_xor)
- **原理**: 双重XOR加密，使用正向和反向密钥
- **特点**: 比单XOR更安全
- **适用场景**: 需要比XOR更高安全性的场景

### 5. Custom Hash (custom_hash)
- **原理**: 结合MD5、SHA1、SHA256三种哈希算法
- **特点**: 多重哈希保护
- **适用场景**: 需要多重保护的场景

## 示例

### 示例1：基本文件压缩

```python
from minizipper import SecureZipper

# 创建zipper
zipper = SecureZipper()

# 压缩单个文件
zipper.create_zip("document.txt", "document.zip")
print("文件压缩完成！")
```

### 示例2：目录压缩

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# 压缩整个项目目录
zipper.create_zip("my_project", "project_backup.zip", include_hidden=True)
print("项目备份完成！")
```

### 示例3：加密压缩

```python
from minizipper import SecureZipper, EncryptionAlgorithm

zipper = SecureZipper()

# 使用HMAC-SHA256算法加密
zipper.setpassword("secure_password_123", EncryptionAlgorithm.HMAC_SHA256)
zipper.create_zip("sensitive_data", "encrypted_backup.zip")
print("敏感数据加密备份完成！")
```

### 示例4：批量文件处理

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# 批量压缩多个文件
files = [
    "report1.pdf",
    "report2.pdf",
    "data.csv",
    "config.json"
]

zipper.create_zip_from_files(files, "reports.zip")
print("批量文件压缩完成！")
```

### 示例5：解压和验证

```python
from minizipper import SecureZipper

zipper = SecureZipper()

# 测试zip文件完整性
if zipper.test_zip_extraction("archive.zip"):
    print("zip文件完整，开始解压...")

    # 解压文件
    if zipper.extract_zip("archive.zip", "extracted_files"):
        print("解压成功！")
    else:
        print("解压失败！")
else:
    print("zip文件损坏！")
```

## 注意事项

1. **密码安全**: 请使用强密码，避免使用简单密码
2. **算法选择**: 根据安全需求选择合适的加密算法
3. **文件大小**: 加密会增加文件大小，特别是HMAC算法
4. **兼容性**: 加密zip文件只能使用本库解压
5. **备份**: 重要文件请做好备份，避免密码丢失

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
