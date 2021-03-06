import sys
import atexit
import paramiko
from scp import SCPClient
# import scpclient
# from contextlib import closing

# ssh -o ProxyCommand="ssh -W %h:%p -q root@10.251.139.76" root@10.251.140.160
# https://www.programcreek.com/python/example/52881/paramiko.ProxyCommand
# https://github.com/paramiko/paramiko/issues/903
# https://adimian.com/blog/2014/10/paramiko-and-corporate-proxies/

# https://blog.csdn.net/huithe/article/details/7484606
# https://blog.csdn.net/yiifaa/article/details/78068962
# https://allenwind.github.io/2018/01/17/Python%E7%A8%8B%E5%BA%8F%E9%80%80%E5%87%BA%E6%97%B6%E7%9A%84%E5%9B%9E%E8%B0%83/

class SClient(object):
    
    def __init__(self, host, port, user, password, proxy):
        # paramiko.util.log_to_file(SSH_LOG_PATH)
        self.host=host
        self.port=port
        self.user=user
        self.pwd=password
        self.proxy = proxy
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._connected = False

    def connect(self):
        sock = None
        if isinstance(self.proxy, SClient):
            sock = self.proxy.open_channel(self)
        try:
            self.client.connect(hostname=self.host, port=self.port, username=self.user, password=self.pwd, sock=sock)
            self._connected = True
        except Exception as e:
            pass
        finally:
            atexit.register(self._close)
                
    def exec(self, cmds):
        '''
            ssh登录远程主机并执行命令
        '''
        if not self._connected:
            self.connect()
        try:
            rst = []
            if isinstance(cmds, list):
                for command in cmds:
                    _, stdout, stderr = self.client.exec_command(command)
                    print(stdout.read().decode("utf-8"))
                    # rst.append({"stdout": stdout, "stderr": stderr})
            else:
                _, stdout, stderr = self.client.exec_command(cmds)
                print(stdout.read().decode("utf-8"))
                # rst.append({"stdout": stdout, "stderr": stderr})
        except Exception as e:
            pass
        finally:
            return rst
            
    def put(self, files, remote_path=b'.', isDir=False):
        '''
            上传文件或者目录到远程主机
        '''
        if not self._connected:
            self.connect()
        try:
            with SCPClient(self.client.get_transport(), progress=progress) as scp:
                scp.put(files, remote_path, recursive=isDir)
        except Exception as e:
            pass
            
    def get(self, remote_path, local_path='', isDir=False,):
        '''
            从远程主机下载文件或者目录到本地
        '''
        if not self._connected:
            self.connect()
        try:
            with SCPClient(self.client.get_transport(), progress=progress) as scp:
                scp.get(remote_path, local_path, recursive=isDir)
        except Exception as e:
            pass

    def _close(self):
        self.client.close()

    def open_channel(self, host):
        sock = None
        if host:
            if not self._connected:
                self.connect()
            dest_addr = (host.host, host.port)
            local_addr = (self.host, self.port)
            transport = self.client.get_transport()
            sock = transport.open_channel("direct-tcpip", dest_addr, local_addr)

        return sock

def progress(filename, size, sent):
    sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100))

