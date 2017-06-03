import paramiko as paramiko
import select
from parse_workers import create_ssh_commands


spec="/Users/Nassim/Desktop/tfworkers"


def send_command(user, host, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, username=user)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command,get_pty=True)
    while not ssh_stdout.channel.exit_status_ready():
        # Only print data if there is data to read in the channel
        if ssh_stdout.channel.recv_ready():
            rl, wl, xl = select.select([ssh_stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                tmp = ssh_stdout.channel.recv(1024)
                output = tmp.decode()
                print(output)

def start_execution(spec, start_port, a3c_dir, log_dir, env_id):
    ssh_commands = create_ssh_commands(spec,start_port, a3c_dir, log_dir, env_id)
    for i in ssh_commands:
        user = i[0]
        host = i[1]
        command = i[2]
        send_command(user,host,command)

#send_command('Nassim','mini',"echo $PATH;tmux new-session -s a3c -n w-0 bash")