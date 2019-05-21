print '#------------------------------------------------------------------------------------------------------------------------------------------------------------'
print '#                                                     Automatic application deploy '
print '#------------------------------------------------------------------------------------------------------------------------------------------------------------'

AdminConfig.setValidationLevel("NONE")

print "Starting script..."
print "Reading config parameters..."

import sys
# get line separator
import java

lineSeparator = java.lang.System.getProperty('line.separator')

CELL_NAME = AdminControl.getCell()
NODE_NAME = AdminControl.getNode()
SERVER_NAME = None
WEB_NAME = None
EAR_NAME = None
WEB_PATH = None
EAR_PATH = None

# Try to get a node, cell, and server from command-line arguments
i = 0
while i < len(sys.argv):
    if sys.argv[i] == "-server":
        SERVER_NAME = sys.argv[i + 1]
    if sys.argv[i] == "-webName":
        WEB_NAME = sys.argv[i + 1]
    if sys.argv[i] == "-earName":
        EAR_NAME = sys.argv[i + 1]
    if sys.argv[i] == "-webPath":
        WEB_PATH = sys.argv[i + 1]
    if sys.argv[i] == "-earPath":
        EAR_PATH = sys.argv[i + 1]
    i = i + 1
# endWhile

if SERVER_NAME == None:
    print "Please specify a server with the \'-server\' option."
    sys.exit(100)
if WEB_NAME == None:
    print "Please specify a web application name with the \'-webName\' option."
    sys.exit(100)
if EAR_NAME == None:
    print "Please specify a ear application name with the \'-earName\' option."
    sys.exit(100)
if WEB_PATH == None:
    print "Please specify a ear application name with the \'-webPath\' option."
    sys.exit(100)
if EAR_PATH == None:
    print "Please specify a ear application name with the \'-earPath\' option."
    sys.exit(100)

print "Cell:  " + CELL_NAME + ", Node:  " + NODE_NAME + ", Server:  " + SERVER_NAME

apps = AdminApp.list("WebSphere:cell=" + CELL_NAME + ",node=" + NODE_NAME + ",server=" + SERVER_NAME).split(
    lineSeparator)

print apps
###Listing Installed Applications###

if (WEB_NAME in apps):
    AdminApp.uninstall(WEB_NAME)
    print WEB_NAME + " Application already uninstalled! "
# endIf
AdminConfig.save()

if (EAR_NAME in apps):
    AdminApp.uninstall(EAR_NAME)
    print EAR_NAME + " Application already uninstalled! "
#endIf
AdminConfig.save()

AdminApp.install(EAR_PATH, ['-appname', EAR_NAME])
print EAR_NAME + " Application already installed! "
AdminConfig.save()

AdminApp.install(WEB_PATH, ['-appname', WEB_NAME])
print WEB_NAME + " Application already installed! "
AdminConfig.save()

appManager = AdminControl.queryNames(
    "type=ApplicationManager,cell=" + CELL_NAME + ",node=" + NODE_NAME + ",process=" + SERVER_NAME + ",*")

AdminControl.invoke(appManager, "startApplication", EAR_NAME)
sleep(1)
AdminControl.invoke(appManager, "startApplication", WEB_NAME)
sleep(1)
