# -*- coding: utf-8 -*-
"""
Interface to the Sage fileserver
"""


#*****************************************************************************
#       Copyright (C) 2016 Volker Braun <vbraun.name@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************



import os
import subprocess



class FileServer(object):

    def __init__(self):
        self.user = 'sagemath'
        self.hostname = 'k8s-ssh.sagemath.org'

    def upstream_directory(self, package):
        """
        Return the directory where the tarball resides on the server
        """
        return os.path.join(
            '/', 'home', 'files', 'files', 'spkg', 'upstream', package.name,
        )

    def upload(self, package):
        """
        Upload the current tarball of package
        """
        subprocess.check_call([
            'ssh', 'files@{}'.format(self.hostname),
            'mkdir -p {0} && touch {0}/index.html'.format(self.upstream_directory(package))
        ])
        subprocess.check_call([
            'rsync', '-av', '--checksum', '-e', 'ssh -l files',
            package.tarball.upstream_fqn,
            '{0}:{1}'.format(self.hostname, self.upstream_directory(package))
        ])

    def publish(self):
        """
        Publish the files
        """
        subprocess.check_call([
            'ssh', 'files@{}'.format(self.hostname), './publish-files.sh'
        ])
