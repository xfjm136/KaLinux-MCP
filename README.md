# Kali Linux Terminal Control MCP

[English](#english) | [中文](#chinese)

<a name="chinese"></a>

# Kali Linux 终端控制 MCP

## 概述

Kali Linux 终端控制 MCP 是一个多通道协议（Multi-Channel Protocol，MCP）实现，它允许通过API方便地访问各种 Kali Linux 安全工具和基本的 Linux 命令。该项目通过标准化的 API 接口，使安全测试和评估过程的自动化变得简单。

## 功能特点

- 执行基本的 Linux shell 命令
- 使用 Nmap 进行网络扫描
- 执行 Metasploit 命令
- 使用 Aircrack-ng 无线工具
- 启动和控制 Burp Suite
- 使用 SQLMap 进行 SQL 注入扫描
- 使用 Hydra 进行密码破解
- 使用 Nikto 进行 Web 服务器扫描
- 使用 WPScan 分析 WordPress 站点
- 使用 John the Ripper 破解密码

## 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/xfjm136/KaLinux-MCP.git
   cd KaLinux-MCP
   ```

2. 安装依赖：
   ```bash
   pip install fastmcp
   ```

3. 确保你已安装 Kali Linux 以及必要的安全工具。

## 使用方法

1. 启动 MCP 服务器：
   ```bash
   python kalinux_mcp.py
   ```

2. 服务器默认会在 8010 端口启动，使用 Server-Sent Events (SSE) 作为传输协议。

3. 从你的客户端应用程序连接到 MCP 服务器以调用各种工具。

## 文件结构

- `tmp/`: 临时文件和命令输出的目录
- `log/`: 日志文件目录
- 这两个目录会在脚本所在位置自动创建

## API 参考

### Shell 命令

执行基本的 shell 命令：

```python
shell_command(command: str, timeout: int = 600) -> str
```

### Nmap 扫描

使用 Nmap 进行网络扫描：

```python
nmap_scan(target: str, nmap_args: List[str] = [], timeout: int = 600) -> str
```

### Metasploit 命令

在 Metasploit 框架中执行命令：

```python
metasploit_command(msf_command: str, timeout: int = 600) -> str
```

### Aircrack-ng

使用 Aircrack-ng 进行无线网络操作：

```python
aircrack_ng(interface: str, operation: str, args: List[str] = [], timeout: int = 600) -> str
```

### Burp Suite

控制 Burp Suite：

```python
burpsuite(action: str = "start") -> str
```

### SQLMap 扫描

进行 SQL 注入扫描：

```python
sqlmap_scan(url: str, sqlmap_args: List[str] = [], timeout: int = 1200) -> str
```

### Hydra 攻击

进行密码破解攻击：

```python
hydra_attack(target: str, service: str, userlist: str, passlist: str, additional_args: List[str] = [], timeout: int = 1800) -> str
```

### Nikto 扫描

扫描 Web 服务器漏洞：

```python
nikto_scan(target: str, nikto_args: List[str] = [], timeout: int = 600) -> str
```

### WPScan

扫描 WordPress 站点：

```python
wpscan(target: str, wpscan_args: List[str] = [], timeout: int = 600) -> str
```

### John the Ripper

破解密码：

```python
john_crack(password_file: str, wordlist: Optional[str] = None, john_args: List[str] = [], timeout: int = 1200) -> str
```

## 配置

- 命令的默认超时时间设置为 600 秒（10 分钟）
- 对于密码破解等密集型操作，超时时间默认增加
- 所有输出文件保存到 `tmp/` 目录，使用基于时间戳的命名
- 日志文件保存到 `log/` 目录

## 示例代码

```python
from fastmcp import FastMCPClient

# 连接到 MCP 服务器
client = FastMCPClient("http://localhost:8010/sse")

# 运行简单的 Nmap 扫描
result = client.call("nmap_scan", {"target": "192.168.1.1", "nmap_args": ["-p", "1-1000"]})
print(result)

# 执行 Metasploit 命令
result = client.call("metasploit_command", {"msf_command": "use auxiliary/scanner/ssh/ssh_login"})
print(result)
```
---

<a name="english"></a>

## Overview

Kali Linux Terminal Control MCP is a Multi-Channel Protocol (MCP) implementation that allows convenient API access to various Kali Linux security tools and basic Linux commands. This project enables easy automation of security testing and assessment processes through a standardized API interface.

## Features

- Execute basic Linux shell commands
- Run network scanning with Nmap
- Execute Metasploit commands
- Utilize Aircrack-ng wireless tools
- Launch and control Burp Suite
- Perform SQL injection scanning with SQLMap
- Conduct password cracking with Hydra
- Execute web server scanning with Nikto
- Analyze WordPress sites with WPScan
- Crack passwords with John the Ripper

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/xfjm136/KaLinux-MCP.git
   cd KaLinux-MCP
   ```

2. Install dependencies:
   ```bash
   pip install fastmcp
   ```

3. Ensure you have Kali Linux with the necessary security tools installed.

## Usage

1. Start the MCP server:
   ```bash
   python kalinux_mcp.py
   ```

2. The server will start on port 8010 by default, using Server-Sent Events (SSE) as the transport protocol.

3. Connect to the MCP server from your client application to call the various tools.

## File Structure

- `tmp/`: Directory for temporary files and command outputs
- `log/`: Directory for log files
- Both directories are automatically created in the same location as the script

## API Reference

### Shell Command

Execute basic shell commands:

```python
shell_command(command: str, timeout: int = 600) -> str
```

### Nmap Scan

Perform network scanning with Nmap:

```python
nmap_scan(target: str, nmap_args: List[str] = [], timeout: int = 600) -> str
```

### Metasploit Command

Execute commands in the Metasploit Framework:

```python
metasploit_command(msf_command: str, timeout: int = 600) -> str
```

### Aircrack-ng

Use Aircrack-ng for wireless network operations:

```python
aircrack_ng(interface: str, operation: str, args: List[str] = [], timeout: int = 600) -> str
```

### Burp Suite

Control Burp Suite:

```python
burpsuite(action: str = "start") -> str
```

### SQLMap Scan

Perform SQL injection scanning:

```python
sqlmap_scan(url: str, sqlmap_args: List[str] = [], timeout: int = 1200) -> str
```

### Hydra Attack

Conduct password cracking attacks:

```python
hydra_attack(target: str, service: str, userlist: str, passlist: str, additional_args: List[str] = [], timeout: int = 1800) -> str
```

### Nikto Scan

Scan web servers for vulnerabilities:

```python
nikto_scan(target: str, nikto_args: List[str] = [], timeout: int = 600) -> str
```

### WPScan

Scan WordPress sites:

```python
wpscan(target: str, wpscan_args: List[str] = [], timeout: int = 600) -> str
```

### John the Ripper

Crack passwords:

```python
john_crack(password_file: str, wordlist: Optional[str] = None, john_args: List[str] = [], timeout: int = 1200) -> str
```

## Configuration

- Default timeout for commands is set to 600 seconds (10 minutes)
- For intensive operations like password cracking, timeout is increased by default
- All output files are saved to the `tmp/` directory with timestamp-based naming
- Log files are saved to the `log/` directory

## Example Code

```python
from fastmcp import FastMCPClient

# Connect to the MCP server
client = FastMCPClient("http://localhost:8010/sse")

# Run a simple Nmap scan
result = client.call("nmap_scan", {"target": "192.168.1.1", "nmap_args": ["-p", "1-1000"]})
print(result)

# Execute a Metasploit command
result = client.call("metasploit_command", {"msf_command": "use auxiliary/scanner/ssh/ssh_login"})
print(result)
```
---

