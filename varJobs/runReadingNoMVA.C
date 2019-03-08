#include "mvaTool.C"
#include "Maps.C"


void runReadingNoMVA(TString regName, TString binDir, TString sampleName, TString inDir, TString outDir, bool isdata=false, int channel=0, TString keyName="SubCat2l", TString treeName="syncTree")
{
  //  gROOT->LoadMacro("/publicfs/cms/user/duncanleg/tW13TeV/tmva/mvaTool.C");
  
  std::cout << sampleName;
  mvaTool t = mvaTool(regName, binDir, channel, keyName, treeName, MapOfChannelMap[keyName] );
  
  t.doReadingNoMVA(sampleName,inDir,outDir, isdata);
  //t.doReading("tW_top_nfh","tW/","output/");
  
}
