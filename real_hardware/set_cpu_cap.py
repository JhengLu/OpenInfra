import paramiko

def set_file_content(ssh, file_path, new_content):
    """
    Change the content of a file on a remote machine.

    Parameters:
    - ssh: The active paramiko SSH connection.
    - file_path: The path to the file on the remote machine.
    - new_content: The content to write to the file.
    """
    command = f"echo '{new_content}' | sudo tee {file_path}"
    stdin, stdout, stderr = ssh.exec_command(command)
    # Read stdout to ensure the command was executed
    output = stdout.read().decode('utf-8').strip()
    error = stderr.read().decode('utf-8').strip()

    if error:
        print(f"Error writing to file: {error}")
    else:
        print(f"File {file_path} updated successfully with content: {new_content}")

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("130.127.133.204", username="jhlu", pkey=paramiko.RSAKey.from_private_key_file("/Users/veritas/.ssh/id_rsa"))

    try:
        # Example usage: change the content of the file to "max 200000"
        set_file_content(ssh, "/users/jhlu/cg_test/cg1/cpu.max", "500000 100000")

    finally:
        ssh.close()

if __name__ == "__main__":
    main()
