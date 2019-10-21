# -*- coding:utf-8 -*-

import sys
import paramiko
from paramiko import AuthenticationException
import time

class ConnectionError(Exception):
    pass

class ShellHandler:
    def __init__(self, host, port, user, psw, su=None, passwd=None):
        self.su = su
        self.passwd = passwd
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.status = 1
        try:
            self.ssh.connect(host, username=user, password=psw, port=port)
        except AuthenticationException:
            self.status = None
        except Exception as e:
            self.status = None

    def execute(self, cmdlist, file_path):
        channel = self.ssh.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('r')

        if (self.su != None):
            stdin.write(self.su + '\n')
            time.sleep(1)
            stdin.write(self.passwd + '\n')

        f = open(file_path, 'a')
        for cmd in cmdlist:
            cmd = cmd.strip('\n')
            stdin.write('\n\n\n')
            stdin.write(cmd + '\n')
        finish = 'end of stdOUT buffer. finished with exit status 1'
        echo_cmd = 'echo {}'.format(finish)
        stdin.write(echo_cmd + '\n')
        shin = stdin
        stdin.flush()

        shout = []
        sherr = []
        exit_status = 0
        for line in stdout:
            if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
                shout = []
            elif str(line).startswith(finish):
                exit_status = int(str(line).rsplit(None,1)[1])
                if exit_status:
                    sherr = shout
                    shout = []
                break
            elif finish in str(line):
                channel.close()
            else:
                shout.append(line)

        if shout and echo_cmd in shout[-1]:
            shout.pop()
        if shout and cmd in shout[0]:
            shout.pop(0)
        if sherr and echo_cmd in sherr[-1]:
            sherr.pop()
        if sherr and cmd in sherr[0]:
            sherr.pop(0)

        for row in shout:
            f.write(row)
        f.close()
        print("执行结果写至文件：%s" % file_path)

        return shin, shout, sherr

class baseSsh:
    login_status = True
    def __init__(self, ip, port, userName, password):
        self.ip = ip
        self.port = port
        self.userName = userName
        self.password = password



class linuxSsh(baseSsh):
    def __init__(self, ip, port, userName, password):
        baseSsh.__init__(self, ip, port, userName, password)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.ip, self.port, self.userName, self.password)
        except:
            self.login_status = False
            print ("远程linux主机%s认证出现异常，请确认登录配置信息及主机在线情况。" % self.ip)

    def shellCmd(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdin, stdout, stderr

    def __del__(self):
        if self.login_status:
            self.ssh.close()




class linuxSftp(baseSsh):
    def __init__(self, ip, port, userName, password):
        baseSsh.__init__(self, ip, port, userName, password)
        try:
            self.conn = paramiko.Transport((self.ip, int(self.port)))
            self.conn.connect(username = self.userName, password = self.password)
        except:
            self.login_status = False
            print ("远程主机%s认证出现异常，请确认登录配置信息及主机在线情况。")
        else:
            self.sftp = paramiko.SFTPClient.from_transport(self.conn)




class linuxScp(linuxSftp):
    def get(self, localfile, remotefile):
        self.sftp.get(remotefile, localfile)
    
    def put(self, localfile, remotefile):
        print (localfile)
        print (remotefile)
        self.sftp.put(localfile, remotefile)

    def __del__(self):
        if self.login_status:
            self.conn.close()



class netSsh(baseSsh):
    login_status = True
    def __init__(self, ip, port, userName, password):
        baseSsh.__init__(self, ip, port, userName, password)

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(username=self.userName, password=self.password, hostname=self.ip, port=self.port)
        except:
            self.login_status = False
            print ("主机%sssh认证失败，请检查远程主机的登录信息及主机在线情况。" % self.ip)
        else:
            self.channel = self.ssh.invoke_shell()
            self.stdin = self.channel.makefile('wb')
            self.stdout = self.channel.makefile('r')

    def exec_su(self, cmd, passwd):
        self.stdin.write(cmd + '\n')
        self.stdin.write(passwd + '\n')
        self.stdin.flush()

    def exec_cmd(self, command):
        finish_cmd = 'cmd_end_off'
        for cmd in command:
            self.stdin.write(cmd + '\n')
        self.stdin.write(finish_cmd + '\n')
        self.stdin.flush()

        shout = ''
        for line in self.stdout:
            if ('cmd_end_off' in line):
                #判断如果结束符号在输出中，则终止循环，否则将结果添加到shout中
                break
            else:
                shout = shout + line

        return shout

    def __del__(self):
        if (self.login_status):
            self.channel.close()
