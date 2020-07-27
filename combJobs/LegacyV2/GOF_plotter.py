#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sys
from ROOT import gROOT
from ROOT import gStyle
from ROOT import gDirectory
from ROOT import TFile
from ROOT import TCanvas, TLine
from ROOT import TGraph
from ROOT import TLegend
from ROOT import TH2F
from ROOT import TLatex


# In[4]:

toy_file = "higgsCombinetoys300.GoodnessOfFit.mH120.379859881.root"
data_file = "higgsCombinedata_obs.GoodnessOfFit.mH120.-1811406412.root"
saveout = "GOF_test"


# In[5]:


def BestFit(tree):
    n = tree.Draw("limit>>h1","quantileExpected==-1","")
    h1 = gROOT.FindObject("h1").Clone()
    if h1.GetEntries() > 1:
        print ("ERROR Best Fit hist has more than 1 entries ")
        sys.exit()
    bestFit = h1.GetMean()
    
    print ("BestFit from data_file: %s"%bestFit)
    return bestFit


# In[6]:


treeName = "limit"
try:
    dataf = TFile.Open(data_file, "r")
except:
    print("ERROR reading file {}".format(data_file))

try:
    treedata = dataf.Get(treeName)
except:
    print("ERROR reading tree {} from file {}".format(treeName, data_file))


# In[7]:


v_obs = BestFit(treedata)


# In[8]:


try:
    toyf = TFile.Open(toy_file, "r")
except:
    print("ERROR reading file {}".format(toy_file))

try:
    treetoy = toyf.Get(treeName)
except:
    print("ERROR reading tree {} from file {}".format(treeName, toy_file))


# In[9]:


def ToyFit(tree, data_obs):
    x = tree.Draw("limit>>h2")
    h2 = gROOT.FindObject("h2").Clone()
    nentries = h2.GetEntries()
    h2.Scale(1./h2.Integral())
    cdf = h2.GetCumulative()
    CL99 = cdf.GetBinCenter(cdf.FindFirstBinAbove(0.99))
    CL95 = cdf.GetBinCenter(cdf.FindFirstBinAbove(0.95))
    CL90 = cdf.GetBinCenter(cdf.FindFirstBinAbove(0.90))
    p_value = 1-cdf.GetBinContent(cdf.FindBin(data_obs))
    print (" CL90: {}\n CL95: {}\n CL99: {}\n obs: {} \n p_value: {}\n sample size {} \n toy_file {}".format(CL90,CL95,CL99,data_obs,p_value,nentries,toy_file))
    return CL90, CL95, CL99, p_value, h2


# In[10]:


cl90, cl95, cl99, P_value, toy_hist =ToyFit(treetoy, v_obs)


# In[11]:


gStyle.SetOptStat(0)


# In[12]:


def plot_GOF(hist, obs, critical, p_value, alpha="0.05"):
    # canvas
    canv = TCanvas("canv","canv", 600,600)
    canv.SetBottomMargin(0.10)
    canv.SetLeftMargin(0.15)
    canv.SetRightMargin(0.12)
    # histograms
    hist.SetMarkerColor(0)
    hist.SetTitle("GOF test - toys {}".format(int(hist.GetEntries())))
    hist.GetXaxis().SetTitleFont(43)
    hist.GetYaxis().SetTitleFont(43)
    hist.GetXaxis().SetTitleSize(20)
    hist.GetYaxis().SetTitleSize(20)
    hist.GetXaxis().SetTitleOffset(0.8)
    hist.GetYaxis().SetTitleOffset(1.5)
    hist.GetXaxis().SetTitle("Statistics")
    hist.GetYaxis().SetTitle("Probability")
    hist.Draw("hist")
    up = hist.GetMaximum()
    hist.GetYaxis().SetRangeUser(0, 1.2*up)
    # lines
    c_line = TLine(critical,0, critical, 1.2*up )
    c_line.SetLineColor(2)
    c_line.SetLineWidth(4)
    c_line.SetLineStyle(2)
    c_line.Draw("L same")
    obs_line = TLine(obs, 0, obs, 1.2*up)
    obs_line.SetLineColor(1)
    obs_line.SetLineWidth(4)
    obs_line.Draw("L same")
    # legend
    leg = TLegend(0.6, 0.65, .95, .95)
    leg.SetFillColor(0)
    leg.SetShadowColor(0)
    leg.SetLineColor(0)
    leg.SetTextFont(43)
    leg.SetTextSize(18)
    leg.AddEntry(c_line, "alpha = {}".format(alpha), 'L')
    leg.AddEntry(obs_line, "data (p-value={0:.2f})".format(p_value), 'L')
    leg.AddEntry(hist, "toys", "L")
    leg.Draw("same")
    # save canvas
    canv.SaveAs("{}.pdf".format(saveout))
    canv.SaveAs("{}.png".format(saveout))
    canv.SaveAs("{}.root".format(saveout))
    
    return canv


# In[13]:


c1 = plot_GOF(toy_hist, v_obs, cl95, P_value, "0.05")






