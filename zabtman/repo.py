from git import *
from os.path import expanduser,basename
from os import rename,listdir
import uuid
import json
class repo(object):
  homedir = expanduser("~")
  repodir=homedir+"/zabbix_configs"
  uniq = uuid.uuid1()
  newfile = ''
  def __init__(self,env):
    self.repo = Repo(self.repodir)
    self.git = self.repo.git
    self.newfile=self.repodir+'/'+env+'-'+str(self.uniq)+'.json'
  def status(self):
    return self.git.status()
  def checkout(self):
    return self.git.checkout(b=self.uniq)
  def add(self,config):
    f = open(self.newfile,'w')
    f.write(json.loads(config))
    f.close()
    return self.git.add(self.newfile)
  def commit(self):
    return self.git.commit(message=self.uniq)
  def push(self):
    return self.git.push('origin',self.uniq)
  def id(self):
    return self.uniq
  def run(self,config):
    self.checkout()
    self.status()
    self.add(config)
    self.commit()
    self.push()
  def list_files(self,branch):
    self.git.checkout(branch)
    self.git.pull()
    print 'Available Templates:'
    return filter(lambda x:'json' in x, listdir(self.repodir))
  def get_file(self,name):
    f = open(self.repodir+'/'+name)
    return f.read()

#repo = repo()
#print repo.checkout()
#print repo.status()
#print repo.add('/tmp/'+repo.id())
#print repo.commit()
#print repo.push()

