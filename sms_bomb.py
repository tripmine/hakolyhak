#!/usr/bin/env python2.7
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
import re
import string
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import getpass

#SETUP YOUR EMAIL ADDRESS / PASSWORD
gmail_user = "FILL IN THE BLANKS"

gmail_pwd = "FILL IN THE BLANKS"

# Capture Target Cell Phone #
phonenum = raw_input('Enter Phone # [FORMAT=0001112222]: ')

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(False)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# The site we will navigate into, handling it's session
br.open("http://fonefinder.net")

# Select the first (index zero) form
br.select_form(nr=0)

# Input the info
br.form['npa'] = phonenum[:3]
br.form['nxx'] = phonenum[3:6]
br.form['thoublock'] = phonenum[6]

# Find Data
br.submit()

# Process Data
html = br.response().read()
soup = BeautifulSoup(html)

# Remove HTML Tags
text_parts = soup.findAll(text=True)
text = ' '.join(text_parts)

# Regex Applicable Data
prov_name = re.findall('[0-9]+ [0-9]+ \w+ \w+ \w+.+PROV', text)

# Convert List to String
L = [str(x) for x in prov_name]
s = string.join(L,' ')

# Display Server Feedback
print("FoneFinder Server Feedback: "+s)


# Provider Selection Menu
print("")
print("1.  Teleflip")
print( "2.  Alltel")		
print("3.  Ameritech")	
print("4.  ATT Wireless")
print("5.  Bellsouth")
print("6.  Boost")	
print("7.  CellularOne")
print("8   CellularOne MMS")
print("9.  Cingular")
print("10. Edge Wireles")
print("11. Sprint PCS")
print("12. T-Mobile")
print("13. Metro PCS")
print("14. Nextel")
print("15. O2")
print("16. Orange")
print("17. Qwest")
print("18. Rogers Wireless")
print("19. Telus Mobility")
print("20. US Cellular")
print("21. Verizon")
print("22. Virgin Mobile")
print("")

foundprov = input("SELECT THE APPLICABLE PROVIDER :")

provider=[]

if foundprov is 1:
  provider = "teleflip.com"
elif foundprov is 2:
  provider = "message.alltel.com"
elif foundprov is 3:
  provider = "paging.acswireless.com"
elif foundprov is 4:
  provider = "txt.att.net"
elif foundprov is 5:
  provider = "bellsouth.cl"
elif foundprov is 6:
  provider = "myboostmobile.com"
elif foundprov is 7:
  provider = "mobile.celloneusa.com"
elif foundprov is 8:
  provider = "mms.uscc.net"
elif foundprov is 9:
  provider = "mobile.mycingular.com"
elif foundprov is 10:
  provider = "sms.edgewireless.com"
elif foundprov is 11:
  provider = "messaging.sprintpcs.com"
elif foundprov is 12:
  provider = "tmomail.net"
elif foundprov is 13:
  provider = "mymetropcs.com"
elif foundprov is 14:
  provider = "messaging.nextel.com"
elif foundprov is 15:
  provider = "mobile.celloneusa.com"
elif foundprov is 16:
  provider = "mobile.celloneusa.com"
elif foundprov is 17:
  provider = "qwestmp.com"
elif foundprov is 18:
  provider = "pcs.rogers.com"
elif foundprov is 19:
  provider = "msg.telus.com"
elif foundprov is 20:
  provider = "email.uscc.net"
elif foundprov is 21:
  provider = "vtext.com"
elif foundprov is 22:
  provider = "vmobl.com"

sms_email = str(phonenum+"@"+provider)

print("")
print("SMS Recipient Address : " +sms_email)

email_count = raw_input("Enter Email Quantity : ")
email_qty = int(email_count)
count = 1

# SEND EMAIL

email_subj = raw_input("Enter Subject ")
email_body = raw_input("Type Message To Send [press enter when complete] ")

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os


def mail(to, subject, text):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   Encoders.encode_base64(part)
   

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

while count <= email_qty:
  mail(sms_email, email_subj, email_body)
  count += 1
