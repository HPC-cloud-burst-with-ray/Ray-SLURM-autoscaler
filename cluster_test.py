from collections import Counter
import socket
import time
import sys
import ray

redis_password_config = ""

def main():
    if redis_password_config == "":
        raise ValueError("Please provide redis password as argument or set redis_password_config variable")

    # ray.init(address='192.168.1.1:1234')
    # ray.init(address='192.168.20.203:6379')     # do Ray
    # ray.init(address='ray://192.168.1.3:10001') 
    # ray.init(address=auto) 

    ray.init(address="192.168.20.203:6379", _redis_password=redis_password_config)

    # @ray.remote
    # def f():
    #     time.sleep(0.01)
    #     return ray._private.services.get_node_ip_address()

    # # Get a list of the IP addresses of the nodes that have joined the cluster.
    # print(set(ray.get([f.remote() for _ in range(1000)])))


    print('''This cluster consists of
        {} nodes in total and the following resources: \n
        {} 
    '''.format(len(ray.nodes()), ray.cluster_resources()))

    @ray.remote
    def f():
        time.sleep(0.01)
        # Return IP address.
        return socket.gethostbyname(socket.gethostname())

    object_ids = [f.remote() for _ in range(2000)]
    ip_addresses = ray.get(object_ids)

    print('Tasks executed')
    for ip_address, num_tasks in Counter(ip_addresses).items():
        print('    {} tasks on {}'.format(num_tasks, ip_address))

    
if __name__ == "__main__":
    # get redis password from arg list 1st
    print(sys.argv)
    if len(sys.argv) == 2:
        redis_password_config = sys.argv[1]
    main()
