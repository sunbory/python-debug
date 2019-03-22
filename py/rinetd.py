import sclient

Class Rinetd(object):

    def __init__(self):
        self.conf="./rinetd/rinetd.conf"
    
    def set_host(hostname, port, username, password):
        self.host=hostname
        self.port=port
        self.user=username
        self.pwd=password
    
    def gen_config(self, maps):
        f = open(self.conf, 'a')
        blank = " "
        for map in maps:
            f.writelines((blank.join(self.host, map.localport, map.remotehost, map.remoteport) + "\n").encode("utf-8"))
        f.close()
        
    def install(self):
        client = sclient.SClient(self.host, self.port, self.user, self.pwd)
        client.send_dir("./rinetd/", "/home/")
        
        cmds=[
            "cd /home/rinetd",
            "chmod +x *.sh",
            "bash start.sh"
        ]
        client.excute_cmds(cmds)
        client.close()
    
    def uninstall(self):
        client = sclient.SClient(self.host, self.port, self.user, self.pwd)
        cmds=[
            "cd /home/rinetd",
            "chmod +x *.sh",
            "bash stop.sh",
            "cd /home && rm -rf ./rinetd"
        ]
        client.excute_cmds(cmds)
        client.close()
        
