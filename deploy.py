'''
Created by Tingkai Liu on Aug 22, 2022
'''


import subprocess
import os

''' TODO: Fill the fields below '''

# The absolute path of Ray library
RAY_PATH = "/home/zhongbozhu/.conda/envs/cloud_burst_ray/lib/python3.9/site-packages/ray"

# The compute node name to IP mapping
SLURM_IP_LOOKUP = """{
    "hal01" : "192.168.20.1",
    "hal02" : "192.168.20.2",
    "hal03" : "192.168.20.3",
    "hal04" : "192.168.20.4",
    "hal05" : "192.168.20.5",
    "hal06" : "192.168.20.6",
    "hal07" : "192.168.20.7",
    "hal08" : "192.168.20.8",
    "hal09" : "192.168.20.9",
    "hal10" : "192.168.20.10",
    "hal11" : "192.168.20.11",
    "hal12" : "192.168.20.12",
    "hal13" : "192.168.20.13",
    "hal14" : "192.168.20.14",
    "hal15" : "192.168.20.15",
    "hal16" : "192.168.20.16",
}"""

MAX_SLURM_JOB_TIME = "01:30:00"

HEAD_NODE_CPUS = "0"
HEAD_NODE_GPUS = "0"
WORKER_NODE_CPUS = "1"
WORKER_NODE_GPUS = "0"

''' End of fields to be filled '''


if __name__ == "__main__":
    
    # Sanity check of Ray path
    while RAY_PATH.endswith('/'):
        RAY_PATH = RAY_PATH[:-1]

    RAY_SLURM_PATH = RAY_PATH + "/autoscaler/_private/slurm"
    TEMPLATE_PATH = RAY_SLURM_PATH + "/template"
    
    if not os.path.exists(RAY_PATH):
        print("Ray path is not vaild. Please fill the fields in deploy.py correctly")
        exit(0)

    if os.path.exists(RAY_SLURM_PATH):
        ans = input("Ray-SLURM packages already exist. Overwrite? [y/n]: ")
        if ans != 'y':
            print("Exited")
            exit(0)

    os.makedirs(RAY_SLURM_PATH, exist_ok=True)
    os.makedirs(TEMPLATE_PATH, exist_ok=True)

    # Copy the files that don't need to be modified
    subprocess.run([
        "cp", 
        "slurm/empty_command_runner.py",
        "slurm/node_provider.py",
        "slurm/slurm_commands.py",
        RAY_SLURM_PATH
    ])

    subprocess.run(["cp", "slurm/template/end_head.sh", TEMPLATE_PATH])

    # Fill and copy __init__ file 
    with open("slurm/__init__.py", "r") as f:
        init = f.read()
    init = init.replace("[_DEPLOY_SLURM_IP_LOOKUP_] ", SLURM_IP_LOOKUP)
    with open(RAY_SLURM_PATH + "/__init__.py", "w") as f:
        f.write(init)

    # Fill and copy bash / Slurm templates
    with open("slurm/template/head.sh", "r") as f:
        template = f.read()
    template = template.replace("[_DEPLOY_HEAD_CPUS_]", HEAD_NODE_CPUS)
    template = template.replace("[_DEPLOY_HEAD_GPUS_]", HEAD_NODE_GPUS)
    with open(TEMPLATE_PATH + "/head.sh", "w") as f:
        f.write(template)
    
    with open("slurm/template/head.slurm", "r") as f:
        template = f.read()
    template = template.replace("[_DEPLOY_HEAD_CPUS_]", HEAD_NODE_CPUS)
    template = template.replace("[_DEPLOY_HEAD_GPUS_]", HEAD_NODE_GPUS)
    template = template.replace("[_DEPLOY_SLURM_JOB_TIME_]", MAX_SLURM_JOB_TIME)
    with open(TEMPLATE_PATH + "/head.slurm", "w") as f:
        f.write(template)
    
    with open("slurm/template/worker.slurm", "r") as f:
        template = f.read()
    template = template.replace("[_DEPLOY_WORKER_CPUS_]", WORKER_NODE_CPUS)
    template = template.replace("[_DEPLOY_WORKER_GPUS_]", WORKER_NODE_GPUS)
    template = template.replace("[_DEPLOY_SLURM_JOB_TIME_]", MAX_SLURM_JOB_TIME)
    with open(TEMPLATE_PATH + "/worker.slurm", "w") as f:
        f.write(template)

    # Fill and generate autoscaler config
    with open("slurm/example-full.yaml", "r") as f:
        template = f.read()
    template = template.replace("[_DEPLOY_RAY_PATH_]", RAY_PATH)
    template = template.replace("[_DEPLOY_RAY_TEMPLATE_PATH_]", TEMPLATE_PATH)
    template = template.replace("[_DEPLOY_HEAD_CPUS_]", HEAD_NODE_CPUS)
    template = template.replace("[_DEPLOY_HEAD_GPUS_]", HEAD_NODE_GPUS)
    template = template.replace("[_DEPLOY_WORKER_CPUS_]", WORKER_NODE_CPUS)
    template = template.replace("[_DEPLOY_WORKER_GPUS_]", WORKER_NODE_GPUS)
    with open("ray-slurm.yaml", "w") as f:
        f.write(template)

    print("Deployment completed")
