import os



def parse_cluster_spec(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    splitted_workers = []
    for l in content:
        splitted_workers.append(l.split(':'))
    return splitted_workers


def create_cluster_dict(fname, start_port):
    splitted_workers = parse_cluster_spec(fname)
    dict= {'worker': []}

    for i in splitted_workers:
        port=start_port
        if len(i) > 4:
            user = i[0]
            host = i[1]
            cores = int(i[2])
            py_path= i[3]
            ps = i[4]
            if ps != 'ps':
                raise Exception('An unsuported option was specified in the cluster spec!')
            dict['ps'] = [host+':'+str(port)]
            port+=1
            c_workers=dict['worker']
            for k in range(1,cores):
                c_workers.append(host+':'+str(port))
                port += 1
            dict['worker']=c_workers
        else:
            user = i[0]
            host = i[1]
            cores = int(i[2])
            py_path = i[3]
            c_workers = dict['worker']
            for k in range(0, cores):
                c_workers.append(host + ':' + str(port))
                port += 1
            dict['worker'] = c_workers
    return(dict)



def create_ssh_commands(fname, start_port, a3c_dir, log_dir, env_id):
    splitted_workers = parse_cluster_spec(os.environ["HOME"]+fname)
    base_cmd = "cd "+a3c_dir+"\nkill $( lsof -i:"+str(start_port-1)+"-"+str(start_port+30)+" -t ) > /dev/null 2>&1\ntmux kill-session -t a3c\n"

    commands=[]
    task_i=0
    for i in splitted_workers:
        port=start_port
        if len(i) > 4:
            user= i[0]
            host = i[1]
            cores = int(i[2])
            py_path= i[3]
            ps = i[4]
            if ps != 'ps':
                raise Exception('An unsuported option was specified in the cluster spec!')
            c_commands = base_cmd
            c_commands += "tmux new-session -s a3c -n ps -d bash\n"
            c_task_i = task_i
            for k in range(1,cores):
                c_commands += "tmux new-window -t a3c -n w-"+str(c_task_i)+" bash\n"
                c_task_i += 1
            c_commands += "tmux new-window -t a3c -n htop bash\n"
            c_commands += "sleep 1 \n"
            c_commands += "tmux send-keys -t a3c:ps 'CUDA_VISIBLE_DEVICES= "+py_path+" worker.py --log-dir "+log_dir+" --env-id "+env_id+" --job-name ps' Enter\n"
            for k in range(1,cores):
                c_commands += "tmux send-keys -t a3c:w-"+str(task_i)+" 'CUDA_VISIBLE_DEVICES= " + py_path + " worker.py --log-dir " + log_dir + " --env-id " + env_id + " --job-name worker --task "+str(task_i)+" --remotes 1' Enter\n"
                task_i += 1
            c_commands += "tmux send-keys -t a3c:htop htop Enter\n"
            c_commands += "echo received commands at "+host+"\n"
            commands.append([user,host,c_commands])
            print(host)
            print("\n")
            print(c_commands)
            print("\n")
        else:
            user = i[0]
            host = i[1]
            cores = int(i[2])
            py_path = i[3]
            c_commands = base_cmd
            c_commands += "tmux new-session -s a3c -n w-"+str(task_i)+" -d bash\n"
            task_i+=1
            c_task_i = task_i
            for k in range(1, cores):
                c_commands += "tmux new-window -t a3c -n w-" + str(c_task_i) + " bash\n"
                c_task_i += 1
            c_commands += "tmux new-window -t a3c -n htop bash\n"
            c_commands += "sleep 1 \n"
            task_i-=1
            for k in range(0, cores):
                c_commands += "tmux send-keys -t a3c:w-" + str(task_i) + " 'CUDA_VISIBLE_DEVICES= " + py_path + " worker.py --log-dir " + log_dir + " --env-id " + env_id + " --job-name worker --task " + str(task_i) + " --remotes 1' Enter\n"
                task_i += 1
            c_commands += "tmux send-keys -t a3c:htop htop Enter\n"
            c_commands += "echo received commands at " + host + "\n"
            commands.append([user, host, c_commands])
            print(host)
            print("\n")
            print(c_commands)
            print("\n")
    return(commands)

