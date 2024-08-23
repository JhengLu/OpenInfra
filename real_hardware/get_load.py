import paramiko
import time

def get_cpu_info(ssh):
    # Command to read CPU utilization from /proc/stat
    command = "cat /proc/stat | grep '^cpu '"
    stdin, stdout, stderr = ssh.exec_command(command)
    cpu_line = stdout.read().decode('utf-8').strip()
    return cpu_line

def calculate_cpu_usage(prev_idle, prev_total, cpu_line):
    cpu_values = list(map(int, cpu_line.split()[1:]))
    idle = cpu_values[3]
    total = sum(cpu_values)

    diff_idle = idle - prev_idle
    diff_total = total - prev_total
    cpu_usage = (100 * (diff_total - diff_idle) / diff_total)

    return cpu_usage, idle, total

def get_cpu_utilization():
    # SSH configuration
    hostname = "130.127.133.204"
    port = 22
    username = "jhlu"
    key_file = "/Users/veritas/.ssh/id_rsa"

    # Create an SSH key object
    ssh_key = paramiko.RSAKey.from_private_key_file(key_file)

    # Connect to the remote machine
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, pkey=ssh_key)

    prev_idle, prev_total = 0, 0

    try:
        while True:
            cpu_line = get_cpu_info(ssh)
            cpu_usage, prev_idle, prev_total = calculate_cpu_usage(prev_idle, prev_total, cpu_line)
            print(f"CPU Utilization: {cpu_usage:.2f}%")
            time.sleep(1)
    finally:
        ssh.close()

if __name__ == "__main__":
    get_cpu_utilization()

