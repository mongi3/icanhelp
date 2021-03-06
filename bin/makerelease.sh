#!/bin/bash -e
# This is a script to build a release for the icanhelp website while
# sanitizing any required data.

# This script should be ran in the directory you want the release tgz
# to be dropped in.  This should NOT be in the subtree for the project.

CURDIR=`pwd`
echo "WARNING: this script assumes you want the output tarball"
echo "  created in the current directory: $CURDIR"
echo
echo "This script will remove any subdir named icanhelp..."
echo
read -n1 -r -p "Press any key to continue... (ctrl-C to quit)" key

PROJECT_BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..
rm -rf icanhelp
hg archive -R $PROJECT_BASE icanhelp

# Create release and cleanup
OUTPUT=`date +%Y_%m_%d`-icanhelpRelease.tgz
cp icanhelp/bin/Vagrantfile .
cp icanhelp/bin/README.txt .
tar -czvf $OUTPUT icanhelp Vagrantfile README.txt
rm -rf icanhelp Vagrantfile README.txt

echo
echo "Release file generated: $OUTFILE"
echo "DONE!"
