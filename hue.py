import requests

with open("input.txt") as fd:
  thelist = fd.readlines()

def genqstr(parms):
  rstr=""
  for k in parms.keys():
    rstr+="&"+k+"="+parms[k]
  return rstr[1:]

def rget(url):
  tries = 0
  while tries<5:
   try:
    return requests.get(url).text
   except:
    print "Error, retry"
    tries +=1
  return ""

with open("output.txt", "a") as fd:
  for i in thelist:
    ii=i.strip()
    print ii
    r=rget(ii)
    if "have an error" in r:
      print "UNTESTABLE"
      with open("untest.txt", "a") as fdt:
        fdt.write(ii+"\n")
      continue
    if len(r) ==0:
      print "ERROR"
      with open("untest.txt", "a") as fdt:
        fdt.write(ii+"\n")
      continue
    if "?" not in ii:
      print "no GET vars, skip"
      with open("untest.txt", "a") as fdt:
        fdt.write(ii+"\n")
      continue
    url,qstr = ii.split("?", 1)
    parms = {}
    if "&" in qstr:
      for qs in qstr.split("&"):
        try:
         k,v = qs.split("=", 1)
        except:
         k,v = qs, ""
        parms[k]=v
    else:
      try:
       k,v = qstr.split("=", 1)
      except:
       k,v = qstr, ""
      parms[k]=v
    for parm in parms.keys():
      oldparm = parms[parm]
      print "testing "+parm
      for l in "\'();\"":
        parms[parm] = oldparm+l
        r=rget(url+"?"+genqstr(parms))
        parms[parm] = oldparm
        if "have an error" in r:
          fd.write(url+"?"+genqstr(parms)+","+parm+"\n")
          print "GOTCHI"
