zabtman
=====

Template import/export manager for Zabbix 2+ using a git repository

#Usage
zabtman --environment "dev-us-ord1" --templates 10001 import|export

#Configuration
1. Move zabtman.sample to "~/.zabtman".
2. The "environment" parameter relates to the sections of the config file. (see zabtman.sample)

#Helpful Hints
1. easy_install GitPython
