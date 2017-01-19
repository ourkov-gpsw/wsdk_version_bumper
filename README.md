# wsdk_version_bumper
Bumps minor or point version of Android WSDK.  

Need more thorough steps on how this works

/bumppoint/<branch>/<ticket>
would be used on a release branch after a release goes out.  Something like:

bumppoint/wsdk0.15/CAL-1234

would do the following:
checkout release/wsdk0.15
create/checkout feature/CAL-1234 branch from the release branch
bump the point version from, say, 0.15.0 to 0.15.1 
add/commit the change
push feature/CAL-1234 to origin


/bumpminor/develop/CAL-4567

would do the following:
checkout develop
create/checkout feature/CAL-4567 branch from develop
bump the minor version from, say, 0.15.0 to 0.16.0
add/commit the changes
push feature/CAL-4567 to origin


Both steps still require going and making the Pull Request in GitHub, merging, and deleting the new branch.  But at least it's a start.  Would be nice to have a standing open ticket to reference for this.
