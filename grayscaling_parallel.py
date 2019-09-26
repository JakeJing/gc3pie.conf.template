#! /usr/bin/env python
#
"""
usage: ./grayscaling_parallel.py in-data/* -vv -C 2 -r sciencecloud -s pjob
This simple ParallelTaskCollection allows you to run a generic command and
will allow you to execute it in a sequential or in a parallel task
collection.

This is mainly used for testing and didactic purpouses, don't use it
on a production environment!
"""
# Copyright (C) 2012-2014 S3IT, Zentrale Informatik, University of Zurich. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#

__docformat__ = 'reStructuredText'
import os
import os.path
import shlex
import gc3libs.exceptions
from gc3libs import Application, Run
from gc3libs.cmdline import SessionBasedScript, nonnegative_int, existing_file
from gc3libs.workflow import TaskCollection
from gc3libs.workflow import ParallelTaskCollection, SequentialTaskCollection
from os.path import abspath, basename

## main: run command-line

if "__main__" == __name__:
    import grayscaling_parallel
    grayscaling_parallel.GRunScript().run()


class GRunScript(SessionBasedScript):
    """
    An `Application` wrapper which will execute the arguments as a
    shell script command. This application will also check if some of
    the argument is a file, and in that case it will add it to the
    files to upload as input.
    """
    version = '1.1.1'
    def setup_args(self):
        self.add_param("input_dirs", nargs='+', type=existing_file, default=None,
                        help="Directories with input files.")

    def new_tasks(self, extra):
        fold_name = [os.path.basename(path) for path in self.params.input_dirs]
        apps = []
        for image in fold_name:
            output_dir = ("colorized-{name}.d".format(name=basename(image)))
            apps.append(GRunApplication(image, output_dir))
        task =  ParallelTaskCollection(apps)
        return [task]

    def after_main_loop(self):
        print ""
        tasks = self.session.tasks.values()
        for app in tasks:
            if isinstance(app, TaskCollection):
                tasks.extend(app.tasks)
            if not isinstance(app, Application):
                continue
            print "==========================================="
            # print "Application     %s" % app.jobname
            print "  state:        %s" % app.execution.state
            print "  command line: %s" % str.join(" ", app.arguments)
            print "  return code:  %s" % app.execution._exitcode
            print "  output dir:   %s" % app.output_dir

class GRunApplication(Application):
    def __init__(self, image, output_dir):
        Application.__init__(self,
                             # arguments = ["convert", inp, "-colorspace", "gray", out],
                             arguments = ["sh", "/home/ubuntu/tutorial_gc3pie/convert.sh", image],
                             inputs=[],
                             outputs = gc3libs.ANY_OUTPUT,
                             output_dir=output_dir,
                             stdout = "stdout.txt",
                             stderr = "stderr.txt")
                             
# notes:
# 1. **output_dir**: is the directory name for saving output for each task, which will be downloaded from cloud to your own instance. That means each task or job will create its own output directory.
# 2. **outputs**: should be set as gc3libs.ANY_OUTPUT, so that everything will be automatically saved in the output_dir.
# 3. **inputs**: can leave empty, so that no input files will be copied to the output_dir. If u want to save anything to the output directory. You can add things here.
# 4. **arguments**: can be a simple command, or ideally you can add a bash script to run the certain script. It would be more useful.



                             
