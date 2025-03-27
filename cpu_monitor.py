import psutil
import time

def monitor_memory_sorted(interval=1):
    print(f"{'PID':<8}{'Process Name':<25}{'Memory (MB)':<15}{'Command'}")
    print("=" * 100)

    processes = sorted(
        psutil.process_iter(attrs=['pid', 'name', 'memory_info']),
        key=lambda p: p.info['memory_info'].rss if p.info['memory_info'] else 0,
        reverse=True  # 按内存降序排序
    )

    for proc in processes[:20]:  # 只显示前 10 个占用最多内存的进程
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            memory = proc.info['memory_info'].rss / (1024 * 1024 * 1024)  # 转换为 MB
            cmd = " ".join(proc.cmdline())  # 获取完整命令

            print(f"{pid:<8}{name:<25}{memory:<15.2f}{cmd}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue  # 跳过已退出或无权限访问的进程

    print("=" * 100)

# 运行监控
monitor_memory_sorted()
