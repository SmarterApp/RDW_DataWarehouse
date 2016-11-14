#!/bin/bash

#
# 2012/01/02
#
# author: Eugene Jen (ejen@wgen.net)
# prereuqusit, the ssh key to git servers are registered.
# if so, then feel free to use cron on OS X or Linux to automated this process
#

cd /tmp
rm -fr udl.git/
git clone --bare git://mcgit.mc.wgenhq.net/mclass/udl
cd udl.git/
git push --mirror ssh://git@github.wgenhq.net/Ed-Ware-SBAC/udl
cd ..
rm -fr udl.git
