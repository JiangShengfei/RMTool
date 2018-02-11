#!/usr/bin/python
# --*-- coding:utf-8 --*--

def readremoteinfo(file_path):
    remoteinfo = []
    f = open(file_path, "r")
    lines = f.readlines()
    for item in lines:
        tmp = []
        for element in item.split("/"):
            tmp.append(element.strip("\n"))
        remoteinfo.append(tmp)
    f.close()
    return remoteinfo

def readcommands(file_path):
    commands = []
    f = open(file_path, "r")
    lines = f.readlines()
    for row in lines:
        commands.append(row.strip("\n"))
    return commands


class std2file:
    open_status = True
    def __init__(self, fileName):
        self.fileName = fileName
        try:
            self.f = open(self.fileName ,'w')
        except:
            open_status = False
            print ("文件%s打开失败，请检查文件路径及文件权限是否正确。")

    def msg_write(self, msg):
        self.f.write(msg)

    def __del__(self):
        if self.open_status:
            self.f.close()
