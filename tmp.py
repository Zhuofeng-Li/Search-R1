import psutil

port = 8091
for conn in psutil.net_connections(kind='tcp'):
    if conn.laddr.port == port:
        pid = conn.pid
        print(f"Found process with PID {pid} occupying port {port}")
        process = psutil.Process(pid)
        process.kill()
        print(f"Terminated process with PID {pid}")
