#include "mvaTool.C"

std::map<TString,std::map<Int_t, TString>> MapOfChannelMap={
    {"SubCat2l",{{0,"inclusive"},{1,"ee_neg"},{2,"ee_pos"},{3,"em_bl_neg"},{4,"em_bl_pos"},{5,"em_bt_neg"},{6,"em_bt_pos"},{7,"mm_bl_neg"},{8,"mm_bl_pos"},{9,"mm_bt_neg"},{10,"mm_bt_pos"}}}
    };

void runReadingNoMVA(TString sampleName, TString inDir, TString outDir, bool isdata=false, int channel=0, TString keyName="SubCat2l")
{
  //  gROOT->LoadMacro("/publicfs/cms/user/duncanleg/tW13TeV/tmva/mvaTool.C");
  
  std::cout << sampleName;
  mvaTool t = mvaTool(channel, keyName, MapOfChannelMap[keyName] );
  
  t.doReadingNoMVA(sampleName,inDir,outDir, isdata);
  //t.doReading("tW_top_nfh","tW/","output/");
  
}
