#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QFile, QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
        QMessageBox, QTextEdit)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupFileMenu()
        self.setupHelpMenu()
        self.setupEditor()

        self.setCentralWidget(self.editor)
        self.setWindowTitle("Syntax Highlighter")

    def about(self):
        QMessageBox.about(self, "About Syntax Highlighter",
                "<p>The <b>Syntax Highlighter</b> example shows how to " \
                "perform simple syntax highlighting by subclassing the " \
                "QSyntaxHighlighter class and describing highlighting " \
                "rules using regular expressions.</p>")

    def newFile(self):
        self.editor.clear()

    def openFile(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open File", '',
                    "C++ Files (*.cpp *.h)")

        if path:
            inFile = QFile(path)
            if inFile.open(QFile.ReadOnly | QFile.Text):
                text = inFile.readAll()

                try:
                    # Python v3.
                    text = str(text, encoding='ascii')
                except TypeError:
                    # Python v2.
                    text = str(text)

                self.editor.setPlainText(text)

    def setupEditor(self):
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)

        self.editor = QTextEdit()
        self.editor.setFont(font)

        self.highlighter = Highlighter(self.editor.document())

    def setupFileMenu(self):
        fileMenu = QMenu("&File", self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction("&New...", self.newFile, "Ctrl+N")
        fileMenu.addAction("&Open...", self.openFile, "Ctrl+O")
        fileMenu.addAction("E&xit", QApplication.instance().quit, "Ctrl+Q")

    def setupHelpMenu(self):
        helpMenu = QMenu("&Help", self)
        self.menuBar().addMenu(helpMenu)

        helpMenu.addAction("&About", self.about)
        helpMenu.addAction("About &Qt", QApplication.instance().aboutQt)


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)

        keywordPatterns_2 = ["\\bchar\\b","\\bCHAR\\b", "\\bclass\\b", "\\bconst\\b",
                "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
                "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
                "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
                "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
                "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
                "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
                "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
                "\\bvolatile\\b"]

        keywordPatterns = [
            "\\bADD\\b",
            "\\bEXTERNAL\\b",
            "\\bPROCEDURE\\b",
            "\\bALL\\b",
            "\\bFETCH\\b",
            "\\bPUBLIC\\b",
            "\\bALTER\\b",
            "\\bFILE\\b",
            "\\bRAISERROR\\b",
            "\\bAND\\b",
            "\\bFILLFACTOR\\b",
            "\\bREAD\\b",
            "\\bANY\\b",
            "\\bFOR\\b",
            "\\bREADTEXT\\b",
            "\\bAS\\b",
            "\\bFOREIGN\\b",
            "\\bRECONFIGURE\\b",
            "\\bASC\\b",
            "\\bFREETEXT\\b",
            "\\bREFERENCES\\b",
            "\\bAUTHORIZATION\\b",
            "\\bFREETEXTTABLE\\b",
            "\\bREPLICATION\\b",
            "\\bBACKUP\\b",
            "\\bFROM\\b",
            "\\bRESTORE\\b",
            "\\bBEGIN\\b",
            "\\bFULL\\b",
            "\\bRESTRICT\\b",
            "\\bBETWEEN\\b",
            "\\bFUNCTION\\b",
            "\\bRETURN\\b",
            "\\bBREAK\\b",
            "\\bGOTO\\b",
            "\\bREVERT\\b",
            "\\bBROWSE\\b",
            "\\bGRANT\\b",
            "\\bREVOKE\\b",
            "\\bBULK\\b",
            "\\bGROUP\\b",
            "\\bRIGHT\\b",
            "\\bBY\\b",
            "\\bHAVING\\b",
            "\\bROLLBACK\\b",
            "\\bCASCADE\\b",
            "\\bHOLDLOCK\\b",
            "\\bROWCOUNT\\b",
            "\\bCASE\\b",
            "\\bIDENTITY\\b",
            "\\bROWGUIDCOL\\b",
            "\\bCHECK\\b",
            "\\bIDENTITY_INSERT\\b",
            "\\bRULE\\b",
            "\\bCHECKPOINT\\b",
            "\\bIDENTITYCOL\\b",
            "\\bSAVE\\b",
            "\\bCLOSE\\b",
            "\\bIF\\b",
            "\\bSCHEMA\\b",
            "\\bCLUSTERED\\b",
            "\\bIN\\b",
            "\\bSECURITYAUDIT\\b",
            "\\bCOALESCE\\b",
            "\\bINDEX\\b",
            "\\bSELECT\\b",
            "\\bCOLLATE\\b",
            "\\bINNER\\b",
            "\\bSEMANTICKEYPHRASETABLE\\b",
            "\\bCOLUMN\\b",
            "\\bINSERT\\b",
            "\\bSEMANTICSIMILARITYDETAILSTABLE\\b",
            "\\bCOMMIT\\b",
            "\\bINTERSECT\\b",
            "\\bSEMANTICSIMILARITYTABLE\\b",
            "\\bCOMPUTE\\b",
            "\\bINTO\\b",
            "\\bSESSION_USER\\b",
            "\\bCONSTRAINT\\b",
            "\\bIS\\b",
            "\\bSET\\b",
            "\\bCONTAINS\\b",
            "\\bJOIN\\b",
            "\\bSETUSER\\b",
            "\\bCONTAINSTABLE\\b",
            "\\bKEY\\b",
            "\\bSHUTDOWN\\b",
            "\\bCONTINUE\\b",
            "\\bKILL\\b",
            "\\bSOME\\b",
            "\\bCONVERT\\b",
            "\\bLEFT\\b",
            "\\bSTATISTICS\\b",
            "\\bCREATE\\b",
            "\\bLIKE\\b",
            "\\bSYSTEM_USER\\b",
            "\\bCROSS\\b",
            "\\bLINENO\\b",
            "\\bTABLE\\b",
            "\\bCURRENT\\b",
            "\\bLOAD\\b",
            "\\bTABLESAMPLE\\b",
            "\\bCURRENT_DATE\\b",
            "\\bMERGE\\b",
            "\\bTEXTSIZE\\b",
            "\\bCURRENT_TIME\\b",
            "\\bNATIONAL\\b",
            "\\bTHEN\\b",
            "\\bCURRENT_TIMESTAMP\\b",
            "\\bNOCHECK\\b",
            "\\bTO\\b",
            "\\bCURRENT_USER\\b",
            "\\bNONCLUSTERED\\b",
            "\\bTOP\\b",
            "\\bCURSOR\\b",
            "\\bNOT\\b",
            "\\bTRAN\\b",
            "\\bDATABASE\\b",
            "\\bNULL\\b",
            "\\bTRANSACTION\\b",
            "\\bDBCC\\b",
            "\\bNULLIF\\b",
            "\\bTRIGGER\\b",
            "\\bDEALLOCATE\\b",
            "\\bOF\\b",
            "\\bTRUNCATE\\b",
            "\\bDECLARE\\b",
            "\\bOFF\\b",
            "\\bTRY_CONVERT\\b",
            "\\bDEFAULT\\b",
            "\\bOFFSETS\\b",
            "\\bTSEQUAL\\b",
            "\\bDELETE\\b",
            "\\bON\\b",
            "\\bUNION\\b",
            "\\bDENY\\b",
            "\\bOPEN\\b",
            "\\bUNIQUE\\b",
            "\\bDESC\\b",
            "\\bOPENDATASOURCE\\b",
            "\\bUNPIVOT\\b",
            "\\bDISK\\b",
            "\\bOPENQUERY\\b",
            "\\bUPDATE\\b",
            "\\bDISTINCT\\b",
            "\\bOPENROWSET\\b",
            "\\bUPDATETEXT\\b",
            "\\bDISTRIBUTED\\b",
            "\\bOPENXML\\b",
            "\\bUSE\\b",
            "\\bDOUBLE\\b",
            "\\bOPTION\\b",
            "\\bUSER\\b",
            "\\bDROP\\b",
            "\\bOR\\b",
            "\\bVALUES\\b",
            "\\bDUMP\\b",
            "\\bORDER\\b",
            "\\bVARYING\\b",
            "\\bELSE\\b",
            "\\bOUTER\\b",
            "\\bVIEW\\b",
            "\\bEND\\b",
            "\\bOVER\\b",
            "\\bWAITFOR\\b",
            "\\bERRLVL\\b",
            "\\bPERCENT\\b",
            "\\bWHEN\\b",
            "\\bESCAPE\\b",
            "\\bPIVOT\\b",
            "\\bWHERE\\b",
            "\\bEXCEPT\\b",
            "\\bPLAN\\b",
            "\\bWHILE\\b",
            "\\bEXEC\\b", "\\bPRECISION\\b", "\\bWITH\\b",
            "\\bEXECUTE\\b", "\\bPRIMARY\\b", "\\bWITHIN GROUP\\b",
            "\\bEXISTS\\b", "\\bPRINT\\b", "\\bWRITETEXT\\b",
            "\\bEXIT\\b", "\\bPROC\\b",
"\\badd\\b",
"\\bexternal\\b",
"\\bprocedure\\b",
"\\ball\\b",
"\\bfetch\\b",
"\\bpublic\\b",
"\\balter\\b",
"\\bfile\\b",
"\\braiserror\\b",
"\\band\\b",
"\\bfillfactor\\b",
"\\bread\\b",
"\\bany\\b",
"\\bfor\\b",
"\\breadtext\\b",
"\\bas\\b",
"\\bforeign\\b",
"\\breconfigure\\b",
"\\basc\\b",
"\\bfreetext\\b",
"\\breferences\\b",
"\\bauthorization\\b",
"\\bfreetexttable\\b",
"\\breplication\\b",
"\\bbackup\\b",
"\\bfrom\\b",
"\\brestore\\b",
"\\bbegin\\b",
"\\bfull\\b",
"\\brestrict\\b",
"\\bbetween\\b",
"\\bfunction\\b",
"\\breturn\\b",
"\\bbreak\\b",
"\\bgoto\\b",
"\\brevert\\b",
"\\bbrowse\\b",
"\\bgrant\\b",
"\\brevoke\\b",
"\\bbulk\\b",
"\\bgroup\\b",
"\\bright\\b",
"\\bby\\b",
"\\bhaving\\b",
"\\brollback\\b",
"\\bcascade\\b",
"\\bholdlock\\b",
"\\browcount\\b",
"\\bcase\\b",
"\\bidentity\\b",
"\\browguidcol\\b",
"\\bcheck\\b",
"\\bidentity_insert\\b",
"\\brule\\b",
"\\bcheckpoint\\b",
"\\bidentitycol\\b",
"\\bsave\\b",
"\\bclose\\b",
"\\bif\\b",
"\\bschema\\b",
"\\bclustered\\b",
"\\bin\\b",
"\\bsecurityaudit\\b",
"\\bcoalesce\\b",
"\\bindex\\b",
"\\bselect\\b",
"\\bcollate\\b",
"\\binner\\b",
"\\bsemantickeyphrasetable\\b",
"\\bcolumn\\b",
"\\binsert\\b",
"\\bsemanticsimilaritydetailstable\\b",
"\\bcommit\\b",
"\\bintersect\\b",
"\\bsemanticsimilaritytable\\b",
"\\bcompute\\b",
"\\binto\\b",
"\\bsession_user\\b",
"\\bconstraint\\b",
"\\bis\\b",
"\\bset\\b",
"\\bcontains\\b",
"\\bjoin\\b",
"\\bsetuser\\b",
"\\bcontainstable\\b",
"\\bkey\\b",
"\\bshutdown\\b",
"\\bcontinue\\b",
"\\bkill\\b",
"\\bsome\\b",
"\\bconvert\\b",
"\\bleft\\b",
"\\bstatistics\\b",
"\\bcreate\\b",
"\\blike\\b",
"\\bsystem_user\\b",
"\\bcross\\b",
"\\blineno\\b",
"\\btable\\b",
"\\bcurrent\\b",
"\\bload\\b",
"\\btablesample\\b",
"\\bcurrent_date\\b",
"\\bmerge\\b",
"\\btextsize\\b",
"\\bcurrent_time\\b",
"\\bnational\\b",
"\\bthen\\b",
"\\bcurrent_timestamp\\b",
"\\bnocheck\\b",
"\\bto\\b",
"\\bcurrent_user\\b",
"\\bnonclustered\\b",
"\\btop\\b",
"\\bcursor\\b",
"\\bnot\\b",
"\\btran\\b",
"\\bdatabase\\b",
"\\bnull\\b",
"\\btransaction\\b",
"\\bdbcc\\b",
"\\bnullif\\b",
"\\btrigger\\b",
"\\bdeallocate\\b",
"\\bof\\b",
"\\btruncate\\b",
"\\bdeclare\\b",
"\\boff\\b",
"\\btry_convert\\b",
"\\bdefault\\b",
"\\boffsets\\b",
"\\btsequal\\b",
"\\bdelete\\b",
"\\bon\\b",
"\\bunion\\b",
"\\bdeny\\b",
"\\bopen\\b",
"\\bunique\\b",
"\\bdesc\\b",
"\\bopendatasource\\b",
"\\bunpivot\\b",
"\\bdisk\\b",
"\\bopenquery\\b",
"\\bupdate\\b",
"\\bdistinct\\b",
"\\bopenrowset\\b",
"\\bupdatetext\\b",
"\\bdistributed\\b",
"\\bopenxml\\b",
"\\buse\\b",
"\\bdouble\\b",
"\\boption\\b",
"\\buser\\b",
"\\bdrop\\b",
"\\bor\\b",
"\\bvalues\\b",
"\\bdump\\b",
"\\border\\b",
"\\bvarying\\b",
"\\belse\\b",
"\\bouter\\b",
"\\bview\\b",
"\\bend\\b",
"\\bover\\b",
"\\bwaitfor\\b",
"\\berrlvl\\b",
"\\bpercent\\b",
"\\bwhen\\b",
"\\bescape\\b",
"\\bpivot\\b",
"\\bwhere\\b",
"\\bexcept\\b",
"\\bplan\\b",
"\\bwhile\\b",
"\\bexec\\b","\\bprecision\\b","\\bwith\\b",
"\\bexecute\\b","\\bprimary\\b","\\bwithin group\\b",
"\\bexists\\b","\\bprint\\b","\\bwritetext\\b",
"\\bexit\\b","\\bproc\\b"
             ]



        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(Qt.darkMagenta)
        self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))


        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(Qt.red)
        self.highlightingRules.append((QRegExp("//[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.red)

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(Qt.darkGreen)
        self.highlightingRules.append((QRegExp("\".*\""), quotationFormat))

        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(Qt.blue)
        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 512)
    window.show()
    sys.exit(app.exec_())