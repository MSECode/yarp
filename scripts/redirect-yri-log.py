import subprocess
import os
import datetime 
import argparse
import sys
from pathlib import Path


def pretty_output():
    # Always disable colored output for logs
    os.environ['YARP_COLORED_OUTPUT'] = "0"

def log(pathToConfig: Path, output_dir: Path):
    pretty_output()
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    log_filename = output_dir / ("yri_output_" + datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".log")
    my_cmd = ['yarprobotinterface', '--config', str(pathToConfig)]
    try:
        prog = subprocess.Popen(my_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except FileNotFoundError:
        print("Error: 'yarprobotinterface' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to start subprocess: {e}")
        sys.exit(1)
    try:
        with open(log_filename, 'w') as log_file:
            for realtime_output in iter(prog.stdout.readline, ''):
                if realtime_output == '' and prog.poll() is not None:
                    break
                if realtime_output:
                    log_file.write(realtime_output)
                    log_file.flush()
                    print(realtime_output.strip(), flush=True)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, terminating the process...")
        prog.terminate()
        try:
            prog.wait(timeout=20)
        except subprocess.TimeoutExpired:
            prog.kill()
        print(f"Process terminated with return code {prog.returncode}.")
        sys.exit(0)
    if prog.returncode != 0:
        print(f"Process exited with non-zero return code: {prog.returncode}")

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
        log(pathToConfig=args.config_file, output_dir=args.output)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received, terminating the process...")
        sys.exit(0)
    

if __name__ == "__main__":
    main()
