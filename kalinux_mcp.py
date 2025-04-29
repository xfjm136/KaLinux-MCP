import sys
from typing import List, Optional
import subprocess
from fastmcp import FastMCP
import os
import re
import time

# 获取当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 定义临时文件夹和日志文件夹路径
TMP_DIR = os.path.join(BASE_DIR, "tmp")
LOG_DIR = os.path.join(BASE_DIR, "log")

# 创建必要的文件夹
os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# 增加超时时间（以秒为单位）
DEFAULT_TIMEOUT = 600  # 10分钟

# 创建FastMCP实例，启用调试模式和DEBUG级别日志
mcp = FastMCP("kali_mcp", debug=True, log_level="DEBUG", 
               log_file=os.path.join(LOG_DIR, "kali_mcp.log"))

@mcp.tool()
def shell_command(command: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    '''
    执行基本的shell命令
    参数:
        command: 要执行的shell命令
        timeout: 命令执行超时时间（秒）
    返回:
        str: 命令执行的输出或错误信息
    '''
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True, timeout=timeout)
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"命令执行超时（超过{timeout}秒）"
    except subprocess.CalledProcessError as e:
        return f"命令执行错误: {e.stderr}"
    except Exception as e:
        return f"执行过程出现异常: {str(e)}"

@mcp.tool()
def nmap_scan(target: str, nmap_args: List[str] = [], timeout: int = DEFAULT_TIMEOUT) -> str:
    '''
    执行nmap网络扫描
    参数:
        target: 目标主机或网络地址
        nmap_args: nmap命令的额外参数列表，默认为空列表
        timeout: 命令执行超时时间（秒）
    返回:
        str: nmap扫描的结果输出或错误信息
    '''
    # 创建输出文件路径
    timestamp = int(time.time())
    output_file = os.path.join(TMP_DIR, f"nmap_scan_{timestamp}.xml")
    
    command_list = ['nmap', '-oX', output_file] + nmap_args + [target]
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, check=True, timeout=timeout)
        with open(output_file, 'r') as f:
            xml_content = f.read()
        return f"Nmap扫描完成，结果已保存至 {output_file}\n\n{result.stdout}"
    except subprocess.TimeoutExpired:
        return f"Nmap扫描超时（超过{timeout}秒），请检查扫描参数或增加超时时间"
    except Exception as e:
        return f"nmap扫描错误: {str(e)}"

@mcp.tool()
def metasploit_command(msf_command: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    '''
    执行Metasploit命令
    参数:
        msf_command: 要在msfconsole中执行的命令
        timeout: 命令执行超时时间（秒）
    返回:
        str: 命令执行的结果或错误信息
    '''
    try:
        # 构建一个临时的RC文件来运行命令
        timestamp = int(time.time())
        rc_file = os.path.join(TMP_DIR, f"msf_temp_{timestamp}.rc")
        output_file = os.path.join(TMP_DIR, f"msf_output_{timestamp}.txt")
        
        with open(rc_file, "w") as f:
            f.write(f"spool {output_file}\n{msf_command}\nexit\n")
        
        result = subprocess.run(['msfconsole', '-q', '-r', rc_file], 
                               capture_output=True, text=True, timeout=timeout)
        
        # 读取输出文件
        output = "命令输出文件不存在"
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                output = f.read()
                
        return f"Metasploit命令执行完成，输出已保存至 {output_file}\n\n{output}"
    except subprocess.TimeoutExpired:
        return f"Metasploit命令执行超时（超过{timeout}秒）"
    except Exception as e:
        return f"Metasploit命令执行错误: {str(e)}"

@mcp.tool()
def aircrack_ng(interface: str, operation: str, args: List[str] = [], timeout: int = DEFAULT_TIMEOUT) -> str:
    '''
    执行aircrack-ng套件命令
    参数:
        interface: 网络接口名称
        operation: 要执行的操作(monitor, scan, capture, crack)
        args: 额外的参数列表
        timeout: 命令执行超时时间（秒）
    返回:
        str: 命令执行的结果或错误信息
    '''
    try:
        timestamp = int(time.time())
        output_prefix = os.path.join(TMP_DIR, f"aircrack_{operation}_{timestamp}")
        
        if operation == "monitor":
            cmd = ['airmon-ng', 'start', interface] + args
        elif operation == "scan":
            cmd = ['airodump-ng', interface, '-w', output_prefix] + args
        elif operation == "capture":
            cmd = ['aireplay-ng', interface, '-w', output_prefix] + args
        elif operation == "crack":
            # 确保输出文件被指定
            output_file = f"{output_prefix}_cracked.txt"
            has_output = False
            for i, arg in enumerate(args):
                if arg == "-o" or arg == "--output":
                    has_output = True
                    break
            if not has_output:
                args.extend(["-o", output_file])
            cmd = ['aircrack-ng'] + args
        else:
            return f"未知的aircrack-ng操作: {operation}"
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return f"Aircrack-ng {operation} 操作完成，输出已保存至 {output_prefix}* 文件\n\n{result.stdout}"
    except subprocess.TimeoutExpired:
        return f"Aircrack-ng命令执行超时（超过{timeout}秒），请检查参数或增加超时时间"
    except Exception as e:
        return f"Aircrack-ng命令执行错误: {str(e)}"

@mcp.tool()
def burpsuite(action: str = "start") -> str:
    '''
    控制Burp Suite
    参数:
        action: 执行的动作，默认为"start"启动Burp Suite
    返回:
        str: 操作结果
    '''
    try:
        timestamp = int(time.time())
        log_file = os.path.join(LOG_DIR, f"burpsuite_{timestamp}.log")
        
        if action == "start":
            # 后台启动Burp Suite
            with open(log_file, 'w') as f:
                subprocess.Popen(['burpsuite'], stdout=f, stderr=f)
            return f"Burp Suite已在后台启动，日志保存在 {log_file}"
        else:
            return f"未知的Burp Suite操作: {action}"
    except Exception as e:
        return f"Burp Suite操作错误: {str(e)}"

@mcp.tool()
def sqlmap_scan(url: str, sqlmap_args: List[str] = [], timeout: int = DEFAULT_TIMEOUT * 2) -> str:
    '''
    使用sqlmap进行SQL注入扫描
    参数:
        url: 要扫描的目标URL
        sqlmap_args: sqlmap的额外参数
        timeout: 命令执行超时时间（秒），默认为普通超时时间的两倍
    返回:
        str: 扫描结果或错误信息
    '''
    timestamp = int(time.time())
    output_dir = os.path.join(TMP_DIR, f"sqlmap_output_{timestamp}")
    
    # 检查是否已经指定了输出目录
    has_output = False
    for i, arg in enumerate(sqlmap_args):
        if arg == "-o" or arg == "--output-dir":
            has_output = True
            break
    
    if not has_output:
        sqlmap_args.extend(["--output-dir", output_dir])
    
    command_list = ['sqlmap', '-u', url] + sqlmap_args
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, check=True, timeout=timeout)
        return f"SQLMap扫描完成，结果已保存至 {output_dir}\n\n{result.stdout}"
    except subprocess.TimeoutExpired:
        return f"SQLMap扫描超时（超过{timeout}秒），但可能已部分完成。请检查 {output_dir} 目录"
    except Exception as e:
        return f"SQLMap扫描错误: {str(e)}"

@mcp.tool()
def hydra_attack(target: str, service: str, userlist: str, passlist: str, additional_args: List[str] = [], timeout: int = DEFAULT_TIMEOUT * 3) -> str:
    '''
    使用Hydra进行密码破解攻击
    参数:
        target: 目标主机
        service: 服务类型(ssh, ftp, http-post-form等)
        userlist: 用户名列表文件路径
        passlist: 密码列表文件路径
        additional_args: 额外的hydra参数
        timeout: 命令执行超时时间（秒），默认为普通超时时间的三倍
    返回:
        str: 破解结果或错误信息
    '''
    timestamp = int(time.time())
    output_file = os.path.join(TMP_DIR, f"hydra_results_{timestamp}.txt")
    
    # 检查是否已经指定了输出文件
    has_output = False
    for i, arg in enumerate(additional_args):
        if arg == "-o" or arg == "-R":
            has_output = True
            break
    
    if not has_output:
        additional_args.extend(["-o", output_file])
    
    command_list = ['hydra', '-L', userlist, '-P', passlist, target, service] + additional_args
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, check=True, timeout=timeout)
        return f"Hydra密码破解完成，结果已保存至 {output_file}\n\n{result.stdout}"
    except subprocess.TimeoutExpired:
        return f"Hydra命令执行超时（超过{timeout}秒），但可能已部分完成。请检查 {output_file} 文件"
    except Exception as e:
        return f"Hydra破解错误: {str(e)}"

@mcp.tool()
def nikto_scan(target: str, nikto_args: List[str] = [], timeout: int = DEFAULT_TIMEOUT) -> str:
    '''
    使用Nikto进行Web服务器扫描
    参数:
        target: 目标主机或URL
        nikto_args: nikto的额外参数
        timeout: 命令执行超时时间（秒）
    返回:
        str: 扫描结果或错误信息
    '''
    timestamp = int(time.time())
    output_file = os.path.join(TMP_DIR, f"nikto_scan_{timestamp}.txt")
    
    # 检查是否已经指定了输出文件
    has_output = False
    for i, arg in enumerate(nikto_args):
        if arg == "-o" or arg == "-output":
            has_output = True
            break
    
    if not has_output:
        nikto_args.extend(["-o", output_file])
    
    command_list = ['nikto', '-h', target] + nikto_args
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, check=True, timeout=timeout)
        return f"Nikto扫描完成，结果已保存至 {output_file}\n\n{result.stdout}"
    except subprocess.TimeoutExpired:
        return f"Nikto扫描超时（超过{timeout}秒），但可能已部分完成。请检查 {output_file} 文件"
    except Exception as e:
        return f"Nikto扫描错误: {str(e)}"

@mcp.tool()
def wpscan(target: str, wpscan_args: List[str] = [], timeout: int = DEFAULT_TIMEOUT) -> str:
    '''
    使用WPScan对WordPress站点进行扫描
    参数:
        target: 目标WordPress站点URL
        wpscan_args: wpscan的额外参数
        timeout: 命令执行超时时间（秒）
    返回:
        str: 扫描结果或错误信息
    '''
    timestamp = int(time.time())
    output_file = os.path.join(TMP_DIR, f"wpscan_{timestamp}.json")
    
    # 检查是否已经指定了输出文件
    has_output = False
    for i, arg in enumerate(wpscan_args):
        if arg == "-o" or arg == "--output":
            has_output = True
            break
            
    if not has_output:
        wpscan_args.extend(["--output", output_file, "--format", "json"])
    
    command_list = ['wpscan', '--url', target] + wpscan_args
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, check=True, timeout=timeout)
        return f"WPScan扫描完成，结果已保存至 {output_file}\n\n{result.stdout}"
    except subprocess.TimeoutExpired:
        return f"WPScan扫描超时（超过{timeout}秒），但可能已部分完成。请检查 {output_file} 文件"
    except Exception as e:
        return f"WPScan扫描错误: {str(e)}"

@mcp.tool()
def john_crack(password_file: str, wordlist: Optional[str] = None, john_args: List[str] = [], timeout: int = DEFAULT_TIMEOUT * 2) -> str:
    '''
    使用John the Ripper破解密码
    参数:
        password_file: 包含哈希值的文件路径
        wordlist: 词典文件路径(可选)
        john_args: john的额外参数
        timeout: 命令执行超时时间（秒），默认为普通超时时间的两倍
    返回:
        str: 破解结果或错误信息
    '''
    timestamp = int(time.time())
    pot_file = os.path.join(TMP_DIR, f"john_pot_{timestamp}")
    
    command_list = ['john', f"--pot={pot_file}"]
    if wordlist:
        command_list.extend(['--wordlist', wordlist])
    command_list.extend(john_args)
    command_list.append(password_file)
    
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, check=True, timeout=timeout)
        # 尝试读取破解结果
        show_result = subprocess.run(['john', f"--pot={pot_file}", '--show', password_file], 
                                    capture_output=True, text=True)
        return f"John密码破解完成，结果已保存至 {pot_file}\n\n{result.stdout}\n\n破解结果:\n{show_result.stdout}"
    except subprocess.TimeoutExpired:
        # 尝试获取已破解的密码
        try:
            show_result = subprocess.run(['john', f"--pot={pot_file}", '--show', password_file], 
                                       capture_output=True, text=True)
            return f"John密码破解超时（超过{timeout}秒），但可能已部分完成。\n已破解的密码:\n{show_result.stdout}"
        except:
            return f"John密码破解超时（超过{timeout}秒）。可以使用命令 'john --pot={pot_file} --show {password_file}' 查看已破解的密码"
    except Exception as e:
        return f"John密码破解错误: {str(e)}"

if __name__ == '__main__':
    # 启动FastMCP服务器
    # transport="sse": 使用Server-Sent Events作为传输方式
    # port=8010: 服务器监听端口
    # host="0.0.0.0": 允许所有网络接口的连接
    mcp.run(transport="sse", port=8010, host="0.0.0.0")