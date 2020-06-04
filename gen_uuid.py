import sys
import uuid

from burp import IBurpExtender, IContextMenuFactory
from java.awt import Toolkit
from java.awt.datatransfer import StringSelection
from java.io import PrintWriter
from javax.swing import JMenuItem, JMenu
from java.util import ArrayList, LinkedList


class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        sys.stdout = callbacks.getStdout()
        self.callbacks = callbacks
        self.stdout = PrintWriter(self.callbacks.getStdout(), True)
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName("Generate UUID")
        callbacks.registerContextMenuFactory(self)
        return

    def createMenuItems(self, invocation):
        self.context = invocation
        mainMenu = ArrayList()
        #menu = LinkedList()
        subMenu = LinkedList()
        mainMenu = JMenuItem("Generate a UUID string and copy to clipbloard")
        menuItem1 = JMenuItem("UUID version 1", actionPerformed=self.genUUID)
        #menuItem2 = JMenuItem("UUID verion 2", actionPerformed=self.genUUID)
        subMenu.add(menuItem1)
        #subMenu.add(menuItem2)
        #mainMenu.add(subMenu)
        return subMenu 

    def genUUID(self, event):
        """
        Generate the UUID string

        Parameters
        ----------
        version: int
            UUID version to use
        """
        version = 4
        if version == 1:
            genuuid = uuid.uuid1()
        elif version == 2:
            genuuid = uuid.uuid2()
        elif version == 3:
            genuuid = uuid.uuid3()
        elif version == 4:
            genuuid = uuid.uuid4()
        elif version == 5:
            genuuid = uuid.uuid5()
        else:
            genuuid = None
        #print(dir(self.copy_to_clipboard))
        #return genuuid.hex
        #self.stdout.println(genuuid.hex)
        clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
        clipboard.setContents(StringSelection(str(genuuid)), None)
        print('Generated UUI: {}'.format(genuuid))
