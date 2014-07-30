#!/usr/bin/python
#coding=utf-8

# This script will create a package for AnyStore SDK
import os
import traceback
import shutil, errno
import zipfile

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            # print 'zipping %s as %s' % (os.path.join(dirname, filename), arcname)
            zf.write(absname, arcname)
    zf.close()

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def main():
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option('-v', '--version',dest='version', help="Version number for the SDK")
	opts, args = parser.parse_args()

	if opts.version:
		version = opts.version


	pubDir = '/publish'
	demoDir = '/Demo'
	sdkDir = '/SDK'
	archiveName = '/AnyStore_SDK'

	print('==> creating publish folder')
	currDir = os.getcwd()
	publishDir = currDir + pubDir

	docPath = currDir + '/docs/guide.md'
	outDocPath = publishDir + '/Readme.html'

	print(publishDir)
	shutil.rmtree(publishDir)
	os.makedirs(publishDir)
	print

	print('==> generating documentation form markdown')
	from grip import export
	export(path=docPath, out_filename=outDocPath)
	print

	print('==> copy resources to publish folder')
	copyanything(currDir + sdkDir, publishDir + sdkDir)
	copyanything(currDir + demoDir, publishDir + demoDir)
	print

	print('==> create archive')
	zip(publishDir, publishDir + archiveName + version)
	print

# ---------- main -------------
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)