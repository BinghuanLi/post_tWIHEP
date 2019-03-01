#Make the job folders for all of the regions we want to study for the tW lepton+jets

import subprocess

baseDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/tWIHEPFramework/"

#for i in [" data"]:
#for i in [""," data"]:
#    continue
for i in [""]:
    #for k in [""," inv"]:
    #if k == " inv" and i == "":continue
    for k in [""]:
#        for j in ["", " ttbarReg", " wJetsReg"," wJets2"]:
#        for j in ["", " ttbarReg"," wJets2", " ttbar2"," sig2"]:
        #for j in [""]:
         for j in [" mva"]:
#        for j in [" ttbarReg", " wJetsReg"," wJets2"]:
#        for j in [" ttbarReg", " wJetsReg"]:
#        for j in [" ttbarReg", " wJets2"]:
#        for j in [" wJets2"]:
#        for j in [" wJetsReg"]:
 #       for j in [""]:
#            for l in [""," electron"]:
            for l in [""]:
                for m in [""]:
                #for m in [" clos", " All2L"," AlljesUp"," AlljesDown"]:
                #for m in [" All2L"," AlljesUp"," AlljesDown"]:
                #for m in [" All2L"]:
                    #for n in [""," systs"]:
                    for n in [""]:
                        if n == " systs" and not m == "": continue
#                    for n in [" systs"]:
                        #if i =="" and m=="": continue
                        if (j == " mva" or j==" Hjtagger") and not m =="": continue
                        if i == " data" and not (m == " All2L" or m == " All3L"): continue
                        #if i == " data" and not (m == "" and n == ""): continue
                        if i == " data" and j==" mva": continue
                        if (i == " flips" or i==" fakes") and (j==" lepSB" or j==" mva" or m==" jesUp" or m==" jesDown"): continue
                        if (i == " flips" ) and (j==" ttZctrl"): continue
                        if (m == " jesUp" or m== " jesDown" ) and (j==" ttWctrl" or j==" ttZctrl"): continue
                        print "makeHEPSubmit.py"+i+k+j+l+m+n
                        subprocess.call( "python "+baseDir+"utils/makeHEPSubmit.py skims"+i+k+j+l+m+n,shell=True)

#for i in ["jesUp","jesDown","jerUp","jerDown"]:
#    for j in [" electron"]:
#        subprocess.call( "python "+baseDir+"utils/makeHEPSubmit.py skims "+i+j,shell=True)

#for j in ["", " ttbarReg"," wJets2", " ttbar2"," sig2"]:
#    subprocess.call("python " +baseDir+"utils/makeHEPSubmit.py skims systs"+j,shell=True)
