__author__ = 'aurcioli'

import argparse
from googledrive import GoogleDrive

logo = ("\n"
        "                         _           _             _\n"
        "                        | |         (_)           | |\n"
        " ___  ___  __ _ _ __ ___| |__   __ _ _  __ _ _ __ | |_\n"
        "/ __|/ _ \/ _` | '__/ __| '_ \ / _` | |/ _` | '_ \| __|\n"
        "\__ \  __/ (_| | | | (__| | | | (_| | | (_| | | | | |_\n"
        "|___/\___|\__,_|_|  \___|_| |_|\__, |_|\__,_|_| |_|\__|\n"
        "                                __/ |\n"
        "                               |___/\n"
        "\n")

parser = argparse.ArgumentParser(description="Cloud Service forensic imaging tool")
parser.add_argument('project_dir', metavar = 'project_dir', type=str, nargs=1, help="Path where project will be created. If project already exists it will use existing settings")
parser.add_argument('service', metavar = 'service_type', type=str, nargs=1, help="Service to forensically image. Accepted values are: google_drive",)
parser.add_argument('--mode','-m', metavar = 'mode', type=str, nargs=1, help="Synchronization mode. Accepted values are: full, metadata. Default value is: full", required=False, default="full")

args = parser.parse_args()

print(logo)

if args.service[0].lower() == "google_drive":
    g = GoogleDrive.GoogleDrive(args.project_dir[0])
    g.full_sync()

