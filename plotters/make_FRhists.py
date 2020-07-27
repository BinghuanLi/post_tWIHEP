from ROOT import TH1F, TH2F, TFile, TTree
from ROOT import gROOT, gStyle
from ROOT import TCanvas

gROOT.SetBatch(1)
gROOT.Reset()
gStyle.SetCanvasColor(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetOptStat(0)
gStyle.SetTitleX(0.5) # title X location
gStyle.SetTitleY(0.96) # title Y location 
gStyle.SetPaintTextFormat(".2f")

def draw_underflow_overflow(h1):
    h1.GetXaxis().SetRange(0, h1.GetNbinsX() + 1)
    h1.Draw()
    return h1

def fill_underflow_overflow(h1):
    nbin = h1.GetNbinsX()
    h1.Fill(h1.GetBinCenter(1),h1.GetBinContent(0))
    h1.Fill(h1.GetBinCenter(nbin),h1.GetBinContent(nbin+1)) 
    h1.Draw()
    return h1


Canv = TCanvas("c1","c1",0,0,800,600)
f_out = TFile(filename,"recreate")

for sample in sampleName:
    file0 = TFile(inputDirectories+sample+postfix,"read")
    if file0.IsZombie():
        print ("file %s is Zombie in make_hists.py" %(inputDirectories+sample+postfix))
        continue
    if not file0.GetListOfKeys().Contains(treename):
        print ("file %s doesn't contains tree %s in make_hists.py"%((inputDirectories+sample+postfix), treename))
        continue
    tree0 = file0.Get(treename)
    for feature, values in features.items():
        for syst in systematics:
            if syst == "nominal":
                if "mcFakes" not in sample: continue 
                hist_name = sample+"_"+feature + "_" + region +"Fakes"
                h01 = TH1F(hist_name, hist_name, values["nbin"], values["min"], values["max"])
                h01.Sumw2()
                input01 = "%s>>%s"%(feature,hist_name)
                tmp_cut = Cuts["TT_mcFakes_%sFakes"%region]
                CUT = "%s%s"%(values["cut"],tmp_cut)
                print (input01,CUT)
                tree0.Draw(input01,CUT)
                h_tmp = fill_underflow_overflow(h01)
                f_out.cd()
                h_tmp.Write() 
                #h01.Write() 

            else:
                for var in upDown:
                    if "ddFakes" not in sample: continue 
                    hist_name = sample+"_"+feature+"_"+syst+"_"+region+var
                    h01 = TH1F(hist_name, hist_name, values["nbin"], values["min"], values["max"])
                    h01.Sumw2()
                    input01 = "%s>>%s"%(feature,hist_name)
                    tmp_cut = Cuts["TT_ddFakes_%s%s"%(region,var)]
                    CUT = "%s%s"%(values["cut"],tmp_cut)
                    tree0.Draw(input01,CUT)
                    h_tmp = fill_underflow_overflow(h01)
                    f_out.cd()
                    #h01.Write() 
                    h_tmp.Write() 

f_out.Close()
    
