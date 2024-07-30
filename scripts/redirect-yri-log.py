import subprocess
import os
import datetime 
import argparse
from pathlib import Path
import sys

def pretty_output():
    if 'YARP_COLORED_OUTPUT' in os.environ:
        if os.environ["YARP_COLORED_OUTPUT"]:
            os.environ['YARP_COLORED_OUTPUT'] = "0"

def log(pathToConfig: Path, pathToLogFile: Path):
    pretty_output()
    my_cmd = ['yarprobotinterface', '--config', pathToConfig, '--dryrun']
    prog = subprocess.Popen(my_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    oFile = pathToLogFile / ("yri_output_" + datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".log")
    with open(oFile, 'w') as log_file:
        try:
            while True:
                realtime_output = prog.stdout.readline()
                if realtime_output == '' and prog.poll() is not None:
                    break
                if realtime_output:
                    log_file.write(realtime_output)
                    log_file.flush()
                    print(realtime_output.strip(), flush=True)
        except KeyboardInterrupt:
            print("KeyboardInterrupt received, terminating the process...")
            prog.terminate()
            prog.wait()
            print("Process terminated")
            sys.exit(0)

def main():
    print(f"Saving log...")
    parser = argparse.ArgumentParser(description="Save the log of the yri run")
    parser.add_argument(
        "--config_file",
        "-c",
        type=lambda p: Path(p).absolute(),
        required=True,
        help="Path to the configuration file containing to feed the yri.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=lambda p: Path(p).absolute(),
        default=Path.cwd(),
        required=False,
        help="Path where the generated log will be saved.",
    )

    args = parser.parse_args()

    try:
        log(pathToConfig=args.config_file, pathToLogFile=args.output)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, terminating the process...")
        sys.exit(0)

if __name__ == "__main__":
    main()
