#
# Module: IEController
# Author: Mayukh Bose
# Version: 0.0.3
# Purpose: To control an Internet Explorer window.
# Modifications (push down list):
# 2005-February-11th - Added GetCurrentUrl() function. Also replaced "pass"
# with "time.sleep(0.1)" in PollWhileBusy(). Both improvements were suggested
# by David L. Wooden
# 2005-January-9th - Used strip() on lots of user params. Also added code to
# find a window by its URL.
# 2004-November-20th - Released module to the public
#
# Copyright (c) 2004, Mayukh Bose
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#    Redistributions of source code must retain the above copyright notice, this list
# of conditions and the following disclaimer.
#    Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution.
#    Neither the name of Mayukh Bose nor the names of other contributors may be used to
# endorse or promote products derived from this software without specific prior written
# permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

from win32com.client import Dispatch
import time
import re
import urllib

class IEController:
    """Class to control an Internet Explorer Window"""
    def __init__(self, window_num = 0, window_url = ''):
        if window_num <= 0 and window_url == '':
            self.ie = self.__CreateNewIE()
        else:
            self.ie = self.__FindOpenIE(window_num, window_url)
            
    def __CreateNewIE(self):
        ie = Dispatch("InternetExplorer.Application")
        ie.Visible = 1
        return ie

    def __FindOpenIE(self, window_num=0, window_url=''):
        # CLSID for ShellWindows
        clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
        ShellWindows = Dispatch(clsid)
        if (window_url != ''):
            window_url = window_url.lower()
            for i in range(ShellWindows.Count):
                if ShellWindows[i].LocationURL.lower().find(window_url) > -1:
                    return ShellWindows[i]
            return self.__CreateNewIE()
          
        if (ShellWindows.Count < 1 or window_num > ShellWindows.Count or window_num <= 0):
            return self.__CreateNewIE()
        else:
            return ShellWindows[window_num - 1]



    def GetCurrentUrl(self):
        return self.ie.LocationURL
    
    def CloseWindow(self):
        self.ie.Quit()
        self.ie = None
        
    def PollWhileBusy(self):        
        while self.ie.Busy:
            time.sleep(0.1)
            
    def Navigate(self, url):
        self.ie.Navigate(url)
        self.PollWhileBusy()

    def GetDocumentHTML(self):
        doc = self.ie.Document    
        return doc.body.outerHTML

    def GetDocumentText(self):
        doc = self.ie.Document
        return doc.body.outerText

    #changed here
    def ClickLink(self, linktext):
        linktext = linktext.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all
        
        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'A'):
                #print elem
                hreftext = elem.outerText
                hreftext = hreftext.lower().strip()
                
                if linktext == hreftext:
                    elem.click()
                    self.PollWhileBusy()
                    return 1
                
        #raise 'Link ' + linktext + ' was not found.'
        
    def ClickButton(self, name = '', caption = ''):
        if (caption == '' and name == ''):
            raise 'ClickButton(): Please specify either a button name or a button caption.'

        if (name != ''):    
            itemtocheck = name.lower().strip()
        else:
            itemtocheck = caption.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all
        
        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'INPUT'):
                type = elem.getAttribute('type')
                type = type.upper()
                if (type == "IMAGE" or type == "SUBMIT" or type == "BUTTON"):
                    if name != '':
                        itemattrib = elem.getAttribute('name')
                    else:
                        itemattrib = elem.getAttribute('value')
                    itemattrib = itemattrib.lower().strip()
                    if itemattrib == itemtocheck:
                        elem.click()
                        self.PollWhileBusy()
                        return 1
                
        raise 'Button ' + itemtocheck + ' was not found.'

    def GetInputValue(self, name):
        name = name.lower().strip()
        print(name)
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'INPUT'):
                itemname = elem.getAttribute('name')
                itemname = itemname.lower().strip()
                print(itemname)
                if itemname == name:
                    value = elem.getAttribute('value')
                    return value
        
        raise 'Input Element ' + name + ' was not found.'

    def SetInputValue(self, name, value):
        name = name.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'INPUT'):
                itemname = elem.getAttribute('name')
                itemname = itemname.lower().strip()
                if itemname == name:
                    elem.setAttribute('value', value)
                    return 1
                
        raise 'Input Element ' + name + ' was not found.'

    def GetTextArea(self, name):
        name = name.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'TEXTAREA'):
                itemname = elem.getAttribute('name')
                itemname = itemname.lower().strip()
                if itemname == name:
                    value = elem.outerText
                    return value
        
        raise 'Text Area ' + name + ' was not found.'

    def SetTextArea(self, name, value):
        name = name.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'TEXTAREA'):
                itemname = elem.getAttribute('name')
                itemname = itemname.lower().strip()
                if itemname == name:
                    elem.outerText = value
                    return 1
        
        raise 'Text Area ' + name + ' was not found.'

    def GetSelectValue(self, name):
        name = name.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'SELECT'):
                itemname = elem.getAttribute('name')
                itemname = itemname.lower().strip()
                if itemname == name:
                    index = elem.selectedIndex
                    option = elem.options(index)
                    optionvalue = option.getAttribute('value')
                    optiontext = option.innerHTML
                    return optionvalue, optiontext
        
        raise 'Select ' + name + ' was not found.'

    def SetSelectValue(self, selname, optionvalue = '', optioncaption = ''):
        if (optioncaption == '' and optionvalue == ''):
            raise 'SetSelectValue(): Please specify either an option value or option caption.'

        if (optionvalue != ''):    
            itemtocheck = optionvalue.lower().strip()
        else:
            itemtocheck = optioncaption.lower().strip()
        selname = selname.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'SELECT'):
                elemname = elem.getAttribute('name')
                elemname = elemname.lower().strip()
                if elemname == selname:
                    for j in range(elem.length):
                        option = elem.options(j)
                        if (optionvalue != ''):
                            itemattrib = option.getAttribute('value')
                        else:
                            itemattrib = option.innerHTML
                        itemattrib = itemattrib.lower().strip()
                        if itemattrib == itemtocheck:
                            option.selected = 1
                            return 1;
                    raise 'Option ' + itemtocheck + ' was not found.'

        raise 'Select ' + selname + ' was not found.'


    # I have changed here
    def GetListSelection(self, selname):
        selname = selname.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all
        listelems = []

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            #print elem
            if (elem.tagName == 'SELECT'):
                elemname = elem.getAttribute('name')
                elemname = elemname.lower().strip()
                #print elemname
                if elemname == selname:
                    for j in range(elem.length):
                        option = elem.options(j)
                        optiontext = option.innerHTML
                        listelems.append(optiontext)
                        #if option.selected:
                        #    optionvalue = option.getAttribute('value')
                        #    optiontext = option.innerHTML
                        #    listtuple = (optionvalue, optiontext)
                        #    listelems.append(listtuple)
                    return listelems
        #raise 'List Selection ' + selname + ' was not found.'

    def SetAllListElements(self, selname, selected = 0):
        selname = selname.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'SELECT'):
                elemname = elem.getAttribute('name')
                elemname = elemname.lower().strip()
                if elemname == selname:
                    for j in range(elem.length):
                        option = elem.options(j)
                        option.selected = selected
                    return 1
        raise 'List Selection ' + selname + ' was not found.'

    def SetListSelection(self, selname, optionvalue = '', optioncaption = '', selected = 1):
        if (optioncaption == '' and optionvalue == ''):
            raise 'SetSelectValue(): Please specify either an option value or option caption.'

        if (optionvalue != ''):    
            itemtocheck = optionvalue.lower().strip()
        else:
            itemtocheck = optioncaption.lower().strip()
        selname = selname.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'SELECT'):
                elemname = elem.getAttribute('name')
                elemname = elemname.lower().strip()
                if elemname == selname:
                    for j in range(elem.length):
                        option = elem.options(j)
                        if (optionvalue != ''):
                            itemattrib = option.getAttribute('value')
                        else:
                            itemattrib = option.innerHTML
                        itemattrib = itemattrib.lower().strip()
                        if itemattrib == itemtocheck:
                            option.selected = selected
                            return 1
                    raise 'Option ' + itemtocheck + ' was not found.'

        raise 'List Selection ' + selname + ' was not found.'

    def GetCheckBoxState(self, cbname):
        cbname = cbname.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'INPUT'):
                itemname = elem.getAttribute('name')
                itemname = itemname.lower().strip()
                print itemname
                if itemname == cbname:
                    checked = elem.getAttribute('checked')
                    return checked
        
        raise 'Check Box ' + cbname + ' was not found.'
        
    #I also changed here
    def SetCheckBoxState(self, cbname, checked = 1):
        cbname = cbname.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'INPUT'):
                itemname = elem.getAttribute('name')
                itemname = itemname.lower().strip()
                if itemname == cbname:
                    elem.click()
                    #elem.setAttribute('checked', checked)
                    return 1
        
        raise 'Check Box ' + cbname + ' was not found.'    
        

    def GetRadioValue(self, rbname):
        return self.GetInputValue(rbname)

    def SetRadioValue(self, rbname, rbvalue, checked = 1):
        rbname = rbname.lower().strip()
        rbvalue = rbvalue.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'INPUT'):
                itemname = elem.getAttribute('name')
                itemname = itemname.lower().strip()
                if itemname == rbname:
                    itemvalue = elem.getAttribute('value')
                    itemvalue = itemvalue.lower().strip()
                    if itemvalue == rbvalue:
                        elem.setAttribute('checked', checked)
                        return 1
        
        raise 'Radio Button ' + rbname + ' was not found.'

    def SubmitForm(self, formname):
        formname = formname.lower().strip()
        doc = self.ie.Document
        elemcoll = doc.all

        for i in range(elemcoll.length):
            elem = elemcoll.item(i)
            if (elem.tagName == 'FORM'):
                itemname = elem.getAttribute('name')
                itemname = itemname.lower().strip()
                if itemname == formname:
                    elem.submit()
                    self.PollWhileBusy()
                    return 1
        
        raise 'Form ' + formname + ' was not found.'    

def ShowMessage(msg, title='Info'):
    "Function to show messages to windows users. This is only used by the demo."
    from win32api import MessageBox
    MessageBox(0, msg, title)

def IterateWeb(url,accessed_list, initial_url):
    accessed_list.append(url)
    ie_temp =IEController()
    ie_temp.Navigate(url)
    doc = ie_temp.ie.Document
    elemcoll = doc.all
    url_list=[]
    for i in range(elemcoll.length):
        elem = elemcoll.item(i)
        if((bool(re.search('http://',str(elem),re.IGNORECASE)))&(not bool(re.search('.pdf',str(elem),re.IGNORECASE)))&(not bool(re.search('.xml',str(elem),re.IGNORECASE)))&(initial_url in str(elem))):
            url_list.append(str(elem))
    #print url_list
    ie_temp.CloseWindow()
    if(len(url_list)==0):
        print "No Url here"
    else: 
        for i in range(len(url_list)):
            flag=0
            for j in range(len(accessed_list)):
                if (url_list[i]==accessed_list[j]):
                    flag=1
                    break
            if(flag==0):
                IterateWeb(url_list[i],accessed_list, initial_url )
          
    
if __name__ == "__main__":
    #ShowMessage('Creating a new IE object....')
    

   # while 1:
   #     ie = IEController()
   #     ie.Navigate("https://www.studentinsurance.com/PearceSite/enroll/Intro.asp?id=273&db=Pearce&Enroll=waive")
   #     a=ie.GetCheckBoxState('verifyunderstand')
   #     if(a==False):
   #         b=ie.SetCheckBoxState( 'verifyunderstand')
   #         #print b
   #     ie.ClickButton('b1')
   #     ins_name=ie.GetListSelection('insid')
   #     #print ins_name
   #     #ie.CloseWindow()
   #     if(ins_name!=None):
   #         break
   #     else:
   #         ie.CloseWindow()
        
        


 
    ie = IEController()
    ie.Navigate("http://www.google.com/index.html")
    temp1=ie.GetCurrentUrl()
    #print temp1
    ie.SetInputValue('q','international student health insurance plan')
    ie.ClickButton(name='btnk',caption='')
    temp=ie.GetCurrentUrl()
    #print temp
    ie.CloseWindow()

    ie1 =IEController()
    ie1.Navigate(temp)
    ie1.ClickLink('aaa')
    doc = ie1.ie.Document
    elemcoll = doc.all
    temp_insurance_list=[]
    for i in range(elemcoll.length):
        elem = elemcoll.item(i)
        if((bool(re.search('http://',str(elem),re.IGNORECASE)))&(not bool(re.search('www.youtube.com',str(elem),re.IGNORECASE)))&(not bool(re.search('google.com/', str(elem), re.IGNORECASE)))&(not bool(str(elem)=='[object]'))&(not bool(re.search('webcache', str(elem), re.IGNORECASE)))):
            temp_insurance_list.append(str(elem))
    #print temp_insurance_list
    insurance_list=[]
    for i in range(len(temp_insurance_list)):
        insurance_list.append(temp_insurance_list[i])

    for i in range(len(temp_insurance_list)):
        for j in range(i+1, len(temp_insurance_list)):
            if((temp_insurance_list[i] in temp_insurance_list[j])&(temp_insurance_list[j] in insurance_list)):
                insurance_list.remove(temp_insurance_list[j])
    print insurance_list
        
        
    #for i in range(0,10):
    #    ie=IEController()
    #    ie.Navigate(insurance_list[i])
    #ie1.CloseWindow()

    ie1 =IEController()
    ie1.Navigate('http://studenthealth.oregonstate.edu/internationalplan')
    ie1.ClickLink('aaa')
    doc = ie1.ie.Document
    elemcoll = doc.all
    for i in range(elemcoll.length):
        elem = elemcoll.item(i)
        print elem
    urllib.urlretrieve("http://studenthealth.oregonstate.edu/sites/default/files/docs/international_broch_201213.pdf", "C:\\Download\\insurance1.pdf")
   

    ie1 =IEController()
    ie1.Navigate('http://www.isoa.org/iso_med_main.aspx')
    ie1.ClickLink('aaa')
    doc = ie1.ie.Document
    elemcoll = doc.all
    for i in range(elemcoll.length):
        elem = elemcoll.item(i)
        if(elem.tagName=='TABLE'):
            print elem.outerText


    accessed_list=[]
    IterateWeb('http://studenthealth.oregonstate.edu/internationalplan',accessed_list,'http://studenthealth.oregonstate.edu')
    print accessed_list

    


