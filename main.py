from fastmcp import FastMCP
import platform
import psutil
import socket
import datetime

# Initialize the FastMCP server
# "SysAdmin" is the name that will appear in logs/inspectors
mcp = FastMCP("SysAdmin")

@mcp.tool()
def get_os_info() -> str:
    """
    Get detailed information about the Operating System.
    Returns OS name, release version, and machine architecture.
    """
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()
    
    return (
        f"OS: {system} {release}\n"
        f"Version: {version}\n"
        f"Architecture: {machine}\n"
        f"Processor: {processor}"
    )

@mcp.tool()
def get_cpu_stats() -> str:
    """
    Get current CPU usage and frequency information.
    Returns usage percentage and frequency in Mhz.
    """
    # Get load percentage per core for more detail
    per_core = psutil.cpu_percent(interval=1, percpu=True)
    avg_load = psutil.cpu_percent(interval=None)
    
    # Get frequency
    freq = psutil.cpu_freq()
    freq_str = f"{freq.current:.2f}MHz" if freq else "Unknown"
    
    # Count cores
    cores_physical = psutil.cpu_count(logical=False)
    cores_logical = psutil.cpu_count(logical=True)

    return (
        f"Average CPU Load: {avg_load}%\n"
        f"Per Core Load: {per_core}\n"
        f"Current Frequency: {freq_str}\n"
        f"Physical Cores: {cores_physical}\n"
        f"Logical Cores: {cores_logical}"
    )

@mcp.tool()
def get_memory_stats() -> str:
    """
    Get current RAM (Memory) usage statistics.
    Returns Total, Available, Used, and Percentage of memory.
    """
    mem = psutil.virtual_memory()
    
    # Convert bytes to GB for readability
    total_gb = f"{mem.total / (1024**3):.2f} GB"
    available_gb = f"{mem.available / (1024**3):.2f} GB"
    used_gb = f"{mem.used / (1024**3):.2f} GB"
    
    return (
        f"Total Memory: {total_gb}\n"
        f"Used Memory: {used_gb}\n"
        f"Available Memory: {available_gb}\n"
        f"Memory Usage: {mem.percent}%"
    )

@mcp.tool()
def get_disk_usage(path: str = "/") -> str:
    """
    Get disk usage statistics for a specific path (default is root '/').
    Useful for checking if hard drives are full.
    """
    try:
        usage = psutil.disk_usage(path)
        
        total_gb = f"{usage.total / (1024**3):.2f} GB"
        used_gb = f"{usage.used / (1024**3):.2f} GB"
        free_gb = f"{usage.free / (1024**3):.2f} GB"
        
        return (
            f"Disk Path: {path}\n"
            f"Total Space: {total_gb}\n"
            f"Used Space: {used_gb}\n"
            f"Free Space: {free_gb}\n"
            f"Disk Usage: {usage.percent}%"
        )
    except Exception as e:
        return f"Error checking disk path '{path}': {str(e)}"

@mcp.tool()
def get_boot_time() -> str:
    """
    Get the exact time the system was last booted (started).
    """
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
    return f"System Booted at: {bt.strftime('%Y-%m-%d %H:%M:%S')}"
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)