import subprocess
import sys
import datetime 

pathToConfig = ""
pathToLogFile = ""
try:
    pathToConfig = sys.argv[1]
    pathToLogFile = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <path_to_conf_files> <path_to_out_file>")

my_cmd = ['yarprobotinterface', '--config', pathToConfig]
prog = subprocess.Popen(my_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
oFile = pathToLogFile + "yri_output_" + datetime.datetime.now().strftime("%d-%m-%Y:%H:%M:%S")+ ".log"
with open(oFile, 'w') as outfile:
    output, errors = prog.communicate()
    outfile.write(output)
