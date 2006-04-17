# -*- coding: UTF-8 -*-
"""
module vinreport.py
-----------------------------------------------------------------------------

 Vinetto : a forensics tool to examine Thumbs.db files
 Copyright (C) 2005, 2006 by Michel Roukine
 
This file is part of Vinetto.
 
 Vinetto is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License as published
 by the Free Software Foundation; either version 2 of the License, or (at
 your option) any later version.
 
 Vinetto is distributed in the hope that it will be
 useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.
 
 You should have received a copy of the GNU General Public License along
 with the vinetto package; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 
-----------------------------------------------------------------------------
"""

__revision__ = "$Revision: 47 $"
__version__ = "0.01"
__author__ = 'Michel Roukine'

HtHeader = []
HtPicRow = []
HtFooter = []
IMGTAG = "<IMG SRC=\"./__TNID__.jpg\" ALT=\"__TNNAME__\">"

from time import time, ctime
        

class Report:
    """ Vinetto report SuperClass.  """
    def __init__ (self, target, outputdir, verstr):
        """ Initialize a new Report instance.  """
        self.target = target
        self.outputdir = outputdir
        self.verstr = verstr


class HtRep(Report):
    """ Html vinetto elementary mode report Class.  """
    def __init__ (self, tDBfname, outputdir, verstr):
        """ Initialize a new HtRep instance.  """
        Report.__init__(self, tDBfname, outputdir, verstr)
        self.rownumber = 0
        
        separatorID = 0
        
        for ligne in open("/usr/share/vinetto/HtRepTemplate.html",
                          "r").readlines():
            if ligne.find("__ITS__") >= 0:
                separatorID += 1
                continue
                
            if separatorID == 0:
                HtHeader.append(ligne)
            elif separatorID == 1:
                HtPicRow.append(ligne)
            elif separatorID == 2:
                HtFooter.append(ligne)
              
        self.TNidList = []
        self.TNtsList = []
        self.TNnameList = []
        
        self.repfile = open(outputdir + "index.html","w")
        
        
    def headwrite (self, REtst):
        """ Writes report header.  """
        
        for ligne in HtHeader:
            ligne = ligne.replace("__DATEREPORT__", "Report date : " + ctime(time()))
            ligne = ligne.replace("__TDBFNAME__", "File : " + self.target)
            ligne = ligne.replace("__ROOTENTRYTST__", \
                                  "Root Entry modify timestamp : " + REtst)
            self.repfile.write(ligne)
 
    
    def addTN (self, TNid, TNtimestamp, TNname):
        """ Sotre thumbnails elements.  """
        self.TNidList.append(TNid)
        self.TNtsList.append(TNtimestamp)
        self.TNnameList.append(TNname)
        
        if len(self.TNidList) >= 5 :
            self.rowflush()

    
    def close(self, Typ1Extracted, Typ2Extracted):
        """ Terminate processing HtRep instance.  """
        if len(self.TNidList) > 0:
            self.rowflush()
            
        typextract = ""
        if Typ1Extracted > 0:
            typextract = str(Typ1Extracted) + " Type 1 thumbnails extracted to " + self.outputdir
        if Typ2Extracted > 0:
            typextract += "<BR>" + str(Typ2Extracted) + " Type 2 thumbnails extracted to " + self.outputdir
            
        for ligne in HtFooter:
            ligne = ligne.replace("__TYPEXTRACT__", typextract)
            ligne = ligne.replace("__VVERSION__", "Vinetto " + self.verstr)
            self.repfile.write(ligne)
        self.repfile.close()

        
    def rowflush(self):
        """ Process a report line.  """
        self.rownumber += 1
        for ligne in HtPicRow:
            ligne = ligne.replace("__ROWNUMBER__", str(self.rownumber))
            for j in range(len(self.TNidList)):
                ligne = ligne.replace("__TNfilled__" + str(j), "1")
                buff = IMGTAG.replace("__TNID__", self.TNidList[j])
                buff = buff.replace("__TNNAME__", self.TNnameList[j])
                ligne = ligne.replace("__IMGTAG__" + str(j), buff)                
                ligne = ligne.replace("__TNID__" + str(j), self.TNidList[j])
            for j in range(len(self.TNidList),5):
                ligne = ligne.replace("__TNfilled__" + str(j), "0")
                ligne = ligne.replace("__IMGTAG__" + str(j), " &nbsp; ")
                ligne = ligne.replace("__TNID__" + str(j), " ")

            self.repfile.write(ligne)
            
        self.repfile.write("<TABLE WIDTH=\"720\"><TR><TD>&nbsp;</TD></TR>" + \
                           "<TR><TD><P ALIGN=\"LEFT\">")
        for i in range(len(self.TNidList)):
            self.repfile.write("<TT>" + self.TNidList[i] + " -- " + \
                               self.TNtsList[i] + " -- " + \
                               self.TNnameList[i] + "</TT><BR>\n")
        self.repfile.write("</P></TD></TR><TR><TD>&nbsp;</TD></TR></TABLE>")
        
        self.TNidList = []
        self.TNtsList = []
        self.TNnameList = []
