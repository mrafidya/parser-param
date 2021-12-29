import csv
import sys #stdout
import glob #directory crawl
import os
import codecs #covert char encoding
import datetime
from cStringIO import StringIO

load_time_default = datetime.datetime.now()
load_time_partition = datetime.datetime.now()
directory = sys.argv[1]
filename = sys.argv[2]


delimiter_char = "|"
BLOCKSIZE = 1048576 # or some other, desired size in bytes

#this for loop never execute if no file in this directory, so you need move for inside file checking
file = glob.glob(os.path.join(directory+filename))

if file:
    for file_name in file:
        ###convert encoding###
        with codecs.open(file_name, "r", "ISO-8859-1") as sourceFile:
            with codecs.open(file_name + ".tmp", "w", "utf-8") as targetFile:
                while True:
                    contents = sourceFile.read(BLOCKSIZE)
                    if not contents:
                        break
                    targetFile.write(contents)
        ######################

        with open(file_name + ".tmp", "rb") as fp: #read tmp file as it is a converted file
            fnc = ''
            function = ''
            capture = 1
            for l in fp:
                line = l.strip()
                line = line.lower()
                line = line.replace(';',' ')
                line = line.replace('   ',' ')
                if line: #get non empty line
                    if '/*' in line:
                        capture = 0

                    if capture == 1:
                        #target
                        if ('insert into' in line.lower() and 'stg_cc.monitoring_function' not in line.lower() and 'stg.proc_log' not in line.lower() and 'v_description' not in line.lower()):
                            line = line.replace('(',' ')
                            insert = line.split(' ')
                            for target in insert:
                                if '.' in target and '\'' not in target and ';' not in target and '.fnc' not in target:
                                    print function+';target;'+target
                        #function
                        elif ('postgres_function_name' in line.lower()):
                            fnc = line.split(' ')
                            for f in fnc:
                                if '.' in f:
                                    function = f.replace('\'','')
                                    function = function.replace(';','')
                                    function = function.replace('(','')
                                    function = function.strip()
                        #delete
                        elif ('delete from' in line.lower() and '--v_cmd' not in line.lower() and 'v_prev_int' not in line.lower() and 'v_description' not in line.lower()):
                            print function+';delete;'
                        #truncate
                        elif ('truncate' in line.lower() and '--v_cmd' not in line.lower() and 'v_prev_int' not in line.lower() and 'v_description' not in line.lower()):
                            print function+';truncate;'
                        #housekeeping
                        elif ('truncate' in line.lower() and '--v_cmd' not in line.lower() and 'v_prev_int' in line.lower() and 'v_description' not in line.lower()):
                            print function+';housekeeping;'
                        #source
                        elif 'v_description' not in line.lower() and '.fnc' not in line.lower() and 'stg_cc.generate_template' not in line.lower() and '-->> description' not in line.lower():
                            words = line.replace('\'',' ')
							words = words.replace('(',' ')
                            words = words.replace(')',' ')
                            words = words.replace('_1_prt_',' ')
                            words = words.split(' ')
                            for word in words:
                                if (('ods_cc.' in word) or ('dwh_cc.' in word) or ('dwh.' in word) or ('stg_cc.' in word) or ('stg.' in word) or ('rpt_cc.' in word) or ('rpt.' in word) or ('cdr.' in word) or ('bds.' in word) or ('bdstest.' in word)) and ('stg_cc.monitoring_function' not in word.lower() and 'stg.proc_log' not in word.lower()):
                                    print function+';source;'+word

                    if '*/' in line:
                        capture = 1

        ### delete tmp file
        os.remove(file_name + ".tmp")
else:

    sys.exit("Directory is kosong")