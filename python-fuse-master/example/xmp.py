#!/usr/bin/env python

#    Copyright (C) 2001  Jeff Epler  <jepler@unpythonic.dhs.org>
#    Copyright (C) 2006  Csaba Henk  <csaba.henk@creo.hu>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.#!/usr/bin/env python

#    Copyright (C) 2001  Jeff Epler  <jepler@unpythonic.dhs.org>
#    Copyright (C) 2006  Csaba Henk  <csaba.henk@creo.hu>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import os
import sys
from errno import *
from stat import *
import fcntl
import string

# pull in some spaghetti to make this stuff work without fuse-py being installed
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
import json
from fuseparts._fuse import main, FuseGetContext
from fuse import Fuse
from tkinter import *
import passwrd
import easygui
import getpass
import requests
import pwd
import grp
global n
if not hasattr(fuse, '__version__'):
    raise RuntimeError("your fuse-py doesn't know of fuse.__version__, probably it's too old.")

fuse.fuse_python_api = (0, 2)

fuse.feature_assert('stateful_files', 'has_init')

global listaa

def flag2mode(flags):
    md = {os.O_RDONLY: 'rb', os.O_WRONLY: 'wb', os.O_RDWR: 'wb+'}
    m = md[flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR)]

    if flags | os.O_APPEND:
        m = m.replace('w', 'a', 1)

    return m


class Xmp(Fuse):

    def __init__(self, *args, **kw):

        Fuse.__init__(self, *args, **kw)
        #self.ourfunction()
        # do stuff to set up your filesystem here, if you want
        # import thread
        # thread.start_new_thread(self.mythread, ())
        self.root = '/'
        self.GetContext()

#    def mythread(self):
#
#        """
#        The beauty of the FUSE python implementation is that with the python interp
#        running in foreground, you can have threads
#        """
#        print "mythread: started"
#        while 1:
#            time.sleep(120)
#            print "mythread: ticking"

   
   
        
        
    def getattr(self, path):
        fileuser = os.lstat("." + path)
        return os.lstat("." + path)
        
        
    '''         
    def ourfunction(self, path):
            w = FuseGetContext()
            
            calleruser =  w["uid"]
            print("UID",os.stat("."+path).st_uid)
            #print("uid",fileuser.st_uid)
            print(calleruser)
            print(path)
            #easygui.msgbox("owner -->"+str(fileuser.st_uid),"user calling"+str(calluser)+ " usercalling2"+str(calluser2))     
            if fileuser.st_gid == w["gid"]:
           
                p = str(oct(fileuser.st_mode))[-3:]
                #print("mode->",p) #16877
                #print("uid-->",w["uid"])
                return os.lstat("." + path)
            else:
                # print(w["uid"])
                # print(fileuser.st_uid)
                mode = str(oct(fileuser.st_mode))[-3:]
                r = requests.get("http://127.0.0.1:5000/permission/"+str(fileuser.st_uid)+"/"+str(calleruser))
                #print(r.json())

                data = r.json()
                #print(type(data))
                if(len(data)==0):
                    #Mandar Mail OWNER 
                    caller_username = getpass.getuser()
                    os.chown(path, uid, gid)
                
                else:
                    newmode = data[0] 
                    # print(newmode)
                    if mode != newmode:
                        o = '0'+ newmode['Mode']
                     
                        os.chmod(path,int(o))  
    '''
    def readlink(self, path):
        return os.readlink("." + path)

    def readdir(self, path, offset):
        for e in os.listdir("." + path):
            yield fuse.Direntry(e)

    def unlink(self, path):
        os.unlink("." + path)

    def rmdir(self, path):
        os.rmdir("." + path)

    def symlink(self, path, path1):
        os.symlink(path, "." + path1)

    def rename(self, path, path1):
        os.rename("." + path, "." + path1)

    def link(self, path, path1):
        os.link("." + path, "." + path1)

    def chmod(self, path, mode):
        os.chmod("." + path, mode)

    def chown(self, path, user, group):
        os.chown("." + path, user, group)

    def truncate(self, path, len):
        f = open("." + path, "a")
        f.truncate(len)
        f.close()

    def mknod(self, path, mode, dev):
        os.mknod("." + path, mode, dev)

    def mkdir(self, path, mode):
        os.mkdir("." + path, mode)

    def utime(self, path, times):
        os.utime("." + path, times)

    # def open(self, path, mode):
    #     os.open("." + path, mode)

#    The following utimens method would do the same as the above utime method.
#    We can't make it better though as the Python stdlib doesn't know of
#    subsecond preciseness in acces/modify times.
#  
#    def utimens(self, path, ts_acc, ts_mod):
#      os.utime("." + path, (ts_acc.tv_sec, ts_mod.tv_sec))

    def access(self, path, mode):
        if not os.access("." + path, mode):
            return -EACCES

#    This is how we could add stub extended attribute handlers...
#    (We can't have ones which aptly delegate requests to the underlying fs
#    because Python lacks a standard xattr interface.)
#
#    def getxattr(self, path, name, size):
#        val = name.swapcase() + '@' + path
#        if size == 0:
#            # We are asked for size of the value.
#            return len(val)
#        return val
#
#    def listxattr(self, path, size):
#        # We use the "user" namespace to please XFS utils
#        aa = ["user." + a for a in ("foo", "bar")]
#        if size == 0:
#            # We are asked for size of the attr list, ie. joint size of attrs
#            # plus null separators.
#            return len("".join(aa)) + len(aa)
#        return aa

    def statfs(self):
        """
        Should return an object with statvfs attributes (f_bsize, f_frsize...).
        Eg., the return value of os.statvfs() is such a thing (since py 2.2).
        If you are not reusing an existing statvfs object, start with
        fuse.StatVFS(), and define the attributes.

        To provide usable information (ie., you want sensible df(1)
        output, you are suggested to specify the following attributes:

            - f_bsize - preferred size of file blocks, in bytes
            - f_frsize - fundamental size of file blcoks, in bytes
                [if you have no idea, use the same as blocksize]
            - f_blocks - total number of blocks in the filesystem
            - f_bfree - number of free blocks
            - f_files - total number of file inodes
            - f_ffree - nunber of free file inodes
        """

        return os.statvfs(".")

    def fsinit(self):
        os.chdir(self.root)

    class XmpFile(object):
        
        

        def __init__(self, path, flags, *mode):
            self.file = os.fdopen(os.open("." + path, flags, *mode),
                                  flag2mode(flags))
            print('Init')
            #self.ourfunction(path)
            self.path = path
            self.counter = 0
            self.uid = os.lstat("." + path).st_uid
            REALOWNER = self.uid
            ownerName2 = pwd.getpwuid(REALOWNER).pw_name
            print(ownerName2)
           
            self.fd = self.file.fileno()
            
            #self.set_resuid = os.getresuid()
        def typesofaccess(self, mode):
                if mode == '4':
                    return 'read'
                elif mode == '6':
                    return 'write'
                elif mode == '7':
                    return 'execute'
            
            
        def getuserdata(self, path):
            w = FuseGetContext() 
            print('path-->', path)
            calleruser = w["uid"]
            fileuser = os.lstat("." + path)
            mode = str(oct(fileuser.st_mode))[-1:]
            realmode = self.typesofaccess(mode)
            REALOWNER = self.uid
            ownerName2 = pwd.getpwuid(REALOWNER).pw_name
            strangerName = pwd.getpwuid(calleruser).pw_name                  
            ownerName=pwd.getpwuid(os.geteuid()).pw_name
            GroupNameOwner=pwd.getpwuid(fileuser.st_gid).pw_name
            GroupNameStranger=pwd.getpwuid(calleruser).pw_name
            print('Group of owner ->', GroupNameOwner)
           # print('Owner of file ->', ownerName)
            print('Owner of file 2.0 ->', ownerName2)
            print('Stranger accessing ->', strangerName)
            print('Group of stranger ->', GroupNameStranger)
            lista = {"Owner":ownerName2,"Stranger":strangerName,"OwnerGroup":GroupNameOwner,"StrangerGroup":GroupNameStranger,"Stranger":strangerName,"Mode":realmode}
            return lista
        
        def operations(op):
            listaa.append(op)

        
        def usermode(self, path, owner, ownergroup, stranger, strangergroup, operation, modeacess):
            
            #operation(operation)
            if operation == 'write':           
                
                if(modeacess != operation):
                    
                    print('usermod -->',self.path)
                    path = self.path
                    newstr = path.replace(".", "")
                    newpath = newstr.replace("swp","")
                    print('newpath -->', newpath)
                    datalist = self.getuserdata(newpath) 
                    
                    print('Owner of write---->',datalist['Owner'])
                    
            if operation == 'read':
             #   listaa = [owner, ownergroup, stranger, strangergroup, operation, modeacess]
                 
                if(modeacess != operation):                            
                    try:
                        r = requests.get("http://127.0.0.1:5000/sendmail/"+owner+"/"+stranger+"/"+ownergroup+'/'+strangergroup+'/'+operation+'/'+modeacess,timeout=5.0)
                    except:
                        print('Error') 
         
     
        
        def read(self, length, offset): 
            print('read')
            lista = self.getuserdata(self.path)
            self.usermode(self.path,lista['Owner'],lista['OwnerGroup'],lista['Stranger'],lista['StrangerGroup'],'read',lista['Mode'])
            return self.file.read(length)

        def write(self, buf, offset):
            #a = passwrd.password()
            print('write')
            lista = self.getuserdata(self.path)
            self.usermode(self.path,lista['Owner'],lista['OwnerGroup'],lista['Stranger'],lista['StrangerGroup'],'write',lista['Mode'])
            self.file.seek(offset)
            #print("buf->",buf)
            #print("off->",offset)
            self.file.write(buf)
            return len(buf)
        
         
            
            
        def ourfunction(self, path):
            w = FuseGetContext()
            
            
            calleruser =  w["uid"]
            fileuser = os.lstat("." + path)
          #  print("owner of file UID: ",os.stat("."+path).st_uid)
            #print("uid",fileuser.st_uid)
           # print('User calling the process: ',calleruser)
            #print('path of file accessed: ', path)
            #easygui.msgbox("owner -->"+str(fileuser.st_uid),"user calling"+str(calluser)+ " usercalling2"+str(calluser2))     
            if fileuser.st_gid == w["gid"]:
           
                p = str(oct(fileuser.st_mode))[-3:]
                #print("mode->",p) #16877
                #print("uid-->",w["uid"])
                return os.lstat("." + path)
            else:
                # print(w["uid"])
                # print(fileuser.st_uid)
                mode = str(oct(fileuser.st_mode))[-1:]
                #r = requests.get("http://127.0.0.1:5000/permission/"+str(fileuser.st_uid)+"/"+str(calleruser))
                #print(r.json())
                print('Mode of access for others:', mode)
                realmode = ''
                if mode == '4':
                    realmode = 'Read'
                elif mode == '6':
                    realmode = 'Read and Write'
                elif mode == '7':
                    realmode = 'read write and execute'
                    
                data = 0
                #data = r.json()
                #print(type(data))
                if(data==0):
                    #Mandar Mail OWNER
                    user = os.lstat("." + path)
                    ownerName2 = pwd.getpwuid(user.st_uid).pw_name
                    strangerName=pwd.getpwuid(calleruser).pw_name                  
                    ownerName=pwd.getpwuid(os.geteuid()).pw_name
                    GroupNameOwner=pwd.getpwuid(user.st_gid).pw_name
                    GroupNameStranger=pwd.getpwuid(w["gid"]).pw_name
                    #print('Group of owner ->', GroupNameOwner)
                    #print('Owner of file ->', ownerName)
                    #('Owner of file 2.0 ->', ownerName2)
                    #print('Stranger accessing ->', strangerName)
                    #print('Group of stranger ->', GroupNameStranger)
                   # print(strangerName + ' can '+ realmode +' your file!')
                  

            
        def release(self, flags):
            self.file.close()

        def _fflush(self):
            if 'w' in self.file.mode or 'a' in self.file.mode:
                self.file.flush()

        def fsync(self, isfsyncfile):
            self._fflush()
            if isfsyncfile and hasattr(os, 'fdatasync'):
                os.fdatasync(self.fd)
            else:
                os.fsync(self.fd)

        def flush(self):
            self._fflush()
            # cf. xmp_flush() in fusexmp_fh.c
            os.close(os.dup(self.fd))

        def fgetattr(self):
            return os.fstat(self.fd)

        def ftruncate(self, len):
            self.file.truncate(len)

        def lock(self, cmd, owner, **kw):
            # The code here is much rather just a demonstration of the locking
            # API than something which actually was seen to be useful.

            # Advisory file locking is pretty messy in Unix, and the Python
            # interface to this doesn't make it better.
            # We can't do fcntl(2)/F_GETLK from Python in a platfrom independent
            # way. The following implementation *might* work under Linux. 
            #
            # if cmd == fcntl.F_GETLK:
            #     import struct
            # 
            #     lockdata = struct.pack('hhQQi', kw['l_type'], os.SEEK_SET,
            #                            kw['l_start'], kw['l_len'], kw['l_pid'])
            #     ld2 = fcntl.fcntl(self.fd, fcntl.F_GETLK, lockdata)
            #     flockfields = ('l_type', 'l_whence', 'l_start', 'l_len', 'l_pid')
            #     uld2 = struct.unpack('hhQQi', ld2)
            #     res = {}
            #     for i in xrange(len(uld2)):
            #          res[flockfields[i]] = uld2[i]
            #  
            #     return fuse.Flock(**res)

            # Convert fcntl-ish lock parameters to Python's weird
            # lockf(3)/flock(2) medley locking API...
            op = { fcntl.F_UNLCK : fcntl.LOCK_UN,
                   fcntl.F_RDLCK : fcntl.LOCK_SH,
                   fcntl.F_WRLCK : fcntl.LOCK_EX }[kw['l_type']]
            if cmd == fcntl.F_GETLK:
                return -EOPNOTSUPP
            elif cmd == fcntl.F_SETLK:
                if op != fcntl.LOCK_UN:
                    op |= fcntl.LOCK_NB
            elif cmd == fcntl.F_SETLKW:
                pass
            else:
                return -EINVAL

            fcntl.lockf(self.fd, op, kw['l_start'], kw['l_len'])

    def main(self, *a, **kw):

        self.file_class = self.XmpFile

        return Fuse.main(self, *a, **kw)


def main():

    usage = """
Userspace nullfs-alike: mirror the filesystem tree from some point on.

""" + Fuse.fusage

    server = Xmp(version="%prog " + fuse.__version__,
                 usage=usage,
                 dash_s_do='setsingle')

    server.parser.add_option(mountopt="root", metavar="PATH", default='/',
                             help="mirror filesystem from under PATH [default: %default]")
    server.parse(values=server, errex=1)

    try:
        if server.fuse_args.mount_expected():
            os.chdir(server.root)
    except OSError:
        print("can't enter root of underlying filesystem", file=sys.stderr)
        sys.exit(1)

    server.main()


if __name__ == '__main__':
    main()
#

import os, sys
from errno import *
from stat import *
import fcntl
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse 


if not hasattr(fuse, '__version__'):
    raise RuntimeError("your fuse-py doesn't know of fuse.__version__, probably it's too old.")

fuse.fuse_python_api = (0, 2)

fuse.feature_assert('stateful_files', 'has_init')


def flag2mode(flags):
    md = {os.O_RDONLY: 'rb', os.O_WRONLY: 'wb', os.O_RDWR: 'wb+'}
    m = md[flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR)]

    if flags | os.O_APPEND:
        m = m.replace('w', 'a', 1)

    return m


class Xmp(Fuse):

    def __init__(self, *args, **kw):

        Fuse.__init__(self, *args, **kw)

        # do stuff to set up your filesystem here, if you want
        #import thread
        #thread.start_new_thread(self.mythread, ())
        self.root = '/'

#    def mythread(self):
#
#        """
#        The beauty of the FUSE python implementation is that with the python interp
#        running in foreground, you can have threads
#        """
#        print "mythread: started"
#        while 1:
#            time.sleep(120)
#            print "mythread: ticking"

    def getattr(self, path):
        return os.lstat("." + path)

    def readlink(self, path):
        return os.readlink("." + path)

    def readdir(self, path, offset):
        for e in os.listdir("." + path):
            yield fuse.Direntry(e)

    def unlink(self, path):
        os.unlink("." + path)

    def rmdir(self, path):
        os.rmdir("." + path)

    def symlink(self, path, path1):
        os.symlink(path, "." + path1)

    def rename(self, path, path1):
        os.rename("." + path, "." + path1)

    def link(self, path, path1):
        os.link("." + path, "." + path1)

    def chmod(self, path, mode):
        os.chmod("." + path, mode)
    
    def chown(self, path, user, group):
        os.chown("." + path, user, group)

    def truncate(self, path, len):
        f = open("." + path, "a")
        f.truncate(len)
        f.close()

    def mknod(self, path, mode, dev):
        os.mknod("." + path, mode, dev)

    def mkdir(self, path, mode):
        os.mkdir("." + path, mode)

    def utime(self, path, times):
        os.utime("." + path, times)

#    The following utimens method would do the same as the above utime method.
#    We can't make it better though as the Python stdlib doesn't know of
#    subsecond preciseness in acces/modify times.
#  
#    def utimens(self, path, ts_acc, ts_mod):
#      os.utime("." + path, (ts_acc.tv_sec, ts_mod.tv_sec))

    def access(self, path, mode):
        if not os.access("." + path, mode):
            return -EACCES

#    This is how we could add stub extended attribute handlers...
#    (We can't have ones which aptly delegate requests to the underlying fs
#    because Python lacks a standard xattr interface.)
#
#    def getxattr(self, path, name, size):
#        val = name.swapcase() + '@' + path
#        if size == 0:
#            # We are asked for size of the value.
#            return len(val)
#        return val
#
#    def listxattr(self, path, size):
#        # We use the "user" namespace to please XFS utils
#        aa = ["user." + a for a in ("foo", "bar")]
#        if size == 0:
#            # We are asked for size of the attr list, ie. joint size of attrs
#            # plus null separators.
#            return len("".join(aa)) + len(aa)
#        return aa

    def statfs(self):
        """
        Should return an object with statvfs attributes (f_bsize, f_frsize...).
        Eg., the return value of os.statvfs() is such a thing (since py 2.2).
        If you are not reusing an existing statvfs object, start with
        fuse.StatVFS(), and define the attributes.

        To provide usable information (ie., you want sensible df(1)
        output, you are suggested to specify the following attributes:

            - f_bsize - preferred size of file blocks, in bytes
            - f_frsize - fundamental size of file blcoks, in bytes
                [if you have no idea, use the same as blocksize]
            - f_blocks - total number of blocks in the filesystem
            - f_bfree - number of free blocks
            - f_files - total number of file inodes
            - f_ffree - nunber of free file inodes
        """

        return os.statvfs(".")

    def fsinit(self):
        os.chdir(self.root)

    class XmpFile(object):

        def __init__(self, path, flags, *mode):
            self.file = os.fdopen(os.open("." + path, flags, *mode),
                                  flag2mode(flags))
            print("III")
            self.fd = self.file.fileno()
            

        def read(self, length, offset):
            print('READ')
            self.file.seek(offset)
            return self.file.read(length)

        def write(self, buf, offset):
            self.file.seek(offset)
            self.file.write(buf)
            return len(buf)

        def release(self, flags):
            self.file.close()

        def _fflush(self):
            if 'w' in self.file.mode or 'a' in self.file.mode:
                self.file.flush()

        def fsync(self, isfsyncfile):
            self._fflush()
            if isfsyncfile and hasattr(os, 'fdatasync'):
                os.fdatasync(self.fd)
            else:
                os.fsync(self.fd)

        def flush(self):
            self._fflush()
            # cf. xmp_flush() in fusexmp_fh.c
            os.close(os.dup(self.fd))

        def fgetattr(self):
            return os.fstat(self.fd)

        def ftruncate(self, len):
            self.file.truncate(len)

        def lock(self, cmd, owner, **kw):
            # The code here is much rather just a demonstration of the locking
            # API than something which actually was seen to be useful.

            # Advisory file locking is pretty messy in Unix, and the Python
            # interface to this doesn't make it better.
            # We can't do fcntl(2)/F_GETLK from Python in a platfrom independent
            # way. The following implementation *might* work under Linux. 
            #
            # if cmd == fcntl.F_GETLK:
            #     import struct
            # 
            #     lockdata = struct.pack('hhQQi', kw['l_type'], os.SEEK_SET,
            #                            kw['l_start'], kw['l_len'], kw['l_pid'])
            #     ld2 = fcntl.fcntl(self.fd, fcntl.F_GETLK, lockdata)
            #     flockfields = ('l_type', 'l_whence', 'l_start', 'l_len', 'l_pid')
            #     uld2 = struct.unpack('hhQQi', ld2)
            #     res = {}
            #     for i in xrange(len(uld2)):
            #          res[flockfields[i]] = uld2[i]
            #  
            #     return fuse.Flock(**res)

            # Convert fcntl-ish lock parameters to Python's weird
            # lockf(3)/flock(2) medley locking API...
            op = { fcntl.F_UNLCK : fcntl.LOCK_UN,
                   fcntl.F_RDLCK : fcntl.LOCK_SH,
                   fcntl.F_WRLCK : fcntl.LOCK_EX }[kw['l_type']]
            if cmd == fcntl.F_GETLK:
                return -EOPNOTSUPP
            elif cmd == fcntl.F_SETLK:
                if op != fcntl.LOCK_UN:
                    op |= fcntl.LOCK_NB
            elif cmd == fcntl.F_SETLKW:
                pass
            else:
                return -EINVAL

            fcntl.lockf(self.fd, op, kw['l_start'], kw['l_len'])


    def main(self, *a, **kw):

        self.file_class = self.XmpFile

        return Fuse.main(self, *a, **kw)


def main():

    usage = """
Userspace nullfs-alike: mirror the filesystem tree from some point on.

""" + Fuse.fusage

    server = Xmp(version="%prog " + fuse.__version__,
                 usage=usage,
                 dash_s_do='setsingle')

    server.parser.add_option(mountopt="root", metavar="PATH", default='/',
                             help="mirror filesystem from under PATH [default: %default]")
    server.parse(values=server, errex=1)

    try:
        if server.fuse_args.mount_expected():
            os.chdir(server.root)
    except OSError:
        print("can't enter root of underlying filesystem", file=sys.stderr)
        sys.exit(1)

    server.main()


if __name__ == '__main__':
    main()
