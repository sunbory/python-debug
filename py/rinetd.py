import sclient

class Rinetd(object):

    def __init__(self):
        self.conf="./rinetd/rinetd.conf"
    
    def set_host(hostname, port=22, username, password):
        self.host=hostname
        self.port=port
        self.user=username
        self.pwd=password
        self.client=sclient.SClient(self.host, self.port, self.user, self.pwd)
    
    def install(self, targets):  
        # generate configs for rinetd
        f = open(self.conf, 'a')
        tmpport=10000
        blank = " "
        for target in targets:
            f.writelines((blank.join(self.host, tmpport, target["Host"], target["Port"]) + "\n").encode("utf-8"))
            target["pHost"]=self.host
            target["pPort"]=tmpport
            tmpport = tmpport + 1
        f.close()
        
        # start proc in target host
        self.client.send_dir("./rinetd/", "/home/")        
        cmds=[
            "cd /home/rinetd",
            "chmod +x *.sh",
            "bash start.sh"
        ]
        self.client.excute_cmds(cmds)

    def uninstall(self):
        cmds=[
            "cd /home/rinetd",
            "chmod +x *.sh",
            "bash stop.sh",
            "cd /home && rm -rf ./rinetd"
        ]
        self.client.excute_cmds(cmds)

        
