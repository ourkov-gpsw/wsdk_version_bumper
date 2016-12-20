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
import sys
import argparse

version_bump_ticket="CAL-1185"
wsdk_url="git@github.com:ourkov-gpsw/my-dumb-android-library.git"

def parseArgs():
	global args
	parser = argparse.ArgumentParser()
	parser.add_argument('--debug', '-d', dest='debug', action='store_true', default=False, help='debug mode.  just print commands')
	parser.add_argument('--minor', '-m', dest='bump_minor', action='store_true', default=False, help='bump minor version (ie. 0.12.0 to 0.13.0)')
	parser.add_argument('--point', '-p', dest='bump_point', action='store_true', default=False, help='bump point version (ie. 0.12.0 to 0.12.1)')
	parser.add_argument('--ticket', '-t', dest='version_bump_ticket', default=version_bump_ticket, help="Jira ticket to reference in commit")
	parser.add_argument('--workspace', '-w', dest='workspace', default='.', help="directory where wsdk is checked out")
	parser.add_argument('--url', '-u', dest='git_url', default=wsdk_url, help="what to clone if workspace does not exist")
        parser.add_argument('--branch', '-b', dest='git_branch', default='master', help="which branch to check out when cloning")
	args = parser.parse_args()
	if not args.bump_minor and not args.bump_point:
		print "Nothing to do.  Need to specify --minor or --point version to bump"
		sys.exit(1)
	if not args.version_bump_ticket:
		print "Need to reference a Jira ticket"
	if not os.path.isfile(args.workspace):
		print "Workspace %s does not exist.  Checking out %s branch of %s" % (args.workspace, args.git_branch, args.git_url)
		os.system("git clone --recursive -b %s %s %s" % (args.git_branch, args.git_url, args.workspace))
		# FIXME  this call errs out complaining about "checkout-branch" is not a valid option
		#git.Repo.clone_from(args.git_url, args.workspace, checkout_branch=args.git_branch)

def checkoutFeatureBranch():
	featureBranch="feature/%s" % args.version_bump_ticket
	print "checking out %s" % featureBranch
	cmd = "git -C %s  checkout -b %s" % (args.workspace, featureBranch)
	print cmd
	# if not args.debug:
	# FIXME		os.system(cmd)

def pushFeatureToOrigin():
	featureBranch="feature/%s" % args.version_bump_ticket
	print "pushing branch to origin"
	cmd = "git -C %s push origin %s" % (args.workspace, featureBranch)
	print cmd
	# if not args.debug:
	# FIXME 	os.system(cmd)

def bumpMinorVersion():
	print "bumping minor version"
	checkoutFeatureBranch()
	propfile=os.path.sep.join([args.workspace, "wsdk", "gradle.properties"])
	#	try:
	if 1:
		contents = open(propfile, 'r').readlines()
		for line in contents:
			if line.startswith("version"):
				# split version into an array
				version=line.split('=')[1].split('.')
				print "old version: %s" % version
				version[1] = str(int(version[1]) + 1)
				print "new version: %s" % version
		f = open(propfile, 'w')
		for line in contents:
			if line.startswith("version"):
				f.write("version = %s" % '.'.join(version))
			else:
				f.write(line)
		return '.'.join(version)
	#except:
	#	print "something musta happened bumping the version"

def bumpPointVersion():
	print "bumping point version"
	checkoutFeatureBranch()
	propfile=os.path.sep.join([args.workspace, "wsdk", "gradle.properties"])
        #try:
	if 1:
                contents = open (propfile, 'r').readlines()
                for line in contents:
                        if line.startswith("version"):
                                # split version into an array
                                version=line.split('=')[1].split('.')
                                print "old version: %s" % version
                                version[2] = str(int(version[2]) + 1)
                                print "new version: %s" % version
		f = open(propfile, 'w')
                for line in contents:
                        if line.startswith("version"):
                                f.write("version = %s" % '.'.join(version))
                        else:
                                f.write(line)
		return '.'.join(version)
        #except:
        #        print "something musta happened bumping the version"

if __name__ == '__main__':
	parseArgs()
	print args
	prop_file = os.path.abspath(os.path.sep.join([args.workspace, "wsdk", "gradle.properties"]))
	repo = git.Repo(os.path.abspath(args.workspace))
	old_branch = repo.active_branch
	new_branch = "feature/%s" % args.version_bump_ticket
	print "checking out new branch: %s" % new_branch
	print "        from old branch: %s" % old_branch
	repo.git.checkout('HEAD', b=new_branch)
	if args.bump_minor:
		new_version = bumpMinorVersion()
	if args.bump_point:
		new_version = bumpPointVersion()
	print "git add %s" % prop_file
	repo.git.add(prop_file)
	commit_message = "[%s] bump version to %s" % (args.version_bump_ticket, new_version.strip())
	print "git commit -m \"%s\"" % commit_message
	repo.git.commit( m=commit_message )
	print "git push origin %s" % new_branch
	repo.git.push( 'origin', new_branch )
	print "======================================================================"
	print "New branch: %s has been pushed to origin: %s" % (new_branch, repo.remotes.origin.url)
	print "Need to go create a pull request from   %s -> %s" % (new_branch, old_branch)


