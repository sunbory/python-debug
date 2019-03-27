import atexit
import paramiko
import scpclient
from contextlib import closing
ERR_LOG_PATH = "./results/error.log"
SSH_LOG_PATH = "./results/ssh.log"

# https://blog.csdn.net/huithe/article/details/7484606
# https://blog.csdn.net/yiifaa/article/details/78068962

# https://adimian.com/blog/2014/10/paramiko-and-corporate-proxies/
class SClient(object):
    
    def __init__(self, hostname, port, username, password):
        paramiko.util.log_to_file(SSH_LOG_PATH)
        self.host=host
        self.port=port
        self.user=username
        self.pwd=password
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=hostname, port=port, username=username, password=password, pkey=None,
                      allow_agent=False, look_for_keys=False, compress=False)
        
        atexit.register(self._close)
        # https://allenwind.github.io/2018/01/17/Python%E7%A8%8B%E5%BA%8F%E9%80%80%E5%87%BA%E6%97%B6%E7%9A%84%E5%9B%9E%E8%B0%83/
        
    def excute_cmd(self, command):
    '''
        ssh登录远程主机并执行单条命令
    '''
        try:
            stdin, stdout, stderr = self.client.exec_command(command)    
        except Exception, e:
            print "excute_cmd " + self.host + ":", self.port, "failed, error is ", e
            return         
        return stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
        
    def excute_cmds(self, cmds):
    '''
        ssh登录远程主机并执行一系列命令
    '''
        try:
            f = open(ERR_LOG_PATH, 'a')
            for command in cmds:
                stdin, stdout, stderr = self.client.exec_command(command)
                stdout_str = stdout.read().decode("utf-8")
                stderr_str = stderr.read().decode("utf-8")
                f.writelines((host + " stdout: " + command + stdout_str + "\n").encode("utf-8"))
                f.writelines((host + " stderr: " + command + stderr_str + "\n").encode("utf-8"))
        except Exception, e:
            print "excute_cmds" + self.host + ":", self.port, "failed, error is ", e
        finally:
            f.close()
            
    def send_file(self, local_file, remote_path):
    '''
        上传文件
    '''
        try:
            with closing(scpclient.Write(self.client.get_transport(), remote_path)) as scp:
                scp.send_file(local_file, True, override_mode=True)
        except Exception, e:
            print "ssh or send file to " + self.host + ":", self.port, "failed, error is ", e
            
    def send_dir(self, local_dir, remote_path):
    '''
        上传目录
    '''
        try:
            with closing(scpclient.WriteDir(self.client.get_transport(), remote_path)) as scp:
                scp.send_dir(local_dir, True, override_mode=True)
        except Exception, e:
            print "ssh or send dir to " + self.host + ":", self.port, "failed, error is ", e

    def fetch_file(self, local_file, remote_path):
    '''
        下载文件
    '''
        try:
            with closing(scpclient.Read(self.client.get_transport(), remote_path)) as scp:
                scp.receive_file(local_filename=local_file)
        except Exception, e:
            if e.message == "'module' object has no attribute 'fchmod'":
                return
            print "get_file_from_vm" + self.host + ":", self.port, "failed, error is ", e
    
    def fetch_dir(self, local_dir, remote_dir, remote_path):
    '''
        下载目录
    '''
        try:
            with closing(scpclient.ReadDir(self.client.get_transport(), remote_path)) as scp:
                scp.receive_dir(local_filename=local_dir, remote_filename=remote_dir)
        except Exception, e:
            if e.message == "'module' object has no attribute 'fchmod'":
                return
            print "get_file_from_vm" + self.host + ":", self.port, "failed, error is ", e
            
    def _close(self):
        self.client.close()

