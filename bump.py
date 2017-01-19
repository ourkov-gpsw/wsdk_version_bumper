#
# Script for bumping versions of Android WSDK
# 
# When we release a build of WSDK, the release branch should have it's point release incremented 
#
# When we create release branches, the develop branch should have it's minor release incremented
#
# TODO: Should we have a ticket that just stays open for these?  
# TODO: Is it possible to auto create a PR? requires github library and credentials
#

import git
import os
import shutil
import sys

from flask import Flask
app = Flask(__name__)

# FIXME just for debugging
git_url="git@github.com:ourkov-gpsw/my-dumb-android-library.git"
workspace="./workspace"
debug=False

def prepWorkspace(branch, ticket):
	print "removing any existing workspace"
	if os.path.isdir(workspace):
		shutil.rmtree(workspace)
	if branch != 'develop':
		branch = "release/%s" % branch
	print "Checking out %s branch of %s" % (branch, git_url)
	os.system("git clone --recursive -b %s %s %s" % (branch, git_url, workspace))
	featureBranch="feature/%s" % ticket
        print "checking out %s" % featureBranch
        cmd = "git -C %s  checkout -b %s" % (workspace, featureBranch)
	print cmd
	os.system(cmd)

def bumpVersion(version_type):
	propfile=os.path.sep.join([workspace, "wsdk", "gradle.properties"])
        contents = open (propfile, 'r').readlines()
        for line in contents:
		if line.startswith("version"):
			# split version into an array
			version=line.split('=')[1].split('.')
 			print "old version: %s" % version
			if version_type == "minor":
 				version[1] = str(int(version[1]) + 1)
			else:
 				version[2] = str(int(version[2]) + 1)
 			print "new version: %s" % version
	newVersion = '.'.join(version).strip()
	f = open(propfile, 'w')
 	for line in contents:
 		if line.startswith("version"):
 			f.write("version = %s\n" % newVersion)
 		else:
			f.write(line)
	return newVersion

def pushFeatureToOrigin(ticket, newVersion):
	featureBranch="feature/%s" % ticket
	propfile = os.path.abspath(os.path.sep.join([workspace, "wsdk", "gradle.properties"]))
	commitMessage = "[%s] bump version to %s" % (ticket, newVersion)
	repo = git.Repo(os.path.abspath(workspace))
	print "git add %s" % propfile
	repo.git.add(propfile)
	print "git commit -m \"%s\"" % commitMessage
	repo.git.commit(m=commitMessage)
	print "pushing %s branch to origin" % featureBranch
	if not debug:
		repo.git.push("origin", featureBranch)

@app.route("/bumpminor/<branch>/<ticket>")
def bumpMinorVersion(branch, ticket):
	print "bumping minor version on branch %s with ticket %s" % (branch, ticket)
	prepWorkspace(branch, ticket)
	newVersion = bumpVersion("minor")
	pushFeatureToOrigin(ticket, newVersion)
	return "bumped minor version to %s on new branch feature/%s.  Need to merge PR to %s" % (newVersion, ticket, branch)

@app.route("/bumppoint/<branch>/<ticket>")
def bumpPointVersion(branch, ticket):
	print "bumping point version on branch %s with ticket %s" % (branch, ticket)
	prepWorkspace(branch, ticket)
	newVersion = bumpVersion("point")
	pushFeatureToOrigin(ticket, newVersion)
	return "bumped point version to %s on new branch feature/%s.  Need to merge PR to %s" % (newVersion, ticket, branch)

helpStr = '''Need to specify version to bump (minor or point), src branch, and ticket

    example:  /bumpminor/develop/CAL-1529

         or:  /bumppoint/wsdk0.15/CAL-1530
'''

@app.route("/")
def showForm():
	return "FIXME: need to implement a web form"

@app.route("/bumppoint/<branch>")
def pointHelp(branch):
	return helpStr

@app.route("/bumpminor/<branch>")
def minorHelp(branch):
	return helpStr

app.run()

