import argparse

from execute_ssh import start_execution

parser = argparse.ArgumentParser(description=None)
parser.add_argument('--log-dir', default="/nfs/ASS/exp1", help='Log directory path')
parser.add_argument('--a3c-dir', default='$HOME/Documents/ASS/agent', help='a3c directory path')
parser.add_argument('--start_port', default=12222, help='start port')
parser.add_argument('--cluster_spec', default="/Documents/ASS/agent/tfspec", help='cluster specification file')
parser.add_argument('--env-id', default="PongDeterministic-v3", help='Environment id')
args = parser.parse_args()

log_dir = args.log_dir
a3c_dir = args.a3c_dir
start_port = args.start_port
tfspec = args.cluster_spec
env_id = args.env_id

start_execution(tfspec, start_port, a3c_dir, log_dir, env_id)