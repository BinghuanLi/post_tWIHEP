from ROOT import *

#import sys,os,math,weightProcesses
import sys,os,math
import optparse
import distutils.util

regPerCat={
"SubCat2l":["DiLepRegion"],
"DNNCat":["DiLepRegion"],
"DNNCat_option2":["SigRegion","ttWctrl"],
"DNNCat_option3":["SigRegion","ttWctrl"],
"DNNSubCat1_option1":["DiLepRegion"],
"DNNSubCat1_option2":["SigRegion","ttWctrl"],
"DNNSubCat1_option3":["SigRegion","ttWctrl"],
"DNNSubCat2_option1":["DiLepRegion"],
"DNNSubCat2_option2":["SigRegion","ttWctrl"],
"DNNSubCat2_option3":["SigRegion","ttWctrl"],
"DNNAMS2Cat1_option1":["SigRegion","ttWctrl"],
"DNNAMS2Cat1_option2":["SigRegion","ttWctrl"],
"DNNAMS2Cat1_option3":["SigRegion","ttWctrl"],
"DNNAMS3Cat1_option1":["SigRegion","ttWctrl"],
"DNNAMS3Cat1_option2":["SigRegion","ttWctrl"],
"DNNAMS3Cat1_option3":["SigRegion","ttWctrl"],
}
subCats={
"SubCat2l":["ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ],
"DNNCat":["ttHnode","Restnode","ttWnode","tHQnode"],
"DNNCat_option2":["ttHnode","Restnode","ttWnode","tHQnode"],
"DNNCat_option3":["ttHnode","Restnode","ttWnode","tHQnode"],
"DNNSubCat1_option1":["ee_neg","ee_pos","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNSubCat1_option2":["ee_neg","ee_pos","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNSubCat1_option3":["ee_neg","ee_pos","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNSubCat2_option1":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNSubCat2_option2":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNSubCat2_option3":["ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode","em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode","mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"],
"DNNAMS2Cat1_option1":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
"DNNAMS2Cat1_option2":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
"DNNAMS2Cat1_option3":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
"DNNAMS3Cat1_option1":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
"DNNAMS3Cat1_option2":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
"DNNAMS3Cat1_option3":["loose_ttHnode","tight_ttHnode","Restnode","ttWnode"],
}

#histoGramPerSample = {"EWK":"EWK","Conv":"Conv","TTW":"TTW","TTZ":"TTZ","Rares":"Rares","TTWW":"TTWW","Fakes":"Fakes", "Flips":"Flips",
histoGramPerSample = {
"WZ":"WZ","ZZ":"ZZ","Convs":"Convs","TTW":"TTW","TTZ":"TTZ","Rares":"Rares","TTWW":"TTWW",
"Fakes":"data_fakes", "Flips":"data_flips",
"mcFakes":"mcFakes","mcFlips":"mcFlips",
#"THQ_htt":"THQ_htt","THQ_hww":"THQ_hww","THQ_hzz":"THQ_hzz",
#"THW_htt":"THW_htt","THW_hww":"THW_hww","THW_hzz":"THW_hzz",
#"TTH_htt":"TTH_htt","TTH_hww":"TTH_hww","TTH_hzz":"TTH_hzz","TTH_hot":"TTH_hot","TTH_hmm":"TTH_hmm"
"VH_htt":"VH_htt","VH_hww":"VH_hww","VH_hzz":"VH_hzz",
"ggH_htt":"ggH_htt","ggH_hww":"ggH_hww","ggH_hzz":"ggH_hzz",
"qqH_htt":"qqH_htt","qqH_hww":"qqH_hww","qqH_hzz":"qqH_hzz",
"THQ_htt":"tHq_htt","THQ_hww":"tHq_hww","THQ_hzz":"tHq_hzz",
"THW_htt":"tHW_htt","THW_hww":"tHW_hww","THW_hzz":"tHW_hzz",
"TTH_htt":"ttH_htt","TTH_hww":"ttH_hww","TTH_hzz":"ttH_hzz","TTH_hmm":"ttH_hmm","TTH_hzg":"ttH_hzg", # sm
#"ttH_htt":"ttH_htt","ttH_hww":"ttH_hww","ttH_hzz":"ttH_hzz","ttH_hmm":"ttH_hmm","ttH_hzg":"ttH_hzg" # kt 
}


samples = [
"Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW",
"TTH_htt","TTH_hww","TTH_hzz","TTH_hzg","TTH_hmm", # sm
#"ttH_htt","ttH_hww","ttH_hzz","ttH_hzg","ttH_hmm", # kt
"mcFakes","mcFlips",
#"THQ_htt","THQ_hzz",
#"THW_htt","THW_hzz",
"THQ_htt","THQ_hww","THQ_hzz",
"THW_htt","THW_hww","THW_hzz"
"ggH_htt","ggH_hww","ggH_hzz",
"qqH_htt","qqH_hww","qqH_hzz",
"VH_htt","VH_hww","VH_hzz",
]



useData = False
use_ctcvcp = True
samplesData = ["Data"]


colourPerSample = {"TTW":kGreen+2,"TTZ":kGreen+4,"Conv":kYellow,"Rares":kBlue,"EWK":kPink,"Fakes":kGray,"TTH":kRed,"Flips":kOrange,"H":kRed+1,"TTWW":kGreen+3}
#colourPerSample = {"TTW":kGreen+2,"TTZ":kGreen+2,"Conv":kYellow,"Rares":kBlue,"EWK":kPink,"TTH":kRed}

ignoreSystPlots = ["PS","herwig","amcatnlo"]


legendOrder = ["TTW","TTWW","TTZ","Conv","Rares","EWK","H","TTH","Fakes","Flips"]

plotLeptonSampleName = "data"

includeDataInStack = False

makeStatBins = False

setNegToZero = True

reScaleBins = False

gROOT.SetBatch()

#from setTDRStyle import setTDRStyle

#setTDRStyle()

latex = TLatex()
latex.SetNDC()
latex.SetTextAlign(31)

cmsTextFont = 61
extraTextFont = 52

latex2 = TLatex();
latex2.SetNDC();
latex2.SetTextSize(0.04);
latex2.SetTextAlign(31);

cmsText = "CMS"
extraText = "Preliminary"

makeSystComps = False #Make a whole bunch of comparison plots if true
makeStackPlots = False #Make some stack plots of the output
reduceBinsToFilled = False #Reduce the histograms to only their filled bins. This might possibly influence the fit, but my tests do not indicate that it does.

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-v', '--var',        dest='variable'  ,      help='variable name of final discriminator',      default='Bin2l_',        type='string')
parser.add_option('-i', '--inDir',        dest='inDir'  ,      help='inDir of histograms',      default='Output/SubCat2l/',        type='string')
parser.add_option('-o', '--outDir',        dest='outDir'  ,      help='outDir of histograms',      default='V0212_datacards/SubCat2l/Bin2l/',        type='string')
parser.add_option('-c', '--cat',        dest='category'  ,      help='type of channels',      default="SubCat2l",        type='string')
parser.add_option('-s', '--smooth',        dest='nSmooth'  ,      help='# iteration of smooth',      default=0,        type='int')
parser.add_option('-y', '--year',        dest='year'  ,      help='data taking year',      default=2018,        type='int')
parser.add_option('-n', '--namefix',        dest='namefix'  ,      help='namefix',      default="datacard",        type='string')


(opt, args) = parser.parse_args()
mvaNameDef = "Bin2l_"
mvaPostfix = ""

inDir = opt.inDir
outDir = opt.outDir
nSmooth = opt.nSmooth
variableName = opt.variable
cat_str = opt.category
year = opt.year
namefix = opt.namefix

doSystDir = False
systDir = inDir+"Systs/"
isEle = False
channeltr = "mu"

if "Bin2l" not in outDir:
    mvaNameDef = variableName + "_"

print "mvaNameDef is "+ mvaNameDef

if "ele" in sys.argv:
    samplesData = samplesDataEle
    plotLeptonSampleName = "Ele"
    channeltr = "ele"
    isEle = True
#if len(sys.argv) > 3: systDir = sys.argv[3]

#weights = weightProcesses.ReweightObject(False,isEle)

if (not os.path.isdir(outDir)):
    os.makedirs(outDir)
if makeSystComps and not os.path.isdir(outDir+"plots/"): os.makedirs(outDir+"plots/")

nominal = {}

systs_2016 = [
"PU_16","CMS_ttHl16_L1PreFiring","CMS_ttHl16_trigger",
"CMS_ttHl16_btag_HFStats1","CMS_ttHl16_btag_HFStats2","CMS_ttHl16_btag_LFStats1","CMS_ttHl16_btag_LFStats2",
"bWeight_jes","CMS_ttHl_btag_cErr1","CMS_ttHl_btag_cErr2","CMS_ttHl_btag_LF","CMS_ttHl_btag_HF",
"CMS_ttHl_lepEff_elloose","CMS_ttHl_lepEff_eltight","CMS_ttHl_lepEff_muloose","CMS_ttHl_lepEff_mutight",
"CMS_ttHl_thu_shape_ttH_x1","CMS_ttHl_thu_shape_ttH_y1",
"CMS_ttHl_FRm_norm","CMS_ttHl_FRm_pt","CMS_ttHl_FRm_be","CMS_ttHl_FRe_norm","CMS_ttHl_FRe_pt","CMS_ttHl_FRe_be","CMS_ttHl_Clos_e_shape","CMS_ttHl_Clos_m_shape","CMS_ttHl_Clos_e_norm","CMS_ttHl17_Clos_m_norm",
"CMS_ttHl_QF",
]

systs_2017 = [
"PU_17","CMS_ttHl17_L1PreFiring","CMS_ttHl17_trigger",
"CMS_ttHl17_btag_HFStats1","CMS_ttHl17_btag_HFStats2","CMS_ttHl17_btag_LFStats1","CMS_ttHl17_btag_LFStats2",
"bWeight_jes","CMS_ttHl_btag_cErr1","CMS_ttHl_btag_cErr2","CMS_ttHl_btag_LF","CMS_ttHl_btag_HF",
"CMS_ttHl_lepEff_elloose","CMS_ttHl_lepEff_eltight","CMS_ttHl_lepEff_muloose","CMS_ttHl_lepEff_mutight",
"CMS_ttHl_thu_shape_ttH_x1","CMS_ttHl_thu_shape_ttH_y1",
"CMS_ttHl_FRm_norm","CMS_ttHl_FRm_pt","CMS_ttHl_FRm_be","CMS_ttHl_FRe_norm","CMS_ttHl_FRe_pt","CMS_ttHl_FRe_be","CMS_ttHl_Clos_e_shape","CMS_ttHl_Clos_m_shape","CMS_ttHl_Clos_e_norm","CMS_ttHl17_Clos_m_norm",
"CMS_ttHl_QF",
]

systs_2018 = [
"PU_18","CMS_ttHl18_trigger",
"CMS_ttHl18_btag_HFStats1","CMS_ttHl18_btag_HFStats2","CMS_ttHl18_btag_LFStats1","CMS_ttHl18_btag_LFStats2",
"bWeight_jes","CMS_ttHl_btag_cErr1","CMS_ttHl_btag_cErr2","CMS_ttHl_btag_LF","CMS_ttHl_btag_HF",
"CMS_ttHl_lepEff_elloose","CMS_ttHl_lepEff_eltight","CMS_ttHl_lepEff_muloose","CMS_ttHl_lepEff_mutight",
"CMS_ttHl_thu_shape_ttH_x1","CMS_ttHl_thu_shape_ttH_y1",
"CMS_ttHl_FRm_norm","CMS_ttHl_FRm_pt","CMS_ttHl_FRm_be","CMS_ttHl_FRe_norm","CMS_ttHl_FRe_pt","CMS_ttHl_FRe_be","CMS_ttHl_Clos_e_shape","CMS_ttHl_Clos_m_shape","CMS_ttHl_Clos_e_norm","CMS_ttHl17_Clos_m_norm",
"CMS_ttHl_QF",
]

systs=[]
if year == 2016:
    systs = systs_2016
    print ( " use 2016 systematics ")
elif year == 2017:
    systs = systs_2017
    print ( " use 2017 systematics ")
elif year == 2018:
    systs = systs_2018
    print ( " use 2018 systematics ")
else:
    print ( " You pass %i to year, however it must be 2016/2017 or 2018, I don't know what to do other than exit the script "%year)
    sys.exit()


systs_ctcvcp = [
"kt_m3_kv_1","kt_m2_kv_1","kt_m1p5_kv_1","kt_m1p25_kv_1","kt_m0p75_kv_1","kt_m0p5_kv_1","kt_m0p25_kv_1","kt_0_kv_1","kt_0p25_kv_1","kt_0p5_kv_1","kt_0p75_kv_1","kt_1_kv_1","kt_1p25_kv_1","kt_1p5_kv_1","kt_2_kv_1","kt_3_kv_1","kt_m2_kv_1p5","kt_m1p5_kv_1p5","kt_m1p25_kv_1p5","kt_m1_kv_1p5","kt_m0p5_kv_1p5","kt_m0p25_kv_1p5","kt_0p25_kv_1p5","kt_0p5_kv_1p5","kt_1_kv_1p5","kt_1p25_kv_1p5","kt_2_kv_1p5","kt_m3_kv_0p5","kt_m2_kv_0p5","kt_m1p25_kv_0p5","kt_1p25_kv_0p5","kt_2_kv_0p5","kt_3_kv_0p5",
#"cosa_m0p9","cosa_m0p8","cosa_m0p7","cosa_m0p6","cosa_m0p5","cosa_m0p4","cosa_m0p3","cosa_m0p2","cosa_m0p1","cosa_mp0","cosa_0p1","cosa_0p2","cosa_0p3","cosa_0p4","cosa_0p5","cosa_0p6","cosa_0p7","cosa_0p8","cosa_0p9"
]

systsFakes =[
"CMS_ttHl_FRm_norm","CMS_ttHl_FRm_pt","CMS_ttHl_FRm_be","CMS_ttHl_FRe_norm","CMS_ttHl_FRe_pt","CMS_ttHl_FRe_be","CMS_ttHl_Clos_e_shape","CMS_ttHl_Clos_m_shape",
]

systFlips=[
"CMS_ttHl_QF",
]


nStatsBins = 0
systHists = {}

totalYieldsCount = {}

def createSum(h1, h2, c=1):
    # h3 = h1 + c*h2
    h3 = h1.Clone(h1.GetName())
    h3.Sumw2()
    h3.SetStats(0)
    h3.Add(h2, c)

    return h3

def findMaxAndMinBins(nominalHists,systHist):
    maxBin = 0
    minBin = 50
    returnNominals = {}
    returnSysts = {}
    for key in nominalHists.keys():
        print " before rebin , hist yield of "+key+" is "+str(nominalHists[key].Integral())
        if nominalHists[key].FindFirstBinAbove() < minBin: minBin = nominalHists[key].FindFirstBinAbove()
        if nominalHists[key].FindLastBinAbove() > maxBin: maxBin = nominalHists[key].FindLastBinAbove()
        if key == "data" or key == "qcd":continue
        for key2 in systHist[key].keys():
            if systHist[key][key2].FindFirstBinAbove() < minBin: minBin = systHist[key][key2].FindFirstBinAbove()
            if systHist[key][key2].FindLastBinAbove() > maxBin: maxBin = systHist[key][key2].FindLastBinAbove()
    xLow = nominalHists[key].GetXaxis().GetBinLowEdge(minBin)
    xHigh = nominalHists[key].GetXaxis().GetBinUpEdge(maxBin)
    for key in nominalHists.keys():
        returnNominals[key] = TH1F(nominalHists[key].GetName(),nominalHists[key].GetTitle(),maxBin-minBin+1,xLow,xHigh)
        i = 1
        for j in range(minBin,maxBin+1):
            returnNominals[key].SetBinContent(i,nominalHists[key].GetBinContent(j))
            returnNominals[key].SetBinError(i,nominalHists[key].GetBinError(j))
            i+=1
        if key == "data" or key == "qcd":continue
        returnSysts[key] = {}
        for key2 in systHist[key].keys():
            returnSysts[key][key2] = TH1F(systHist[key][key2].GetName(),systHist[key][key2].GetTitle(),maxBin-minBin+1,xLow,xHigh)
            i = 1
            for j in range(minBin,maxBin+1):
                returnSysts[key][key2].SetBinContent(i,systHist[key][key2].GetBinContent(j))
                returnSysts[key][key2].SetBinError(i,systHist[key][key2].GetBinError(j))
                i+=1
    print "Hists have been rescaled to fit range {0}-{1}".format(xLow,xHigh)
    return (returnNominals,returnSysts)

def setAllNegBinsToZero(hist, key):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) < 0.: 
            hist.SetBinContent(i,0.)
            print " set negative bins to 0. the key is ", key 

def makeAllSystHists(nominal,systHists,region,savePost=""):
    latexFile = open(outDir+"plots/{0}latexFile{1}.tex".format(region,savePost),"w")
    secondLatexFile = open(outDir+"plots/{0}latexFile{1}NotBeamer.tex".format(region,savePost),"w")
    latexFile.write("\\documentclass{beamer}\n\\usetheme{Warsaw}\n\n\\usepackage{graphicx}\n\\useoutertheme{infolines}\n\\setbeamertemplate{headline}{}\n\n\\begin{document}\n\n")
    for sample in nominal.keys():
        if sample == "data" or sample == "qcd": continue
        for syst in systHists[sample].keys():
            doPlot = True
            for ignore in ignoreSystPlots:
                if ignore in syst: doPlot = False
            if not doPlot: continue
            if "Down" in syst or "stat" in syst or "down" in syst: continue
            downSystName = syst.split("Up")[0]+"Down"
            shortenedName = syst.split("Up")[0]
            if "up" in syst: downSystName = syst.split("up")[0]+"down"
            makeSystHist(nominal[sample],systHists[sample][syst],systHists[sample][downSystName],region+sample+shortenedName+savePost)
            latexFile.write("\\frame{{\n\\frametitle{{{0}-{1}-{2}}}\n".format(region,sample,shortenedName))
            latexFile.write("\\includegraphics[width=0.9\\textwidth]{"+region+sample+shortenedName+savePost+".png}")
            secondLatexFile.write("\\includegraphics[width=0.5\\textwidth]{"+region+sample+shortenedName+savePost+".png}\n")
            latexFile.write("\n}\n")
        #Now make one for the statistical uncertainty
        statHists = getStatUpDownHists(nominal[sample])
        makeSystHist(nominal[sample],statHists[0],statHists[1],region+sample+"stats"+savePost)
        latexFile.write("\\frame{{\n\\frametitle{{{0}-{1}-{2}}}\n".format(region,sample,"Stats"))
        latexFile.write("\\includegraphics[width=0.9\\textwidth]{"+region+sample+"stats"+savePost+".png}")
        secondLatexFile.write("\\includegraphics[width=0.5\\textwidth]{"+region+sample+"stats"+savePost+".png}\n")
        latexFile.write("\n}\n")

    latexFile.write("\\frame{{\n\\frametitle{{MVA {0}}}\n".format(region))
    latexFile.write("\\includegraphics[width=0.9\\textwidth]{{mva{0}{1}.png}}".format(region,savePost))
    latexFile.write("\n}\n")                                                                       

    latexFile.write("\\end{document}")
            

def getStatUpDownHists(nominal):
    #get histograms with the bins altered up and down by the bin error
     statsUp = nominal.Clone(nominal.GetName()+"StatsUp")
     statsDown = nominal.Clone(nominal.GetName()+"StatsDown")
     for i in range(1,nominal.GetXaxis().GetNbins()+1):
         statsUp.SetBinContent(i,nominal.GetBinContent(i)+nominal.GetBinError(i))
         statsDown.SetBinContent(i,nominal.GetBinContent(i)-nominal.GetBinError(i))
     return statsUp,statsDown

def makeSystHist(nominalHist,upHist,downHist,canvasName):
#    canvasName = upHist.GetName().split("Up")[0]
    canvy = TCanvas(canvasName,canvasName,1000,800)
    canvy.cd()
    canvy.SetBottomMargin(0.3)
    nominalHist.SetLineColor(kBlack)
    histMax = 0.
    if upHist.GetMaximum() > histMax: histMax = upHist.GetMaximum() 
    if downHist.GetMaximum() > histMax: histMax = downHist.GetMaximum()
    nominalHist.SetMaximum(histMax*1.2)
    nominalHist.Draw("hist")
    upHist.SetLineColor(kRed)
    upHist.Draw("hist same")
    downHist.SetLineColor(kBlue)
    downHist.Draw("hist same")

    latex.SetTextSize(0.04)
    latex.SetTextFont(cmsTextFont)
    latex.DrawLatex(0.23, 0.95, cmsText )
    
    latex.SetTextFont(extraTextFont)
    latex.SetTextSize(0.04*0.76)
    latex.DrawLatex(0.35, 0.95 , extraText )
    
    latex2.DrawLatex(0.95, 0.95, canvasName);
    
    ratioCanvy = TPad("mva_ratio","mva_ratio",0.0,0.0,1.0,1.0)
    ratioCanvy.SetTopMargin(0.7)
    ratioCanvy.SetFillColor(0)
    ratioCanvy.SetFillStyle(0)
    ratioCanvy.SetGridy(1)
    ratioCanvy.Draw()
    ratioCanvy.cd(0)
    SetOwnership(ratioCanvy,False)
    

    
#    text2 = TLatex(0.45,0.98, "#mu channel " + canvasName)
#    text2.SetNDC()
#    text2.SetTextAlign(13)
#    text2.SetX(0.18)
#    text2.SetY(0.92)
#    text2.SetTextFont(42)
#    text2.SetTextSize(0.0610687)
#

    upHistRatio = upHist.Clone()
    upHistRatio.Divide(nominalHist)
    upHistRatio.SetMaximum(1.3)
    upHistRatio.SetMinimum(0.7)
    upHistRatio.Draw("hist same")
    downHistRatio = downHist.Clone()
    downHistRatio.Divide(nominalHist)
    downHistRatio.GetXaxis().SetTitle("BDT Discriminant")
    downHistRatio.Draw("hist same")

    canvy.SaveAs(outDir+"plots/"+canvasName+".png")

def makeStackPlot(nominal,systHists,region,savePost = ""):
    stack = THStack("mva_{0}".format(region),"mva_{0}".format(region))
    canvy = TCanvas("MVA_{0}".format(region),"MVA_{0}".format(region),1000,800)
    leggy = TLegend(0.8,0.6,0.95,0.9)
    leggy.SetFillStyle(1001)
    leggy.SetBorderSize(1)
    leggy.SetFillColor(0)
    leggy.SetLineColor(0)
    leggy.SetShadowColor(0)
    leggy.SetFillColor(kWhite)
    
    canvy.cd()
    if includeDataInStack: canvy.SetBottomMargin(0.3)
    dataHist = 0
    sumHist = nominal[nominal.keys()[0]].Clone()
    sumHist.Reset()
    for i in nominal.keys():
        if i == "data":
            dataHist = nominal["data"]
            dataHist.SetMarkerStyle(20)
            dataHist.SetMarkerSize(1.2)
            dataHist.SetMarkerColor(kBlack)
            continue
        nominal[i].SetFillColor(colourPerSample[i])
        nominal[i].SetLineColor(kBlack)
        nominal[i].SetLineWidth(1)
#        stack.Add(nominal[i])
        sumHist.Add(nominal[i])
        #Do systematic estimation here when I get aorund to it)

    if "data" in nominal.keys():
        leggy.AddEntry(nominal['data'],"Data","p")
    for entry in legendOrder:
        leggy.AddEntry(nominal[entry],entry,"f")

    legendOrder.reverse()
    for entry in legendOrder:
        stack.Add(nominal[entry])

    maxi = stack.GetMaximum()
    if dataHist.GetMaximum() > stack.GetMaximum(): maxi = dataHist.GetMaximum()
    stack.SetMaximum(maxi)
    stack.Draw("hist")
    
    if includeDataInStack: dataHist.Draw("e1x0 same")
    leggy.Draw()

    if includeDataInStack:
        ratioCanvy = TPad("mva_ratio","mva_ratio",0.0,0.0,1.0,1.0)
        ratioCanvy.SetTopMargin(0.7)
        ratioCanvy.SetFillColor(0)
        ratioCanvy.SetFillStyle(0)
        ratioCanvy.SetGridy(1)
        ratioCanvy.Draw()
        ratioCanvy.cd(0)
        SetOwnership(ratioCanvy,False)

        sumHistoData = dataHist.Clone(dataHist.GetName()+"_ratio")
        sumHistoData.Sumw2()
        sumHistoData.Divide(sumHist)

        sumHistoData.GetYaxis().SetTitle("Data/MC")
        sumHistoData.GetYaxis().SetTitleOffset(1.3)
        ratioCanvy.cd()
        SetOwnership(sumHistoData,False)
        sumHistoData.SetMinimum(0.8)
        sumHistoData.SetMaximum(1.2)
        sumHistoData.GetXaxis().SetTitleOffset(1.2)
        sumHistoData.GetXaxis().SetLabelSize(0.04)
        sumHistoData.GetYaxis().SetNdivisions(6)
        sumHistoData.GetYaxis().SetTitleSize(0.03)
        sumHistoData.Draw("E1X0")

    canvy.SaveAs(outDir+"plots/mva{0}{1}.png".format(region,savePost))
    canvy.SaveAs(outDir+"plots/mva{0}{1}.root".format(region,savePost))


def getDownHist(upHist,nominalHist):
    downHist = nominalHist.Clone(upHist.GetName().split("Up")[0]+"Down")
    downHist.SetDirectory(0)
    for i in range(1,nominalHist.GetXaxis().GetNbins()+1):
        diffBin = nominalHist.GetBinContent(i) - upHist.GetBinContent(i)
        downHist.SetBinContent(i,nominalHist.GetBinContent(i) + diffBin)
        if downHist.GetBinContent(i) < 0.: downHist.SetBinContent(i,0.)
    return downHist

def makeStatBinVariations(hist, binNumber, region, channeltr):

    variationHistUp = hist.Clone("{2}_{2}_ttH{1}{3}_template_statbin{0}Up".format(binNumber,region,hist.GetName(),channeltr))
    variationHistDown = hist.Clone("{2}_{2}_ttH{1}{3}_template_statbin{0}Down".format(binNumber,region,hist.GetName(),channeltr))
    binWeight = hist.GetBinContent(binNumber)
    shift = 0

    shift = hist.GetBinError(binNumber)
    variationHistUp.SetBinContent(binNumber,binWeight+shift)
    variationHistDown.SetBinContent(binNumber,binWeight-shift)
    return (variationHistUp,variationHistDown)


def makeDatacard(mvaName,regions,channeltr,savePostfix=""):
    for region in regions:
        saveName = "2lss"
        # Rename SigRegion to 2lss
        if not region == "SigRegion": saveName = region
        outFile = TFile(outDir+"{0}_{1}_{2}{3}.root".format(namefix,saveName,channeltr,savePostfix),"RECREATE")

        totalYieldsCount[region] = {}
        nominal = {}
        systHists = {}
        if doSystDir: systDir = inDir + "Systs" + saveName + "/"
        FakeSubFile = TFile(inDir+channeltr+"/"+region+"/output_"+channeltr+"_FakeSub.root","READ")
        for sample in samples:
            #get input file
            inFile = TFile(inDir+channeltr+"/"+region+"/output_"+channeltr+"_"+sample+".root","READ")
            if inFile.IsZombie():
                print (inDir+channeltr+"/"+region+"/output_"+channeltr+"_"+sample+".root" + " is Zombie ")
                continue
            print sample
            #get nominal plot"
            if histoGramPerSample[sample] in nominal.keys():
                if sample!="Fakes": 
                    if use_ctcvcp and ("THQ" in sample or "THW" in sample) :
                        nominal[histoGramPerSample[sample]].Add(inFile.Get(mvaName+sample+savePostfix))
                    else:
                        nominal[histoGramPerSample[sample]].Add(inFile.Get(mvaName+sample))
                else:
                    nominal[histoGramPerSample[sample]].Add(FakeSubFile.Get(mvaName+"FakeSub"),-1)
                #print "yield of histograms " + mvaName+sample+" : " + str(inFile.Get(mvaName+sample).Clone(mvaName+sample).Integral())
                for sys in systs:
                    if sample == "Fakes" and  "Clos" not in sys and "_FR" not in sys : continue
                    if sample == "Flips" and  "CMS_ttHl_QF" not in sys : continue
                    if sample != "Fakes" and sample != "Flips" and (("Clos" in sys or "_FR" in sys) or ("CMS_ttHl_QF" in sys)): continue
                    
                    #print mvaName+sample+"_"+sys+"_up"
                    if sample!="Fakes": 
                        systHists[histoGramPerSample[sample]][sys+"Up"].Add(inFile.Get(mvaName+sample+"_"+sys+"_up"))
                        systHists[histoGramPerSample[sample]][sys+"Down"].Add(inFile.Get(mvaName+sample+"_"+sys+"_down"))
                    else:
                        systHists[histoGramPerSample[sample]][sys+"Up"].Add(FakeSubFile.Get(mvaName+"FakeSub_"+sys+"_up"),-1)
                        systHists[histoGramPerSample[sample]][sys+"Down"].Add(FakeSubFile.Get(mvaName+"FakeSub_"+sys+"_down"),-1)

            else:
                print ' try to get hist "' + mvaName + sample + '" from file "' + inDir+channeltr+"/"+region+"/output_"+channeltr+"_"+sample+".root" 
                if sample!="Fakes": 
                    if use_ctcvcp and ("THQ" in sample or "THW" in sample) :
                        nominal[histoGramPerSample[sample]]= inFile.Get(mvaName+sample+savePostfix).Clone(histoGramPerSample[sample])
                    else:
                        nominal[histoGramPerSample[sample]] = inFile.Get(mvaName+sample).Clone(histoGramPerSample[sample])
                    nominal[histoGramPerSample[sample]].Sumw2()
                    nominal[histoGramPerSample[sample]].SetDirectory(0)
                    print ' the yield is ' + str(nominal[histoGramPerSample[sample]].Integral())
                else:
                    nominal[histoGramPerSample[sample]]=inFile.Get(mvaName+sample).Clone(histoGramPerSample[sample])
                    nominal[histoGramPerSample[sample]].Sumw2()
                    nominal[histoGramPerSample[sample]].SetDirectory(0)
                    nominal[histoGramPerSample[sample]].Add(FakeSubFile.Get(mvaName+"FakeSub"),-1)

                systHists[histoGramPerSample[sample]] = {}
                for sys in systs:
                    if sample == "Fakes" and  "Clos" not in sys and "_FR" not in sys : continue
                    if sample == "Flips" and  "CMS_ttHl_QF" not in sys : continue
                    if sample != "Fakes" and sample != "Flips" and (("Clos" in sys or "_FR" in sys) or ("CMS_ttHl_QF" in sys)): continue
                    #print sys, mvaName+sample+"_"+sys+"_up"
                    systNameForClone = histoGramPerSample[sample]+"_"+sys
                    if "statbin" in sys: systNameForClone = histoGramPerSample[sample]+"_"+histoGramPerSample[sample]+"_"+plotLeptonSampleName+"_"+sys
                    if sample!="Fakes": 
                        systHists[histoGramPerSample[sample]][sys+"Up"] = inFile.Get(mvaName+sample+"_"+sys+"_up").Clone(systNameForClone+"Up")
                        systHists[histoGramPerSample[sample]][sys+"Up"].SetDirectory(0)
                        systHists[histoGramPerSample[sample]][sys+"Down"] = inFile.Get(mvaName+sample+"_"+sys+"_down").Clone(systNameForClone+"Down")
                        systHists[histoGramPerSample[sample]][sys+"Down"].SetDirectory(0)
                        systHists[histoGramPerSample[sample]][sys+"Up"].Sumw2()
                        systHists[histoGramPerSample[sample]][sys+"Down"].Sumw2()
                    else:
                        systHists[histoGramPerSample[sample]][sys+"Up"] = inFile.Get(mvaName+sample+"_"+sys+"_up").Clone(systNameForClone+"Up")
                        systHists[histoGramPerSample[sample]][sys+"Up"].SetDirectory(0)
                        systHists[histoGramPerSample[sample]][sys+"Down"] = inFile.Get(mvaName+sample+"_"+sys+"_down").Clone(systNameForClone+"Down")
                        systHists[histoGramPerSample[sample]][sys+"Down"].SetDirectory(0)
                        systHists[histoGramPerSample[sample]][sys+"Up"].Sumw2()
                        systHists[histoGramPerSample[sample]][sys+"Down"].Sumw2()
                        systHists[histoGramPerSample[sample]][sys+"Up"].Add(FakeSubFile.Get(mvaName+"FakeSub_"+sys+"_up"),-1)
                        systHists[histoGramPerSample[sample]][sys+"Down"].Add(FakeSubFile.Get(mvaName+"FakeSub_"+sys+"_down"),-1)

        dirSysts = ["CMS_scale_j"]
        upDown = ["Up","Down"]
        if doSystDir:
            for ud in upDown:
                for syst in dirSysts:
                    #dirName = syst+ud
                    dirName = "JES"+ud
                    print "Processing systematic in {0}".format(dirName)
                    FakeSubFile = TFile(inDir+channeltr+"/"+dirName+region+"/output_"+channeltr+"_FakeSub.root","READ")
                    for sample in samples:
                        if sample=="Flips": continue
                        if sample != "Fakes":
                            inFile = TFile(inDir+channeltr+"/"+dirName+region+"/output_"+channeltr+"_"+sample+".root","READ")
                            if inFile.IsZombie():
                                print (inDir+channeltr+"/"+dirName+region+"/output_"+channeltr+"_"+sample+".root" + " is Zombie ")
                                continue
                            print "Processing sample {0}".format(sample)
                            if dirName not in systHists[histoGramPerSample[sample]]:
                                systHists[histoGramPerSample[sample]][dirName] = inFile.Get(mvaName+sample+"_bWeight_jes_"+ud.lower()).Clone(histoGramPerSample[sample]+"_"+syst+ud)
                                systHists[histoGramPerSample[sample]][dirName].SetDirectory(0)
                            else:
                                systHists[histoGramPerSample[sample]][dirName] = inFile.Get(mvaName+sample+"_bWeight_jes_"+ud.lower()).Clone(histoGramPerSample[sample]+"_"+syst+ud)
                        else:
                            inFile = TFile(inDir+channeltr+"/"+region+"/output_"+channeltr+"_"+sample+".root","READ")
                            if inFile.IsZombie():
                                print (inDir+channeltr+"/"+region+"/output_"+channeltr+"_"+sample+".root" + " is Zombie ")
                                continue
                            print "Processing sample {0}".format(sample)
                            if dirName not in systHists[histoGramPerSample[sample]]:
                                systHists[histoGramPerSample[sample]][dirName] = inFile.Get(mvaName+sample).Clone(histoGramPerSample[sample]+"_"+syst+ud)
                                systHists[histoGramPerSample[sample]][dirName].Sumw2()
                                systHists[histoGramPerSample[sample]][dirName].SetDirectory(0)
                                systHists[histoGramPerSample[sample]][dirName].Add(FakeSubFile.Get(mvaName+"FakeSub_bWeight_jes_"+ud.lower()).Clone(histoGramPerSample[sample]+"_"+syst+ud),-1)
                            else:
                                systHists[histoGramPerSample[sample]][dirName] = inFile.Get(mvaName+sample).Clone(histoGramPerSample[sample]+"_"+syst+ud)
                                systHists[histoGramPerSample[sample]][dirName].Sumw2()
                                systHists[histoGramPerSample[sample]][dirName].Add(FakeSubFile.Get(mvaName+"FakeSub_bWeight_jes_"+ud.lower()).Clone(histoGramPerSample[sample]+"_"+syst+ud),-1)

        if useData:
            for sample in samplesData:
                print "Dataset: {0}".format(sample)
                inFile = TFile(inDir+channeltr+"/"+region+"/output_"+channeltr+"_"+sample+".root","READ")
                #inFile = TFile(inDir+region+"/output_"+sample+".root","READ")
                #inFileQCD = TFile(inDir+"QCD{0}/output_".format(region)+sample+".root","READ")
                if inFile.IsZombie():
                    print (inDir+channeltr+"/"+region+"/output_"+channeltr+"_"+sample+".root" + " is Zombie ")
                    continue
                if "data" not in nominal.keys():
                    nominal["data"] = inFile.Get(mvaName+sample).Clone("data_obs")
                    nominal["data"].SetDirectory(0)
                    #nominal["qcd"] = inFileQCD.Get(mvaName+sample).Clone("qcd")
                    #nominal["qcd"].SetDirectory(0)
                    #print "QCD template has {0}".format(nominal["qcd"].Integral())
                else:
                    nominal["data"].Add(inFile.Get(mvaName+sample))
                    #nominal["qcd"].Add(inFileQCD.Get(mvaName+sample))
                    #print "QCD template has {0}".format(nominal["qcd"].Integral())

        #Here we should grab the systematic samples if we're doing that.        
        sysDirNamesList = []
        sysNamesToGetDownHist = []
        if doSystDir:
            for fileName in os.listdir(systDir):
                sample = fileName.split("_")[1]
                sample2 = fileName.split("output_")[1].split(".root")[0]
                syst = fileName.split("_")[-1].split(".")[0]
                inFile = TFile(systDir+fileName,"READ")
                if syst in systHists[sample].keys():
                    print "Adding 1 {0},{1},{2}".format( sample, syst, sample2), systHists[sample][syst].Integral(),
                    systHists[sample][syst].Add(inFile.Get(mvaName+sample2))
                    print systHists[sample][syst].Integral()
                elif syst+"Up" in systHists[sample].keys():
                    print "Adding 2 {0},{1},{2}".format( sample, syst, sample2),
                    print systHists[sample][syst+"Up"].Integral(),
                    systHists[sample][syst+"Up"].Add(inFile.Get(mvaName+sample2))
                    print sample2,systHists[sample][syst+"Up"].Integral()
        #            systHists[sample][syst+"Down"].Add(getDownHist(inFile.Get(mvaName+sample2),nominal[sample]))
                else:
                    print "Making new {0},{1},{2}".format( sample, syst, sample2)
                    cloneName = syst
                    sysDirNamesList.append(syst)
                    if "up" in syst:
                        cloneName = syst.split("up")[0]+"Up"
                    elif "down" in syst:
                        cloneName = syst.split("down")[0]+"Down"
                    else:
                        systHists[sample][syst+"Up"] = inFile.Get(mvaName+sample2).Clone(sample+"_"+syst+"Up")
                        systHists[sample][syst+"Up"].SetDirectory(0)
                        sysNamesToGetDownHist.append((sample,syst))
        #                systHists[sample][syst+"Down"] = getDownHist(systHists[sample][syst+"Up"],nominal[sample])
                        continue
                    systHists[sample][syst] = inFile.Get(mvaName+sample2).Clone(sample+"_"+cloneName)
                    systHists[sample][syst].SetDirectory(0)

        for pair in sysNamesToGetDownHist:

            print "Entry: ",pair[0],pair[1]
            #A hack to normalise herwig sample correctly
            if pair[0] == "ttbar" and pair[1] == "herwig":
                systHists[pair[0]][pair[1]+"Up"].Scale(0.5)
            systHists[pair[0]][pair[1]+"Down"] = getDownHist(systHists[pair[0]][pair[1]+"Up"],nominal[pair[0]])

#        halveSize = ["isr","fsr","tune","hdamp"]
        halveSize = []

        for key in nominal.keys():
            if setNegToZero: setAllNegBinsToZero(nominal[key], key)
            totalYieldsCount[region][key] = nominal[key].Integral()

            nominal[key].Sumw2()
            
            #Make the stat variation histograms
            if "data" in key or "qcd" in key: continue
            if makeStatBins:
                for i in range(1,nominal[key].GetXaxis().GetNbins()+1):
                    systHists[key]["statbin"+str(i)+"up"],systHists[key]["statbin"+str(i)+"down"] = makeStatBinVariations(nominal[key],i,region,channeltr)

        #Here make a loop to find out the highest and lowest filled bins so get rid of zero occupancy bins?
    #    for key in nominal.keys():

        if reScaleBins:
            (nominal,systHists) = findMaxAndMinBins(nominal,systHists)
        outFile.cd()
        print sysDirNamesList
        for key in nominal.keys():
            #scaleFactor = weights.getDatasetWeight(key,region)
            scaleFactor = 1 
            nominal[key].Scale(scaleFactor)
            totalYieldsCount[region][key] *= scaleFactor
#            if key in perMCSFs.keys():
#                nominal[key].Scale(perMCSFs[key])
#                totalYieldsCount[region][key] *= perMCSFs[key]
            if nSmooth >=1 : nominal[key].Smooth(nSmooth)
            nominal[key].Write()
            print key, nominal[key].Integral()
            if key == "data" or key == "qcd": continue
            for key2 in systHists[key].keys():
                systHists[key][key2].Scale(scaleFactor)
#                if key in perMCSFs.keys():
#                    for systName in halveSize:
#                        if key == "ttbar" and systName in key2: 
    #                        print "rescaling: ",key,key2
#                            systHists[key][key2].Scale(0.5)
#                    systHists[key][key2].Scale(perMCSFs[key])
                if setNegToZero: setAllNegBinsToZero(systHists[key][key2], key)
                if nSmooth >=1 : systHists[key][key2].Smooth(nSmooth)
                systHists[key][key2].Write()
                
        if not useData: 
            for key in nominal.keys():
                if "data" not in nominal.keys():
                    nominal["data"] = nominal[key].Clone("data_obs")
                    nominal["data"].SetDirectory(0)
                elif key=="data": continue
                else:    
                    nominal["data"].Add(nominal[key])
        
            totalYieldsCount[region]["data"] = nominal["data"].Integral()
            nominal["data"].Write()

        if makeSystComps: 
            makeAllSystHists(nominal,systHists,region,savePostfix)
        if makeStackPlots:
            makeStackPlot(nominal,systHists,region,savePostfix)


    for region in regions:
        print region
        for key in totalYieldsCount[region].keys():
            print key, totalYieldsCount[region][key]

    for j in regions:
        for i in []:
            print totalYieldsCount[j][i],

    print ""

    for j in regions:
        for i in []:
            print "{0} {1}".format(j,i),

    print

    for j in regions:
        #if useData:
        print totalYieldsCount[j]["data"]

if __name__ == "__main__":

    #regions = ["3j1t","2j1t","3j2t","4j1t","4j2t"]
    #regions = ["2L"]
#    for postName in ["bin10_","bin20_","bin30_","bin40_","bin50_","bin80_","bin100_","bin1000_"]:
#    for postName in ["bin10_","bin20_","bin30_","bin40_","bin50_","bin80_"]:
#    for postName in ["bin80_","bin100_"]:
#    for postName in ["bin1000_"]:
    #regions = ["SigRegion","ttWctrl"]
    #channels = [ "ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ]
    regions=regPerCat[cat_str]
    channels=subCats[cat_str]
    #channels = [ "ee_neg"]
    
    if "tHq"  in namefix :

        histoGramPerSample = {
        "WZ":"WZ","ZZ":"ZZ","Convs":"Convs","TTW":"TTW","TTZ":"TTZ","Rares":"Rares","TTWW":"TTWW",
        "Fakes":"data_fakes", "Flips":"data_flips",
        "mcFakes":"mcFakes","mcFlips":"mcFlips",
        "VH_htt":"VH_htt","VH_hww":"VH_hww","VH_hzz":"VH_hzz",
        "ggH_htt":"ggH_htt","ggH_hww":"ggH_hww","ggH_hzz":"ggH_hzz",
        "qqH_htt":"qqH_htt","qqH_hww":"qqH_hww","qqH_hzz":"qqH_hzz",
        "THQ_htt":"tHq_htt","THQ_hww":"tHq_hww","THQ_hzz":"tHq_hzz",
        "THW_htt":"tHW_htt","THW_hww":"tHW_hww","THW_hzz":"tHW_hzz",
        "ttH_htt":"ttH_htt","ttH_hww":"ttH_hww","ttH_hzz":"ttH_hzz","ttH_hmm":"ttH_hmm","ttH_hzg":"ttH_hzg" # kt 
        }
        
        
        samples = [
        "Rares","WZ","ZZ","Convs","TTW","TTZ","TTWW",
        "ttH_htt","ttH_hww","ttH_hzz","ttH_hzg","ttH_hmm", # kt
        "mcFakes","mcFlips",
        "THQ_htt","THQ_hww","THQ_hzz",
        "THW_htt","THW_hww","THW_hzz"
        "ggH_htt","ggH_hww","ggH_hzz",
        "qqH_htt","qqH_hww","qqH_hzz",
        "VH_htt","VH_hww","VH_hzz",
        ]
        
        for postName in systs_ctcvcp:
        #for postName in [""]:
            print mvaNameDef, "_"+postName
            for channel in channels:
                if postName=="":
                    makeDatacard(mvaNameDef,regions,channel,postName)
                else:
                    makeDatacard(mvaNameDef,regions,channel,"_"+postName)
                #makeDatacard(mvaNameDef+postName,regions,channel,postName[:-1])
    else:
        for channel in channels:
            makeDatacard(mvaNameDef,regions,channel,"")

