__author__ = 'aurcioli'

import argparse
from googledrive import GoogleDrive
from project import Project
from oi import IO

parser = argparse.ArgumentParser(description="Cloud Service forensic imaging tool")
parser.add_argument('project_dir', metavar='project_dir', type=str, nargs=1,
                    help="Path where project will be created. If project already exists it will use existing settings")
parser.add_argument('service', metavar='service_type', type=str, nargs=1,
                    help="Accepted values: google_drive, dropbox, onedrive", )
parser.add_argument('--mode', '-m', metavar='mode', type=str, nargs=1,
                    help="Synchronization mode. Accepted values are: full, metadata. Default value is: full",
                    required=False, default="full")
parser.add_argument('--threads', '-t', metavar='threads', type=int,
                    help="Amount of parallel threads used to download files", default=5)
parser.add_argument('--prompt','-p', help="Prompt before actually downloading anything", action="store_true")

args = parser.parse_args()

IO.IO.print_logo()

service = args.service[0]
working_dir = args.project_dir[0]
threads = args.threads

P = Project.Project(args)

if args.service[0].lower() == "google_drive":
    g = GoogleDrive.GoogleDrive(P)
    g.full_sync()
