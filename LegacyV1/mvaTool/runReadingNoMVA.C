#include "mvaTool.C"
#include "Maps.C"
//#include "Maps_5nodes.C"

void runReadingNoMVA(TString regName, TString binDir, TString sampleName, TString inDir, TString outDir, bool isdata=false, int nPerBin =5, int channel=0, TString keyName="SubCat2l", TString treeName="syncTree", TString baseDir="", int dataEra=2018)
{
  //  gROOT->LoadMacro("/publicfs/cms/user/duncanleg/tW13TeV/tmva/mvaTool.C");
  
  std::cout << sampleName;
  
  mvaTool t;
  if(keyName.Contains("DNN")){
      t = mvaTool(regName, binDir, nPerBin, channel, keyName, treeName, MapOfChannelMap[keyName], IDOfReWeight, baseDir, dataEra, BinMap[keyName] );
  }else{
      t = mvaTool(regName, binDir, nPerBin, channel, keyName, treeName, MapOfChannelMap[keyName], IDOfReWeight, baseDir, dataEra);
  }
  
  t.doReadingNoMVA(sampleName,inDir,outDir, isdata);
  //t.doReading("tW_top_nfh","tW/","output/");
  
}
