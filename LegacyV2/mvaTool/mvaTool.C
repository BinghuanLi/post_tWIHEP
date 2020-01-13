#define mvaTool_cxx
#include "mvaTool.h"

mvaTool::mvaTool(TString regName, TString binDir, Int_t nPerBin, Int_t channel, TString Category, TString TreeName, std::map<Int_t, TString> channelNameMap, std::map<TString, int> IDOfReWeight, TString inputbaseDir, int dataEra, TString varName, std::map<TString, Int_t> DNNBinMap){
  
  _channel = channel;
  _nPerBin = nPerBin;
  _IDOfReWeight = IDOfReWeight;
  _DNNBinMap = DNNBinMap;
  subCat2l = Category;
  _varName = varName;
  treeName = TreeName+varName;
  ChannelNameMap = channelNameMap;
  BinDir = binDir;
  RegName = regName;
  _inputbaseDir = inputbaseDir;
  _systMap = {
    {"JESUp_FlavorQCD","_CMS_scale_j_jesFlavorQCD_up"}, {"JESUp_RelativeBal","_CMS_scale_j_jesRelativeBal_up"}, {"JESUp_HF","_CMS_scale_j_jesHF_up"}, {"JESUp_BBEC1","_CMS_scale_j_jesBBEC1_up"}, {"JESUp_EC2","_CMS_scale_j_jesEC2_up"},
    {"JESUp_Absolute","_CMS_scale_j_jesAbsolute_up"}, {"JESUp_BBEC1_2016","_CMS_scale_j_jesBBEC1_2016_up"}, {"JESUp_EC2_2016","_CMS_scale_j_jesEC2_2016_up"}, {"JESUp_Absolute_2016","_CMS_scale_j_jesAbsolute_2016_up"}, {"JESUp_HF_2016","_CMS_scale_j_jesHF_2016_up"},
    {"JESUp_RelativeSample_2016","_CMS_scale_j_jesRelativeSample_2016_up"}, {"JESUp_BBEC1_2017","_CMS_scale_j_jesBBEC1_2017_up"}, {"JESUp_EC2_2017","_CMS_scale_j_jesEC2_2017_up"}, {"JESUp_Absolute_2017","_CMS_scale_j_jesAbsolute_2017_up"}, {"JESUp_HF_2017","_CMS_scale_j_jesHF_2017_up"},
    {"JESUp_RelativeSample_2017","_CMS_scale_j_jesRelativeSample_2017_up"}, {"JESUp_BBEC1_2018","_CMS_scale_j_jesBBEC1_2018_up"}, {"JESUp_EC2_2018","_CMS_scale_j_jesEC2_2018_up"}, {"JESUp_Absolute_2018","_CMS_scale_j_jesAbsolute_2018_up"}, {"JESUp_HF_2018","_CMS_scale_j_jesHF_2018_up"},
    {"JESUp_RelativeSample_2018","_CMS_scale_j_jesRelativeSample_2018_up"},
    {"JESDown_FlavorQCD","_CMS_scale_j_jesFlavorQCD_down"}, {"JESDown_RelativeBal","_CMS_scale_j_jesRelativeBal_down"}, {"JESDown_HF","_CMS_scale_j_jesHF_down"}, {"JESDown_BBEC1","_CMS_scale_j_jesBBEC1_down"}, {"JESDown_EC2","_CMS_scale_j_jesEC2_down"},
    {"JESDown_Absolute","_CMS_scale_j_jesAbsolute_down"}, {"JESDown_BBEC1_2016","_CMS_scale_j_jesBBEC1_2016_down"}, {"JESDown_EC2_2016","_CMS_scale_j_jesEC2_2016_down"}, {"JESDown_Absolute_2016","_CMS_scale_j_jesAbsolute_2016_down"}, {"JESDown_HF_2016","_CMS_scale_j_jesHF_2016_down"},
    {"JESDown_RelativeSample_2016","_CMS_scale_j_jesRelativeSample_2016_down"}, {"JESDown_BBEC1_2017","_CMS_scale_j_jesBBEC1_2017_down"}, {"JESDown_EC2_2017","_CMS_scale_j_jesEC2_2017_down"}, {"JESDown_Absolute_2017","_CMS_scale_j_jesAbsolute_2017_down"}, {"JESDown_HF_2017","_CMS_scale_j_jesHF_2017_down"},
    {"JESDown_RelativeSample_2017","_CMS_scale_j_jesRelativeSample_2017_down"}, {"JESDown_BBEC1_2018","_CMS_scale_j_jesBBEC1_2018_down"}, {"JESDown_EC2_2018","_CMS_scale_j_jesEC2_2018_down"}, {"JESDown_Absolute_2018","_CMS_scale_j_jesAbsolute_2018_down"}, {"JESDown_HF_2018","_CMS_scale_j_jesHF_2018_down"},
    {"JESDown_RelativeSample_2018","_CMS_scale_j_jesRelativeSample_2018_down"},
  };
  theBinFile = new TFile((binDir+"/OptBin_"+regName+".root"));
  the2DBinFile = new TFile((binDir+"/DNNBin_"+regName+".root"));
  //  regionNames = {"3j1t","3j2t","2j1t","4j1t","4j2t"};
  regionNames = {""};
  _DataEra = dataEra;
  //Start by initialising the list of variables we will base the MVA on

  
  baseName = "";
    /*
    varList.push_back("TrueInteractions");
    varList.push_back("nBestVTX");
    
    varList.push_back("mT_lep1");
    varList.push_back("mT_lep2");
    varList.push_back("Hj_tagger_resTop");
    varList.push_back("Dilep_mtWmin");

    varList.push_back("massll");
    varList.push_back("Sum2lCharge");
    varList.push_back("n_presel_jet");
    varList.push_back("n_presel_ele");
    varList.push_back("n_presel_mu");
    varList.push_back("MHT");
    varList.push_back("metLD");
    varList.push_back("Dilep_bestMVA");
    varList.push_back("Dilep_worseMVA");
    varList.push_back("Dilep_pdgId");
    varList.push_back("Dilep_htllv");
    varList.push_back("Dilep_nTight");
    varList.push_back("HighestJetCSV");
    varList.push_back("HtJet");
    varList.push_back("maxeta");
    varList.push_back("leadLep_jetdr");
    varList.push_back("secondLep_jetdr");
    varList.push_back("minMllAFOS");
    varList.push_back("minMllAFAS");
    varList.push_back("minMllSFOS");
    varList.push_back("nLepFO");
    varList.push_back("nLepTight");
    varList.push_back("puWeight");
    varList.push_back("bWeight");
    varList.push_back("TriggerSF");
    varList.push_back("lepSF");
    varList.push_back("leadLep_BDT");
    varList.push_back("secondLep_BDT");
    varList.push_back("leadLep_corrpt");
    varList.push_back("secondLep_corrpt");
    varList.push_back("mbb");
    varList.push_back("mbb_loose");
    varList.push_back("avg_dr_jet");
    varList.push_back("dr_leps");
    varList.push_back("jet1_pt");
    varList.push_back("jet2_pt");
    varList.push_back("jet3_pt");
    varList.push_back("jet4_pt");
    varList.push_back("jet1_eta");
    varList.push_back("jet2_eta");
    varList.push_back("jet3_eta");
    varList.push_back("jet4_eta");
    varList.push_back("lep1_conePt");
    varList.push_back("lep2_conePt");
    varList.push_back("lep1_eta");
    varList.push_back("lep2_eta");
    varList.push_back("massL");
    varList.push_back("nBJetLoose");
    */
   
    TString catname = ChannelNameMap[_channel];
    TString flag = subCat2l;
    if (flag.Contains("option1")){
        flag.ReplaceAll("option1","");
    }
    
    varList.push_back("DNN_maxval");
    
    varList.push_back("nBJetMedium"); // please always load nBJetMedium
    varList.push_back("Bin2l");
    varList.push_back("mvaOutput_2lss_ttV");
    varList.push_back("mvaOutput_2lss_ttbar");
    varList.push_back("Hj_tagger_hadTop");
    varList.push_back("Hj_tagger");
    varList.push_back("hadTop_BDT");
    if(flag.Contains("DNN")){
        if(subCat2l.Contains("option1")){
        varList.push_back((flag+catname+"_nBin1"));
        varList.push_back((flag+catname+"_nBin2"));
        varList.push_back((flag+catname+"_nBin3"));
        varList.push_back((flag+catname+"_nBin4"));
        varList.push_back((flag+catname+"_nBin5"));
        varList.push_back((flag+catname+"_nBin6"));
        varList.push_back((flag+catname+"_nBin7"));
        varList.push_back((flag+catname+"_nBin8"));
        varList.push_back((flag+catname+"_nBin9"));
        varList.push_back((flag+catname+"_nBin10"));
        varList.push_back((flag+catname+"_nBin11"));
        varList.push_back((flag+catname+"_nBin12"));
        varList.push_back((flag+catname+"_nBin13"));
        varList.push_back((flag+catname+"_nBin14"));
        varList.push_back((flag+catname+"_nBin15"));
        varList.push_back((flag+catname+"_nBin16"));
        varList.push_back((flag+catname+"_nBin17"));
        varList.push_back((flag+catname+"_nBin18"));
        varList.push_back((flag+catname+"_nBin19"));
        varList.push_back((flag+"BIN"));
        }else{
        varList.push_back((flag+"_"+catname+"_nBin1"));
        varList.push_back((flag+"_"+catname+"_nBin2"));
        varList.push_back((flag+"_"+catname+"_nBin3"));
        varList.push_back((flag+"_"+catname+"_nBin4"));
        varList.push_back((flag+"_"+catname+"_nBin5"));
        varList.push_back((flag+"_"+catname+"_nBin6"));
        varList.push_back((flag+"_"+catname+"_nBin7"));
        varList.push_back((flag+"_"+catname+"_nBin8"));
        varList.push_back((flag+"_"+catname+"_nBin9"));
        varList.push_back((flag+"_"+catname+"_nBin10"));
        varList.push_back((flag+"_"+catname+"_nBin11"));
        varList.push_back((flag+"_"+catname+"_nBin12"));
        varList.push_back((flag+"_"+catname+"_nBin13"));
        varList.push_back((flag+"_"+catname+"_nBin14"));
        varList.push_back((flag+"_"+catname+"_nBin15"));
        varList.push_back((flag+"_"+catname+"_nBin16"));
        varList.push_back((flag+"_"+catname+"_nBin17"));
        varList.push_back((flag+"_"+catname+"_nBin18"));
        varList.push_back((flag+"_"+catname+"_nBin19"));
        varList.push_back((flag+"_"+"BIN"));
        }
        
    }
    /* 
    varList.push_back("DNNCat_2DBin_GT10");
    varList.push_back("DNNCat_2DBin_GT15");
    varList.push_back("DNNCat_2DBin_GT20");
    varList.push_back("DNNSubCat2_2DBin_GT5");
    varList.push_back("DNNSubCat2_2DBin_GT10");
    varList.push_back("DNNSubCat2_2DBin_GT15");
    varList.push_back("DNNSubCat2_2DBin_GT20");
    */
  
  //At some point this should be filled out with the names of the systematics so that we can read those too
  if(_varName.Contains("JERUp")){
    systlist.push_back("_CMS_ttHl_JER_up"); 
  }
  if(_varName.Contains("JERDown")){
    systlist.push_back("_CMS_ttHl_JER_down"); 
  }
  if(_varName.Contains("MetShiftUp")){
    systlist.push_back("_CMS_ttHl_UnclusteredEn_up"); 
  }
  if(_varName.Contains("MetShiftDown")){
    systlist.push_back("_CMS_ttHl_UnclusteredEn_down"); 
  }
  if(_varName.Contains("JESUp") || _varName.Contains("JESDown")){
    systlist.push_back(_systMap[_varName]); 
  }
  if (_varName ==""){
    systlist.push_back("");
    systlist.push_back("_PU_16_up");
    systlist.push_back("_PU_16_down");
    systlist.push_back("_PU_17_up");
    systlist.push_back("_PU_17_down");
    systlist.push_back("_PU_18_up");
    systlist.push_back("_PU_18_down");
    systlist.push_back("_CMS_ttHl16_L1PreFiring_up");
    systlist.push_back("_CMS_ttHl16_L1PreFiring_down");
    systlist.push_back("_CMS_ttHl17_L1PreFiring_up");
    systlist.push_back("_CMS_ttHl17_L1PreFiring_down");
    systlist.push_back("_CMS_ttHl16_trigger_up");
    systlist.push_back("_CMS_ttHl16_trigger_down");
    systlist.push_back("_CMS_ttHl17_trigger_up");
    systlist.push_back("_CMS_ttHl17_trigger_down");
    systlist.push_back("_CMS_ttHl18_trigger_up");
    systlist.push_back("_CMS_ttHl18_trigger_down");
    systlist.push_back("_CMS_ttHl_lepEff_elloose_up");
    systlist.push_back("_CMS_ttHl_lepEff_elloose_down");
    systlist.push_back("_CMS_ttHl_lepEff_eltight_up");
    systlist.push_back("_CMS_ttHl_lepEff_eltight_down");
    systlist.push_back("_CMS_ttHl_lepEff_muloose_up");
    systlist.push_back("_CMS_ttHl_lepEff_muloose_down");
    systlist.push_back("_CMS_ttHl_lepEff_mutight_up");
    systlist.push_back("_CMS_ttHl_lepEff_mutight_down");
    systlist.push_back("_CMS_ttHl16_btag_HFStats1_up"); 
    systlist.push_back("_CMS_ttHl16_btag_HFStats1_down"); 
    systlist.push_back("_CMS_ttHl16_btag_HFStats2_up"); 
    systlist.push_back("_CMS_ttHl16_btag_HFStats2_down"); 
    systlist.push_back("_CMS_ttHl16_btag_LFStats1_up"); 
    systlist.push_back("_CMS_ttHl16_btag_LFStats1_down"); 
    systlist.push_back("_CMS_ttHl16_btag_LFStats2_up"); 
    systlist.push_back("_CMS_ttHl16_btag_LFStats2_down"); 
    systlist.push_back("_CMS_ttHl17_btag_HFStats1_up"); 
    systlist.push_back("_CMS_ttHl17_btag_HFStats1_down"); 
    systlist.push_back("_CMS_ttHl17_btag_HFStats2_up"); 
    systlist.push_back("_CMS_ttHl17_btag_HFStats2_down"); 
    systlist.push_back("_CMS_ttHl17_btag_LFStats1_up"); 
    systlist.push_back("_CMS_ttHl17_btag_LFStats1_down"); 
    systlist.push_back("_CMS_ttHl17_btag_LFStats2_up"); 
    systlist.push_back("_CMS_ttHl17_btag_LFStats2_down"); 
    systlist.push_back("_CMS_ttHl18_btag_HFStats1_up"); 
    systlist.push_back("_CMS_ttHl18_btag_HFStats1_down"); 
    systlist.push_back("_CMS_ttHl18_btag_HFStats2_up"); 
    systlist.push_back("_CMS_ttHl18_btag_HFStats2_down"); 
    systlist.push_back("_CMS_ttHl18_btag_LFStats1_up"); 
    systlist.push_back("_CMS_ttHl18_btag_LFStats1_down"); 
    systlist.push_back("_CMS_ttHl18_btag_LFStats2_up"); 
    systlist.push_back("_CMS_ttHl18_btag_LFStats2_down"); 
    systlist.push_back("_CMS_ttHl_btag_cErr1_up"); 
    systlist.push_back("_CMS_ttHl_btag_cErr1_down"); 
    systlist.push_back("_CMS_ttHl_btag_cErr2_up"); 
    systlist.push_back("_CMS_ttHl_btag_cErr2_down"); 
    systlist.push_back("_CMS_ttHl_btag_LF_up"); 
    systlist.push_back("_CMS_ttHl_btag_LF_down"); 
    systlist.push_back("_CMS_ttHl_btag_HF_up"); 
    systlist.push_back("_CMS_ttHl_btag_HF_down"); 
    systlist.push_back("_CMS_ttHl_FRm_norm_up");
    systlist.push_back("_CMS_ttHl_FRm_norm_down");
    systlist.push_back("_CMS_ttHl_FRm_pt_up");
    systlist.push_back("_CMS_ttHl_FRm_pt_down");
    systlist.push_back("_CMS_ttHl_FRm_be_up");
    systlist.push_back("_CMS_ttHl_FRm_be_down");
    systlist.push_back("_CMS_ttHl_FRe_norm_up");
    systlist.push_back("_CMS_ttHl_FRe_norm_down");
    systlist.push_back("_CMS_ttHl_FRe_pt_up");
    systlist.push_back("_CMS_ttHl_FRe_pt_down");
    systlist.push_back("_CMS_ttHl_FRe_be_up");
    systlist.push_back("_CMS_ttHl_FRe_be_down");
    systlist.push_back("_CMS_ttHl_Clos_m_shape_up");
    systlist.push_back("_CMS_ttHl_Clos_m_shape_down");
    systlist.push_back("_CMS_ttHl_Clos_m_norm_up");
    systlist.push_back("_CMS_ttHl_Clos_m_norm_down");
    systlist.push_back("_CMS_ttHl_Clos_e_shape_up");
    systlist.push_back("_CMS_ttHl_Clos_e_shape_down");
    systlist.push_back("_CMS_ttHl_Clos_e_norm_up");
    systlist.push_back("_CMS_ttHl_Clos_e_norm_down");
    systlist.push_back("_CMS_ttHl_QF_up");
    systlist.push_back("_CMS_ttHl_QF_down");
    systlist.push_back("_CMS_ttHl_thu_shape_ttH_x1_up");
    systlist.push_back("_CMS_ttHl_thu_shape_ttH_x1_down");
    systlist.push_back("_CMS_ttHl_thu_shape_ttH_y1_up");
    systlist.push_back("_CMS_ttHl_thu_shape_ttH_y1_down");
  }
  for (auto& IDs : _IDOfReWeight){
    //std::cout<< " push_back systlist "<< IDs.first <<std::endl;
    systlist.push_back("_"+IDs.first);
  }
}

void mvaTool::doReading(TString sampleName, TString inDir, TString outDir, bool isData){
  
  std::cout << "Entering reading routine" << std::endl;
  TMVA::Tools::Instance();

  //Get the reader object
  reader = new TMVA::Reader( "!Color:!Silent" );
  unsigned int varsize = varList.size();
  float treevars[varsize];
  //int treevars[varsize];

  std::cout << "Entering variable adding" << std::endl;
  for (unsigned int i=0; i<varsize;i++){
    treevars[i] = 0;
    std::cout << "[Variable loop] Adding variable: " << varList[i].Data() << std::endl;
    reader->AddVariable( varList[i].Data(), &(treevars[i]) );
  }

  reader->BookMVA( "BDT_ttbar", baseName+"loader/weights/tWLepJet_training_BDT_Grad_1000_20_0.1_ttbar.weights.xml" );
  //  reader->BookMVA( "BDT_wJets", baseName+"loader/weights/tWLepJet_training_BDT_Grad_1000_20_0.1_wJets.weights.xml" );

  std::cout << "Finished reading BDT training" << std::endl;

  std::cout << "Processing sample: " << sampleName << std::endl;
  
  processMCSample(sampleName,inDir,outDir,treevars, isData);
  
  std::cout << "Finished processing " << sampleName << std::endl;
  
}

void mvaTool::doReadingNoMVA(TString sampleName, TString inDir, TString outDir, bool isData){
  
  std::cout << "Entering reading routine" << std::endl;

  unsigned int varsize = varList.size();
  float treevars[varsize];
  //int treevars[varsize];

  std::cout << "Entering variable adding" << std::endl;
  for (unsigned int i=0; i<varsize;i++){
    treevars[i] = 0;
    std::cout << "[Variable loop] Adding variable: " << varList[i].Data() << std::endl;
  }


  std::cout << "Finished reading BDT training" << std::endl;

  std::cout << "Processing sample: " << sampleName << std::endl;
  
  processMCSample(sampleName,inDir,outDir,treevars,isData, false);
  
  std::cout << "Finished processing " << sampleName << std::endl;
  
}


//Do the thing
void mvaTool::processMCSample(TString sampleName, TString inDir, TString outDir, float * treevars, bool isData, bool doMVA){

  TString dirWithTrees = _inputbaseDir + "/"+RegName+"/"+std::to_string(_DataEra)+"/"+inDir+"/"+sampleName+"_"+RegName+".root";
  std::vector<TFile*> theoutputfiles;
  for (auto const regionName : regionNames){
    std::cout << "Createing file " << outDir+regionName+"/output_"+ChannelNameMap[_channel]+"_"+sampleName+".root" <<std::endl;
    TFile *theoutputfile = new TFile( (outDir+regionName+"/output_"+ChannelNameMap[_channel]+"_"+sampleName+".root").Data(), "update");//change to update for adding variations
    theoutputfiles.push_back(theoutputfile);
  }

  std::cout << "Files have been create" << std::endl;
  //  TFile *thetreefile = new TFile( (outDir+"bdtTree_"+sampleName+".root").Data(), "RECREATE");
  //theTreeOutputFileMap[sampleName] = thetreefile;
  
  //------------------------
  // Systematic loop
  //------------------------
  // WIP. This will include the additional files at some point
  

  for (unsigned int j=0; j < systlist.size(); j++){
    if (isData && sampleName !="Fakes" && sampleName!="Flips" && systlist[j] != "") continue;
    if (isData && sampleName =="Fakes" && !(systlist[j].Contains("_FRm_") || systlist[j].Contains("_FRe_") || systlist[j].Contains("_Clos_m_") || systlist[j].Contains("_Clos_e_") || systlist[j] == ""))continue;
    if (!isData && sampleName =="FakeSub" && !(systlist[j].Contains("_FRm_") || systlist[j].Contains("_FRe_") || systlist[j].Contains("_Clos_m_") || systlist[j].Contains("_Clos_e_") || systlist[j] == "" ))continue;
    if (!isData && sampleName !="FakeSub" && (systlist[j].Contains("_FRm_") || systlist[j].Contains("_FRe_") || systlist[j].Contains("_Clos_m_") || systlist[j].Contains("_Clos_e_")))continue;
    if (isData && sampleName =="Flips" && !(systlist[j].Contains("ttHl_QF") || systlist[j] ==""))continue;
    if (!(sampleName.Contains("ttH") || sampleName.Contains("THQ") || sampleName.Contains("THW")) && ((systlist[j].Contains("_kt_") && systlist[j].Contains("_kv_"))|| systlist[j].Contains("cosa")))continue;
    //std::cout<<" createHist " << sampleName << systlist[j] << std::endl;
    createHists(sampleName+systlist[j]);
  }

  
  loopInSample(dirWithTrees,sampleName,treevars,isData,doMVA);
  //makeStatVariationHists(sampleName,theoutputfiles); //We do this in processMCSample so that we have the output file to save the stat variations into.

  saveHists(theoutputfiles);
    
  for (auto const outputfile: theoutputfiles){
    outputfile->Close();
    delete outputfile;
  }
}

//Loop over the events in the desired sample
void mvaTool::loopInSample(TString dirWithTrees, TString sampleName, float* treevars, bool isData, bool doMVA){

  unsigned int varsize = varList.size();

  //TChain* theTree = new TChain("syncTree");
  TChain* theTree = new TChain(treeName);
  theTree->Add(dirWithTrees);
  std::cout << "[loopInSample] Added "<<dirWithTrees << " to TChain" << std::endl;
  
  for (unsigned int ivar=0; ivar<varsize; ivar++) theTree->SetBranchAddress( varList[ivar].Data(), &(treevars[ivar]));

  

  std::cout << "[loopInSample] Finished assigning variables" << std::endl;
  theweight=0.;
  theTree->SetBranchAddress( "EventWeight", &theweight );
  if(theTree->GetListOfBranches()->FindObject("EVENT_rWeights") ){
  theTree->SetBranchAddress("EVENT_rWeights", &EVENT_rWeights);
  EVENT_rWeights->clear();
  };
  if(theTree->GetListOfBranches()->FindObject("EVENT_genWeights") ){
  theTree->SetBranchAddress("EVENT_genWeights", &EVENT_genWeights);
  EVENT_genWeights->clear();
  };

  //Get the systematic weights here. We will then fill hists separately as a result of this.
  float puWeight=0., puWeightUp = 0., puWeightDown = 0.;
  float ChargeMis=0., ChargeMisUp = 0., ChargeMisDown = 0.;
  float lepSFWeight=0., elelooseSFWeight=0. , eletightSFWeight=1., mulooseSFWeight=0., mutightSFWeight=1.;
  float elelooseSFWeightUp = 0., elelooseSFWeightDown = 0., eletightSFWeightUp = 1., eletightSFWeightDown = 1., mulooseSFWeightUp = 0., mulooseSFWeightDown = 0., mutightSFWeightUp = 1., mutightSFWeightDown = 1.;
  // prefire 
  float Prefire(0.), Prefire_SysUp(0.), Prefire_SysDown(0.);
  // genWeights
  double genWeight =0.;
  float genWeight_muF0p5(0.), genWeight_muF2(0.), genWeight_muR0p5(0.), genWeight_muR2(0.); // x1 down, x1 up, y1 down , y1 up
  float CMS_ttHl_thu_shape_ttH(0.), CMS_ttHl_thu_shape_ttH_up(0.), CMS_ttHl_thu_shape_ttH_down(0.);
  float CMS_ttHl_thu_shape_ttW(0.), CMS_ttHl_thu_shape_ttW_up(0.), CMS_ttHl_thu_shape_ttW_down(0.);
  float CMS_ttHl_thu_shape_ttZ(0.), CMS_ttHl_thu_shape_ttZ_up(0.), CMS_ttHl_thu_shape_ttZ_down(0.);
  
  float trigSFWeight=0., trigSFWeightUp = 0., trigSFWeightDown = 0.;
  float bWeight=0., bWeightlfs1Up = 0., bWeightlfs1Down = 0., bWeightlfs2Up = 0., bWeightlfs2Down = 0., bWeighthfs1Up = 0., bWeighthfs1Down = 0., bWeighthfs2Up = 0., bWeighthfs2Down = 0., bWeightcferr1Up = 0., bWeightcferr1Down = 0., bWeightcferr2Up = 0., bWeightcferr2Down = 0., bWeightjerUp = 0., bWeightjerDown = 0., bWeightlfUp = 0., bWeightlfDown = 0., bWeighthfUp = 0., bWeighthfDown = 0.;
  float mistagWeight=0., mistagWeighthfs1Up = 0., mistagWeighthfs1Down = 0., mistagWeighthfs2Up = 0., mistagWeighthfs2Down = 0., mistagWeightcferr1Up = 0., mistagWeightcferr1Down = 0., mistagWeightcferr2Up = 0., mistagWeightcferr2Down = 0., mistagWeightjerUp = 0., mistagWeightjerDown = 0., mistagWeightlfUp = 0., mistagWeightlfDown = 0.;
 
  float FakeRateWeight=0., FakeRateWeight_m_normUp=0.,FakeRateWeight_m_normDown=0., FakeRateWeight_e_normUp=0.,FakeRateWeight_e_normDown=0., FakeRateWeight_m_ptUp=0.,FakeRateWeight_m_ptDown=0., FakeRateWeight_e_ptUp=0.,FakeRateWeight_e_ptDown=0., FakeRateWeight_m_beUp=0.,FakeRateWeight_m_beDown=0., FakeRateWeight_e_beUp=0.,FakeRateWeight_e_beDown=0.;

  // fake rate closures
  float FakeRate_Clos_m_shape(1.), FakeRate_Clos_m_shape_up(1.), FakeRate_Clos_m_shape_down(1.);
  float FakeRate_Clos_e_shape(1.), FakeRate_Clos_e_shape_up(1.), FakeRate_Clos_e_shape_down(1.);
  float FakeRate_Clos_m_norm(1.), FakeRate_Clos_m_norm_up(1.), FakeRate_Clos_m_norm_down(1.);
  float FakeRate_Clos_e_norm(1.), FakeRate_Clos_e_norm_up(1.), FakeRate_Clos_e_norm_down(1.);
  float FakeRate_Clos_m_bt_norm(1.), FakeRate_Clos_m_bt_norm_up(1.), FakeRate_Clos_m_bt_norm_down(1.);
  float FakeRate_Clos_e_bt_norm(1.), FakeRate_Clos_e_bt_norm_up(1.), FakeRate_Clos_e_bt_norm_down(1.);
  float FakeRate_Clos_m_shape_mm_up(1.), FakeRate_Clos_m_shape_mm_down(1.);
  float FakeRate_Clos_m_shape_em_up(1.), FakeRate_Clos_m_shape_em_down(1.);
  float FakeRate_Clos_e_shape_ee_up(1.), FakeRate_Clos_e_shape_ee_down(1.);
  float FakeRate_Clos_e_shape_em_up(1.), FakeRate_Clos_e_shape_em_down(1.);
 
  double pdfUp = 0., pdfDown = 0.;
 
 
 
  float Dilepton_flav = 0.; // 1: mm , 2: em, 3: ee
  float lep1_pdgId(0.), lep2_pdgId(0.);
  int nbJets3040 = 0., nbJets4000 = 0.;

  double met = -100.,metPhi = 100.;
  float lepPt = -100., lepPhi = 100.;

  float theChannel = 0;
  
  
  theTree->SetBranchAddress( subCat2l.Data(),&theChannel);
  if (doMVA){
    //theTree->SetBranchAddress( "channel",&theChannel);
    theTree->SetBranchAddress( "M_nBJet3040",&nbJets3040);
    theTree->SetBranchAddress( "M_nBJet4000",&nbJets4000);
  }
    
    theTree->SetBranchAddress( "lep1_pdgId", &lep1_pdgId );
    theTree->SetBranchAddress( "lep2_pdgId", &lep2_pdgId );
  //if (!isData){
    theTree->SetBranchAddress( "puWeight", &puWeight );
    theTree->SetBranchAddress( "puWeight_SysUp", &puWeightUp );
    theTree->SetBranchAddress( "puWeight_SysDown", &puWeightDown );
  
    
    std::cout << "[loopInSample] Finished assigning pileup weights" << std::endl;

    theTree->SetBranchAddress( "lepSF", &lepSFWeight );
    theTree->SetBranchAddress( "elelooseSF_SysUp", &elelooseSFWeightUp );
    theTree->SetBranchAddress( "elelooseSF", &elelooseSFWeight );
    theTree->SetBranchAddress( "elelooseSF_SysDown", &elelooseSFWeightDown );
    theTree->SetBranchAddress( "mulooseSF_SysUp", &mulooseSFWeightUp );
    theTree->SetBranchAddress( "mulooseSF", &mulooseSFWeight );
    theTree->SetBranchAddress( "mulooseSF_SysDown", &mulooseSFWeightDown );
    theTree->SetBranchAddress( "mutightSF_SysUp", &mutightSFWeightUp );
    theTree->SetBranchAddress( "mutightSF", &mutightSFWeight );
    theTree->SetBranchAddress( "mutightSF_SysDown", &mutightSFWeightDown );
    theTree->SetBranchAddress( "eletightSF_SysUp", &eletightSFWeightUp );
    theTree->SetBranchAddress( "eletightSF", &eletightSFWeight );
    theTree->SetBranchAddress( "eletightSF_SysDown", &eletightSFWeightDown );
    theTree->SetBranchAddress( "TriggerSF", &trigSFWeight );
    theTree->SetBranchAddress( "TriggerSF_SysUp", &trigSFWeightUp );
    theTree->SetBranchAddress( "TriggerSF_SysDown", &trigSFWeightDown );
    
    theTree->SetBranchAddress( "EVENT_genWeight", &genWeight );
    theTree->SetBranchAddress( "genWeight_muF0p5", &genWeight_muF0p5 );
    theTree->SetBranchAddress( "genWeight_muF2", &genWeight_muF2 );
    theTree->SetBranchAddress( "genWeight_muR0p5", &genWeight_muR0p5 );
    theTree->SetBranchAddress( "genWeight_muR2", &genWeight_muR2 );
    theTree->SetBranchAddress( "Prefire", &Prefire );
    theTree->SetBranchAddress( "Prefire_SysUp", &Prefire_SysUp );
    theTree->SetBranchAddress( "Prefire_SysDown", &Prefire_SysDown );
    /*
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttH", &CMS_ttHl_thu_shape_ttH );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttH_SysUp", &CMS_ttHl_thu_shape_ttH_up );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttH_SysDown", &CMS_ttHl_thu_shape_ttH_down );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttW", &CMS_ttHl_thu_shape_ttW );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttW_SysUp", &CMS_ttHl_thu_shape_ttW_up );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttW_SysDown", &CMS_ttHl_thu_shape_ttW_down );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttZ", &CMS_ttHl_thu_shape_ttZ );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttZ_SysUp", &CMS_ttHl_thu_shape_ttZ_up );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttZ_SysDown", &CMS_ttHl_thu_shape_ttZ_down );
    */

    theTree->SetBranchAddress( "bWeight_central", &bWeight );
    theTree->SetBranchAddress( "bWeight_up_hfstats1", &bWeighthfs1Up );
    theTree->SetBranchAddress( "bWeight_down_hfstats1", &bWeighthfs1Down );
    theTree->SetBranchAddress( "bWeight_up_hfstats2", &bWeighthfs2Up );
    theTree->SetBranchAddress( "bWeight_down_hfstats2", &bWeighthfs2Down );
    theTree->SetBranchAddress( "bWeight_up_lfstats1", &bWeightlfs1Up );
    theTree->SetBranchAddress( "bWeight_down_lfstats1", &bWeightlfs1Down );
    theTree->SetBranchAddress( "bWeight_up_lfstats2", &bWeightlfs2Up );
    theTree->SetBranchAddress( "bWeight_down_lfstats2", &bWeightlfs2Down );
    theTree->SetBranchAddress( "bWeight_up_cferr1", &bWeightcferr1Up );
    theTree->SetBranchAddress( "bWeight_down_cferr1", &bWeightcferr1Down );
    theTree->SetBranchAddress( "bWeight_up_cferr2", &bWeightcferr2Up );
    theTree->SetBranchAddress( "bWeight_down_cferr2", &bWeightcferr2Down );
    theTree->SetBranchAddress( "bWeight_up_jes", &bWeightjerUp );
    theTree->SetBranchAddress( "bWeight_down_jes", &bWeightjerDown );
    theTree->SetBranchAddress( "bWeight_up_lf", &bWeightlfUp );
    theTree->SetBranchAddress( "bWeight_down_lf", &bWeightlfDown );
    theTree->SetBranchAddress( "bWeight_up_hf", &bWeighthfUp );
    theTree->SetBranchAddress( "bWeight_down_hf", &bWeighthfDown );
    
    
  
  
    /*
    theTree->SetBranchAddress( "misTagWeight_central", &mistagWeight );
    theTree->SetBranchAddress( "misTagWeight_up_hfstats1", &mistagWeighthfs1Up );
    theTree->SetBranchAddress( "misTagWeight_down_hfstats1", &mistagWeighthfs1Down );
    theTree->SetBranchAddress( "misTagWeight_up_hfstats2", &mistagWeighthfs2Up );
    theTree->SetBranchAddress( "misTagWeight_down_hfstats2", &mistagWeighthfs2Down );
    theTree->SetBranchAddress( "misTagWeight_up_cferr1", &mistagWeightcferr1Up );
    theTree->SetBranchAddress( "misTagWeight_down_cferr1", &mistagWeightcferr1Down );
    theTree->SetBranchAddress( "misTagWeight_up_cferr2", &mistagWeightcferr2Up );
    theTree->SetBranchAddress( "misTagWeight_down_cferr2", &mistagWeightcferr2Down );
    theTree->SetBranchAddress( "misTagWeight_up_jes", &mistagWeightjerUp );
    theTree->SetBranchAddress( "misTagWeight_down_jes", &mistagWeightjerDown );
    theTree->SetBranchAddress( "misTagWeight_up_lf", &mistagWeightlfUp );
    theTree->SetBranchAddress( "misTagWeight_down_lf", &mistagWeightlfDown );
     
    theTree->SetBranchAddress( "EVENT_PDFtthbbWeightUp",&pdfUp );
    theTree->SetBranchAddress( "EVENT_PDFtthbbWeightDown",&pdfDown );
    */
    std::cout << "[loopInSample] Finished assigning lepton weights" << std::endl;
    //}else if(sampleName.Contains("Flips")){
        theTree->SetBranchAddress( "ChargeMis", &ChargeMis );
        theTree->SetBranchAddress( "ChargeMis_SysUp", &ChargeMisUp );
        theTree->SetBranchAddress( "ChargeMis_SysDown", &ChargeMisDown );
        std::cout << "[loopInSample] Finished assigning ChargeMis weights" << std::endl;
    //}else if(sampleName.Contains("Fakes")){
        theTree->SetBranchAddress( "FakeRate", &FakeRateWeight);
        theTree->SetBranchAddress( "FakeRate_m_up", &FakeRateWeight_m_normUp);
        theTree->SetBranchAddress( "FakeRate_m_down", &FakeRateWeight_m_normDown);
        theTree->SetBranchAddress( "FakeRate_m_pt1", &FakeRateWeight_m_ptUp);
        theTree->SetBranchAddress( "FakeRate_m_pt2", &FakeRateWeight_m_ptDown);
        theTree->SetBranchAddress( "FakeRate_m_be1", &FakeRateWeight_m_beUp);
        theTree->SetBranchAddress( "FakeRate_m_be2", &FakeRateWeight_m_beDown);
        theTree->SetBranchAddress( "FakeRate_e_up", &FakeRateWeight_e_normUp);
        theTree->SetBranchAddress( "FakeRate_e_down", &FakeRateWeight_e_normDown);
        theTree->SetBranchAddress( "FakeRate_e_pt1", &FakeRateWeight_e_ptUp);
        theTree->SetBranchAddress( "FakeRate_e_pt2", &FakeRateWeight_e_ptDown);
        theTree->SetBranchAddress( "FakeRate_e_be1", &FakeRateWeight_e_beUp);
        theTree->SetBranchAddress( "FakeRate_e_be2", &FakeRateWeight_e_beDown);
        std::cout << "[loopInSample] Finished assigning FakeRate weights" << std::endl;
        theTree->SetBranchAddress( "FakeRate_e_QCD", &FakeRate_Clos_e_shape_up);
        theTree->SetBranchAddress( "FakeRate_e_TT", &FakeRate_Clos_e_shape_down);
        theTree->SetBranchAddress( "FakeRate_m_QCD", &FakeRate_Clos_m_shape_up);
        theTree->SetBranchAddress( "FakeRate_m_TT", &FakeRate_Clos_m_shape_down);
        /*
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_e_shape_ee_SysUp", &FakeRate_Clos_e_shape_ee_up);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_e_shape_ee_SysDown", &FakeRate_Clos_e_shape_ee_down);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_e_shape_em_SysUp", &FakeRate_Clos_e_shape_em_up);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_e_shape_em_SysDown", &FakeRate_Clos_e_shape_em_down);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_m_shape_mm_SysUp", &FakeRate_Clos_m_shape_mm_up);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_m_shape_mm_SysDown", &FakeRate_Clos_m_shape_mm_down);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_m_shape_em_SysUp", &FakeRate_Clos_m_shape_em_up);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_m_shape_em_SysDown", &FakeRate_Clos_m_shape_em_down);
        std::cout << "[loopInSample] Finished assigning FakeRate Closure weights" << std::endl;
        */
  
    //}
    
  
  //  std::vector<float> bTagSysts;
  //  setbTagVars(theTree);
  
  if (theTree ==0) cout << "No TTree found for " << sampleName << "!" << std::endl;

  std::tuple<float,float> bSysts (std::make_pair(1.,1.));
  std::tuple<float,float> mistagSysts (std::make_pair(1.,1.));

  //Loop over the events
  std::cout << theTree->GetEntries() << " events in loop for sample " << sampleName <<" varName " << _varName <<  std::endl; 
  for (int i = 0; i < theTree->GetEntries(); i++){
     
    //if (i > 20000) break;
    if (i%500 == 0){
      printf ("Processing event %i\r", i);
      fflush(stdout);
    }
    theTree->GetEntry(i);
    
    if (fabs(_channel)>0.01 && fabs(theChannel - _channel)>0.01) continue;
    //std::cout << " now fill the channel: "<< ChannelNameMap[_channel]<<std::endl; 
    //cut optimization
    /*
    if(!(
         hadTop_BDT>0.04 && maxeta <2.16 
      && leadLep_jetdr <2.416 && secondLep_jetdr < 1.984
      && lep1_conePt < 280 && lep2_conePt <200
      && Mt_metleadlep < 680
       )) continue;
    */
    //if (theChannel < 0 || theChannel > 4) continue;
    
    // get muF/muR factors
    if(EVENT_genWeights->size()>0){
        genWeight = EVENT_genWeights->at(0);
    }
    float factor_muF0p5(1.), factor_muF2(1.), factor_muR0p5(1.), factor_muR2(1.);

    //std::tie(factor_muF0p5, factor_muF2, factor_muR0p5, factor_muR2) = get_muFmuR_factor(sampleName);

    if (theChannel == 0){ // A backup because I messed up the channel flag in the first reprocessing.
      //      std::cout << "Zero! njets are: " << nbJets4000 << " " << nbJets3040 <<std::endl;
      //if ((nbJets4000 + nbJets3040) != 1) continue;
    }

    if (doMVA)  mvaValue = reader->EvaluateMVA("BDT_ttbar");
    else {
      mvaValue = 0.;
      theChannel = 0;
      Dilepton_flav = (28 - fabs(lep1_pdgId) - fabs(lep2_pdgId))/2;
    }
    //    mvawJetsValue = reader->EvaluateMVA("BDT_wJets");
    mvawJetsValue = 0.;

    float mtw = std::sqrt(2*met*lepPt*(1-cos(metPhi-lepPhi)));
    int nbJet = -1;
    for (unsigned int ivar=0; ivar<varsize; ivar++){
        if(varList[ivar].Contains("nBJetMedium")){
            nbJet = treevars[ivar];
        }
    }
    //    std::cout << met << " " << lepPt << " " << metPhi << " " << lepPhi << " " << mtw << std::endl;
    //std::cout<<" event " << i << std::endl; 
    if(_varName.Contains("JERUp")){
        fillHists(sampleName+"_CMS_ttHl_JER_up",treevars,mvaValue,mvawJetsValue,theweight,met,mtw,theChannel);
    }
    if(_varName.Contains("JERDown")){
        fillHists(sampleName+"_CMS_ttHl_JER_down",treevars,mvaValue,mvawJetsValue,theweight,met,mtw,theChannel);
    }
    if(_varName.Contains("MetShiftUp")){
        fillHists(sampleName+"_CMS_ttHl_UnclusteredEn_up",treevars,mvaValue,mvawJetsValue,theweight,met,mtw,theChannel);
    }
    if(_varName.Contains("MetShiftDown")){
        fillHists(sampleName+"_CMS_ttHl_UnclusteredEn_down",treevars,mvaValue,mvawJetsValue,theweight,met,mtw,theChannel);
    }
    if(_varName.Contains("JESUp") || _varName.Contains("JESDown")){
        fillHists(sampleName+_systMap[_varName],treevars,mvaValue,mvawJetsValue,theweight,met,mtw,theChannel);
    }
    
    //std::cout << " now fill the weight-based systematic histograms "<<std::endl; 
    //Now fill the weight-based systematic histograms
 if(_varName==""){
        fillHists(sampleName,treevars,mvaValue,mvawJetsValue,theweight,met,mtw,theChannel);
   if(theweight!=0){
    if (!isData){
      if(sampleName.Contains("FakeSub")){
        /*
        std::tie(FakeRate_Clos_e_shape_up, FakeRate_Clos_e_shape_down, FakeRate_Clos_m_shape_up, FakeRate_Clos_m_shape_down)=calculateClosSyst(Dilepton_flav , FakeRate_Clos_e_shape_ee_up, FakeRate_Clos_e_shape_ee_down, FakeRate_Clos_e_shape_em_up, FakeRate_Clos_e_shape_em_down, FakeRate_Clos_m_shape_mm_up, FakeRate_Clos_m_shape_mm_down, FakeRate_Clos_m_shape_em_up, FakeRate_Clos_m_shape_em_down);
        calculateClosNormSyst(Dilepton_flav, nbJet, FakeRate_Clos_e_norm_up, FakeRate_Clos_e_norm_down, FakeRate_Clos_e_bt_norm_up, FakeRate_Clos_e_bt_norm_down, FakeRate_Clos_m_norm_up, FakeRate_Clos_m_norm_down, FakeRate_Clos_m_bt_norm_up, FakeRate_Clos_m_bt_norm_down);
        fillHists(sampleName+"_CMS_ttHl_Clos_e_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_norm_up/FakeRate_Clos_e_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_Clos_e_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_norm_down/FakeRate_Clos_e_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_Clos_m_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_norm_up/FakeRate_Clos_m_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_Clos_m_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_norm_down/FakeRate_Clos_m_norm) ,met,mtw,theChannel);
        */
        fillHists(sampleName+"_CMS_ttHl_Clos_e_shape_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_shape_up/FakeRateWeight) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_Clos_e_shape_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_shape_down/FakeRateWeight) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_Clos_m_shape_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_shape_up/FakeRateWeight) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_Clos_m_shape_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_shape_down/FakeRateWeight) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRm_norm_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_normUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRm_norm_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_normDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRm_pt_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_ptUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRm_pt_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_ptDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRm_be_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_beUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRm_be_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_beDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRe_norm_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_normUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRe_norm_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_normDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRe_pt_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_ptUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRe_pt_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_ptDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRe_be_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_beUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_FRe_be_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_beDown/FakeRateWeight),met,mtw,theChannel);
        //fillHists(sampleName+"_bWeight_jes_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightjerUp/bWeight),met,mtw,theChannel);
        //fillHists(sampleName+"_bWeight_jes_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightjerDown/bWeight),met,mtw,theChannel);
      
      }else{
        //calculateLepTightEffSyst(Dilepton_flav,  eletightSFWeightUp,  eletightSFWeightDown,  mutightSFWeightUp,  mutightSFWeightDown);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttH_x1_up",treevars,mvaValue,mvawJetsValue,theweight * (genWeight_muF2/genWeight) * factor_muF2,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttH_x1_down",treevars,mvaValue,mvawJetsValue,theweight * (genWeight_muF0p5/genWeight) * factor_muF0p5,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttH_y1_up",treevars,mvaValue,mvawJetsValue,theweight * (genWeight_muR2/genWeight) * factor_muR2,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttH_y1_down",treevars,mvaValue,mvawJetsValue,theweight * (genWeight_muR0p5/genWeight) * factor_muR0p5,met,mtw,theChannel);
        /*
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttH_up",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttH_up/CMS_ttHl_thu_shape_ttH),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttH_down",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttH_down/CMS_ttHl_thu_shape_ttH),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttW_up",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttW_up/CMS_ttHl_thu_shape_ttW),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttW_down",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttW_down/CMS_ttHl_thu_shape_ttW),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttZ_up",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttZ_up/CMS_ttHl_thu_shape_ttZ),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttZ_down",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttZ_down/CMS_ttHl_thu_shape_ttZ),met,mtw,theChannel);
        */
        fillHists(sampleName+"_CMS_ttHl16_L1PreFiring_up",treevars,mvaValue,mvawJetsValue,theweight * (Prefire_SysUp/Prefire),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_L1PreFiring_down",treevars,mvaValue,mvawJetsValue,theweight * (Prefire_SysDown/Prefire),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_L1PreFiring_up",treevars,mvaValue,mvawJetsValue,theweight * (Prefire_SysUp/Prefire),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_L1PreFiring_down",treevars,mvaValue,mvawJetsValue,theweight * (Prefire_SysDown/Prefire),met,mtw,theChannel);
        fillHists(sampleName+"_PU_16_up",treevars,mvaValue,mvawJetsValue,theweight * (puWeightUp/puWeight),met,mtw,theChannel);
        fillHists(sampleName+"_PU_16_down",treevars,mvaValue,mvawJetsValue,theweight * (puWeightDown/puWeight),met,mtw,theChannel);
        fillHists(sampleName+"_PU_17_up",treevars,mvaValue,mvawJetsValue,theweight * (puWeightUp/puWeight),met,mtw,theChannel);
        fillHists(sampleName+"_PU_17_down",treevars,mvaValue,mvawJetsValue,theweight * (puWeightDown/puWeight),met,mtw,theChannel);
        fillHists(sampleName+"_PU_18_up",treevars,mvaValue,mvawJetsValue,theweight * (puWeightUp/puWeight),met,mtw,theChannel);
        fillHists(sampleName+"_PU_18_down",treevars,mvaValue,mvawJetsValue,theweight * (puWeightDown/puWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_trigger_up",treevars,mvaValue,mvawJetsValue,theweight * (trigSFWeightUp/trigSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_trigger_down",treevars,mvaValue,mvawJetsValue,theweight * (trigSFWeightDown/trigSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_trigger_up",treevars,mvaValue,mvawJetsValue,theweight * (trigSFWeightUp/trigSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_trigger_down",treevars,mvaValue,mvawJetsValue,theweight * (trigSFWeightDown/trigSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl18_trigger_up",treevars,mvaValue,mvawJetsValue,theweight * (trigSFWeightUp/trigSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl18_trigger_down",treevars,mvaValue,mvawJetsValue,theweight * (trigSFWeightDown/trigSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_lepEff_elloose_up",treevars,mvaValue,mvawJetsValue,theweight * (elelooseSFWeightUp/elelooseSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_lepEff_elloose_down",treevars,mvaValue,mvawJetsValue,theweight * (elelooseSFWeightDown/elelooseSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_lepEff_eltight_up",treevars,mvaValue,mvawJetsValue,theweight * (eletightSFWeightUp/eletightSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_lepEff_eltight_down",treevars,mvaValue,mvawJetsValue,theweight * (eletightSFWeightDown/eletightSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_lepEff_muloose_up",treevars,mvaValue,mvawJetsValue,theweight * (mulooseSFWeightUp/mulooseSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_lepEff_muloose_down",treevars,mvaValue,mvawJetsValue,theweight * (mulooseSFWeightDown/mulooseSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_lepEff_mutight_up",treevars,mvaValue,mvawJetsValue,theweight * (mutightSFWeightUp/mutightSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_lepEff_mutight_down",treevars,mvaValue,mvawJetsValue,theweight * (mutightSFWeightDown/mutightSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_HFStats1_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs1Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_HFStats1_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs1Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_HFStats2_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs2Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_HFStats2_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs2Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_LFStats1_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs1Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_LFStats1_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs1Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_LFStats2_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs2Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_LFStats2_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs2Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_HFStats1_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs1Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_HFStats1_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs1Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_HFStats2_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs2Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_HFStats2_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs2Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_LFStats1_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs1Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_LFStats1_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs1Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_LFStats2_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs2Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_LFStats2_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs2Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl18_btag_HFStats1_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs1Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl18_btag_HFStats1_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs1Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl18_btag_HFStats2_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs2Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl18_btag_HFStats2_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs2Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl18_btag_LFStats1_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs1Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl18_btag_LFStats1_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs1Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl18_btag_LFStats2_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs2Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl18_btag_LFStats2_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs2Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_btag_cErr1_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightcferr1Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_btag_cErr1_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightcferr1Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_btag_cErr2_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightcferr2Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_btag_cErr2_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightcferr2Down/bWeight),met,mtw,theChannel);
        //fillHists(sampleName+"_bWeight_jes_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightjerUp/bWeight),met,mtw,theChannel);
        //fillHists(sampleName+"_bWeight_jes_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightjerDown/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_btag_LF_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfUp/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_btag_LF_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfDown/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_btag_HF_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfUp/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_btag_HF_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfDown/bWeight),met,mtw,theChannel);
        if (theTree->GetListOfBranches()->FindObject("EVENT_rWeights") && (sampleName.Contains("ttH") || sampleName.Contains("THQ") || sampleName.Contains("THW"))){
            for (auto& IDs : _IDOfReWeight){
                //std::cout<< " fill syst "<< IDs.first <<std::endl;
                if(EVENT_rWeights->size()>= IDs.second && EVENT_rWeights->size()>=12){
                    float rWeight = EVENT_rWeights->at(IDs.second-1)/EVENT_rWeights->at(11);
                    fillHists(sampleName+"_"+IDs.first,treevars,mvaValue,mvawJetsValue,theweight * rWeight,met,mtw,theChannel);
                }
            }
        }
      }
    }else if(sampleName.Contains("Flips")){
      fillHists(sampleName+"_CMS_ttHl_QF_up",treevars,mvaValue,mvawJetsValue,theweight * (ChargeMisUp/ChargeMis),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_QF_down",treevars,mvaValue,mvawJetsValue,theweight * (ChargeMisDown/ChargeMis),met,mtw,theChannel);
    }else if(sampleName.Contains("Fakes")){
      /*
      std::tie(FakeRate_Clos_e_shape_up, FakeRate_Clos_e_shape_down, FakeRate_Clos_m_shape_up, FakeRate_Clos_m_shape_down)=calculateClosSyst(Dilepton_flav , FakeRate_Clos_e_shape_ee_up, FakeRate_Clos_e_shape_ee_down, FakeRate_Clos_e_shape_em_up, FakeRate_Clos_e_shape_em_down, FakeRate_Clos_m_shape_mm_up, FakeRate_Clos_m_shape_mm_down, FakeRate_Clos_m_shape_em_up, FakeRate_Clos_m_shape_em_down);
      calculateClosNormSyst(Dilepton_flav, nbJet, FakeRate_Clos_e_norm_up, FakeRate_Clos_e_norm_down, FakeRate_Clos_e_bt_norm_up, FakeRate_Clos_e_bt_norm_down, FakeRate_Clos_m_norm_up, FakeRate_Clos_m_norm_down, FakeRate_Clos_m_bt_norm_up, FakeRate_Clos_m_bt_norm_down);
      fillHists(sampleName+"_CMS_ttHl_Clos_e_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_norm_up/FakeRate_Clos_e_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_Clos_e_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_norm_down/FakeRate_Clos_e_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_Clos_m_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_norm_up/FakeRate_Clos_m_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_Clos_m_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_norm_down/FakeRate_Clos_m_norm) ,met,mtw,theChannel);
      */
      fillHists(sampleName+"_CMS_ttHl_Clos_e_shape_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_shape_up/FakeRateWeight) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_Clos_e_shape_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_shape_down/FakeRateWeight) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_Clos_m_shape_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_shape_up/FakeRateWeight) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_Clos_m_shape_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_shape_down/FakeRateWeight) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRm_norm_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_normUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRm_norm_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_normDown/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRm_pt_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_ptUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRm_pt_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_ptDown/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRm_be_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_beUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRm_be_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_beDown/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRe_norm_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_normUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRe_norm_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_normDown/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRe_pt_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_ptUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRe_pt_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_ptDown/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRe_be_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_beUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl_FRe_be_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_beDown/FakeRateWeight),met,mtw,theChannel);
    }
   }else{
    std::cout<< sampleName<< " :  EventWeight is 0 , please Check !!! "<<std::endl; 
   }
  }
  }
} 

void mvaTool::createHists(TString sampleName){

  for (unsigned int region = 0; region < regionNames.size(); region++){


    std::vector<TH1F*> histovect;
    std::vector<TH1F*> bdtVect;


    //Make a histogram per variable
    for (unsigned int i = 0; i<varList.size(); i++){
      int nbins = 1;
      double xmin = -1000;
      double xmax = 1000;
    
      if(varList[i]== "Hj_tagger_resTop") {nbins= 20; xmin= -1.01; xmax= 1.01;};
      if(varList[i]== "Hj_tagger_hadTop") {nbins= 10; xmin= 0.; xmax= 1.01;};
      if(varList[i]== "Hj_tagger") {nbins= 10; xmin= 0.; xmax= 1.0;};
      if(varList[i]== "hadTop_BDT") {nbins= 10; xmin= 0.; xmax= 1.0;};
      if(varList[i]== "Dilep_mtWmin") {nbins= 10; xmin= 0; xmax= 200;};
      if(varList[i]== "mT_lep1") {nbins= 10; xmin= 0; xmax= 200;};
      if(varList[i]== "mT_lep2") {nbins= 10; xmin= 0; xmax= 200;};
      if(varList[i]== "TrueInteractions") {nbins= 100; xmin= -0.5; xmax= 99.5;};
      if(varList[i]== "nBestVTX") {nbins= 100; xmin= -0.5; xmax= 99.5;};
      if(varList[i]== "leadLep_corrpt") {nbins= 10; xmin= 0; xmax= 200;};
      if(varList[i]== "secondLep_corrpt") {nbins= 10; xmin= 0; xmax= 100;};
      if(varList[i]== "massll") {nbins= 10; xmin= 0; xmax= 400;};
      if(varList[i]== "Sum2lCharge") {nbins= 5; xmin= -2.5; xmax= 2.5;};
      if(varList[i]== "n_presel_jet") {nbins= 4; xmin= 3.5; xmax= 7.5;};
      if(varList[i]== "nBJetLoose") {nbins= 6; xmin= -0.5; xmax= 5.5;};
      if(varList[i]== "nBJetMedium") {nbins= 6; xmin= -0.5; xmax= 5.5;};
      if(varList[i]== "MHT") {nbins= 10; xmin= 0; xmax= 400;};
      if(varList[i]== "PFMET") {nbins= 50; xmin= 0; xmax= 500;};
      if(varList[i]== "metLD") {nbins= 20; xmin= 0; xmax= 200;};
      if(varList[i]== "Dilep_bestMVA") {nbins= 8; xmin= 0.6; xmax= 1;};
      if(varList[i]== "Dilep_worseMVA") {nbins= 8; xmin= 0.6; xmax= 1;};
      if(varList[i]== "Dilep_pdgId") {nbins= 5; xmin= -0.5; xmax= 4.5;};
      if(varList[i]== "Dilep_htllv") {nbins= 10; xmin= 0; xmax= 600;};
      if(varList[i]== "Dilep_nTight") {nbins= 3; xmin= -0.5; xmax= 2.5;};
      if(varList[i]== "HighestJetCSV") {nbins= 15; xmin= 0; xmax= 1;};
      if(varList[i]== "leadJetCSV") {nbins= 15; xmin= 0; xmax= 1;};
      if(varList[i]== "secondJetCSV") {nbins= 15; xmin= 0; xmax= 1;};
      if(varList[i]== "thirdJetCSV") {nbins= 15; xmin= 0; xmax= 1;};
      if(varList[i]== "fourthJetCSV") {nbins= 15; xmin= 0; xmax= 1;};
      if(varList[i]== "HtJet") {nbins= 10; xmin= 0; xmax= 1000;};
      if(varList[i]== "ttbarBDT_2lss") {nbins= 10; xmin= -1; xmax= 1;};
      if(varList[i]== "ttvBDT_2lss") {nbins= 10; xmin= -1; xmax= 1;};
      if(varList[i]== "Mt_metleadlep") {nbins= 10; xmin= 0; xmax= 400;};
      if(varList[i]== "maxeta") {nbins= 10; xmin= 0; xmax= 2.5;};
      if(varList[i]== "leadLep_jetdr") {nbins= 10; xmin= 0; xmax= 4;};
      if(varList[i]== "secondLep_jetdr") {nbins= 10; xmin= 0; xmax= 4;};
      if(varList[i]== "minMllAFOS") {nbins= 10; xmin= 0; xmax= 300;};
      if(varList[i]== "minMllAFAS") {nbins= 10; xmin= 0; xmax= 300;};
      if(varList[i]== "minMllSFOS") {nbins= 10; xmin= 0; xmax= 300;};
      if(varList[i]== "nLepFO") {nbins= 6; xmin= -0.5; xmax= 5.5;};
      if(varList[i]== "nLepTight") {nbins= 6; xmin= -0.5; xmax= 5.5;};
      if(varList[i]== "n_presel_ele") {nbins= 6; xmin= -0.5; xmax= 5.5;};
      if(varList[i]== "n_presel_mu") {nbins= 6; xmin= -0.5; xmax= 5.5;};
      if(varList[i]== "puWeight") {nbins= 30; xmin= 0.6; xmax= 1.4;};
      if(varList[i]== "bWeight") {nbins= 30; xmin= 0.6; xmax= 1.4;};
      if(varList[i]== "TriggerSF") {nbins= 30; xmin= 0.88; xmax= 1.12;};
      if(varList[i]== "lepSF") {nbins= 30; xmin= 0.6; xmax= 1.4;};
      if(varList[i]== "leadLep_BDT") {nbins= 10; xmin= -1; xmax= 1;};
      if(varList[i]== "secondLep_BDT") {nbins= 10; xmin= -1; xmax= 1;};
      if(varList[i]== "mbb") {nbins= 50; xmin= 0; xmax= 500;};
      if(varList[i]== "mbb_loose") {nbins= 50; xmin= 0; xmax= 500;};
      if(varList[i]== "avg_dr_jet") {nbins= 50; xmin= 0.; xmax= 10.;};
      if(varList[i]== "dr_leps") {nbins= 10; xmin= 0.; xmax= 5;};
      if(varList[i]== "mvaOutput_2lss_ttV") {nbins= 20; xmin= -1; xmax= 1;};
      if(varList[i]== "mvaOutput_2lss_ttbar") {nbins= 20; xmin= -1; xmax= 1;};
      if(varList[i]== "resTop_BDT") {nbins= 20; xmin= -1; xmax= 1;};
      if(varList[i]== "massL") {nbins= 20; xmin= 0; xmax= 400;};
      if(varList[i]== "jet1_pt") {nbins= 20; xmin= 0; xmax= 800;};
      if(varList[i]== "jet2_pt") {nbins= 20; xmin= 0; xmax= 600;};
      if(varList[i]== "jet3_pt") {nbins= 20; xmin= 0; xmax= 400;};
      if(varList[i]== "jet4_pt") {nbins= 20; xmin= 0; xmax= 200;};
      if(varList[i]== "jet1_eta") {nbins= 20; xmin= -4; xmax= 4;};
      if(varList[i]== "jet2_eta") {nbins= 20; xmin= -4; xmax= 4;};
      if(varList[i]== "jet3_eta") {nbins= 20; xmin= -4; xmax= 4;};
      if(varList[i]== "jet4_eta") {nbins= 20; xmin= -4; xmax= 4;};
      if(varList[i]== "lep1_conePt") {nbins= 20; xmin= 0; xmax= 200;};
      if(varList[i]== "lep2_conePt") {nbins= 20; xmin= 0; xmax= 100;};
      if(varList[i]== "lep1_eta") {nbins= 20; xmin= -4; xmax= 4;};
      if(varList[i]== "lep2_eta") {nbins= 20; xmin= -4; xmax= 4;};
      if(varList[i]== "Bin2l") {nbins= 11; xmin= 0.5; xmax= 11.5;};
      if(varList[i]== "DNN_maxval") {nbins= 20; xmin= 0; xmax= 1;};
      if(varList[i]== "DNN_maxval_option2") {nbins= 20; xmin= 0; xmax= 1;};
      if(varList[i]== "DNN_maxval_option3") {nbins= 20; xmin= 0; xmax= 1;};
      if(varList[i]== "DNNCat_2DBin_GT5") {nbins= 50; xmin= 0.5; xmax= 50.5;};
      if(varList[i]== "DNNCat_2DBin_GT10") {nbins= 50; xmin= 0.5; xmax= 50.5;};
      if(varList[i]== "DNNCat_2DBin_GT15") {nbins= 50; xmin= 0.5; xmax= 50.5;};
      if(varList[i]== "DNNCat_2DBin_GT20") {nbins= 50; xmin= 0.5; xmax= 50.5;};
      if(varList[i]== "DNNSubCat2_2DBin_GT5") {nbins= 30; xmin= 0.5; xmax= 30.5;};
      if(varList[i]== "DNNSubCat2_2DBin_GT10") {nbins= 30; xmin= 0.5; xmax= 30.5;};
      if(varList[i]== "DNNSubCat2_2DBin_GT15") {nbins= 30; xmin= 0.5; xmax= 30.5;};
      if(varList[i]== "DNNSubCat2_2DBin_GT20") {nbins= 30; xmin= 0.5; xmax= 30.5;};
      TString str_bin = "";
      if(varList[i].Contains("_nBin")){
        string varname = varList[i].Data();
        regex pattern("(.*_nBin)([0-9]+)");
        smatch result;
        regex_match(varname, result, pattern);
        str_bin = result.str(2);
        int n  = stoi(result.str(2));
        nbins = n;
        xmin = 0.5;
        xmax = xmin + nbins;
      }
      if(varList[i].Contains("_BIN") && varList[i].Contains("DNN")){
          int n = _DNNBinMap[ChannelNameMap[_channel]];
          nbins = n;
          xmin = 0.5;
          xmax = xmin + nbins;
      }
      TString histoName = subCat2l+"_"+varList[i]+"_"+ChannelNameMap[_channel];
      TH1F* h_sig = (TH1F*) theBinFile->Get(histoName+"_Sig");
      TString map_postfix = "NULL";
      if(varList[i].Contains("GT5"))map_postfix="GT5";
      if(varList[i].Contains("GT10"))map_postfix="GT10";
      if(varList[i].Contains("GT15"))map_postfix="GT15";
      if(varList[i].Contains("GT20"))map_postfix="GT20";
      TString MapName = ChannelNameMap[_channel] + "_Map_"+map_postfix;
      TH2F* h_map = (TH2F*) the2DBinFile->Get(MapName);
      if(BinDir.Contains("Regular")){
        if(h_sig==0){
            TH1F* histo = new TH1F((varList[i] + "_" + sampleName).Data(), (varList[i] + "_" + sampleName).Data(),nbins,xmin,xmax);
            histo->Sumw2();
            histovect.push_back(histo);
        }else{
            TH1F* h_bkg = (TH1F*) theBinFile->Get(histoName+"_Bkg");
            nbins = 2 * floor((h_sig->Integral() + h_bkg->Integral())/5.);
            std::cout<< " rebin the regular bin to nbins "<< nbins << std::endl;
            TH1F* histo = new TH1F((varList[i] + "_" + sampleName).Data(), (varList[i] + "_" + sampleName).Data(),nbins,xmin,xmax);
            histo->Sumw2();
            histovect.push_back(histo);
        }
      }else if(h_sig==0){
        if(h_map==0){
            TString flag = subCat2l;
            flag.ReplaceAll("option1","");
            if(flag.Contains("DNN") && varList[i].Contains("nBin")){
                TH1F* histo = new TH1F((flag+"nBin"+str_bin + "_" + sampleName).Data(), (flag+"nBin"+str_bin+ "_" + sampleName).Data(),nbins,xmin,xmax);
                histo->Sumw2();
                histovect.push_back(histo);
            }else{
                TH1F* histo = new TH1F((varList[i] + "_" + sampleName).Data(), (varList[i] + "_" + sampleName).Data(),nbins,xmin,xmax);
                histo->Sumw2();
                histovect.push_back(histo);
            }
        }else{
            xmax = h_map->GetMaximum() + 0.5;
            xmin = h_map->GetMinimum() - 0.5;
            nbins = xmax - xmin;
            TH1F* histo = new TH1F((varList[i] + "_" + sampleName).Data(), (varList[i] + "_" + sampleName).Data(),nbins,xmin,xmax);
            histo->Sumw2();
            histovect.push_back(histo);
        }
      }else{
        std::vector<double> bins;
        bins.clear();
        bins=getBins(theBinFile, histoName, _nPerBin , 0.1, xmin, xmax);
        if(bins.size()<=1){
            TH1F* histo = new TH1F((varList[i] + "_" + sampleName).Data(), (varList[i] + "_" + sampleName).Data(),1,xmin,xmax);
            histo->Sumw2();
            histovect.push_back(histo);
        }else{
            nbins = bins.size() - 1;
            const int binEdge = bins.size();
            double *binning = new double[binEdge];
            for(int i=0; i<bins.size(); i++){
                binning[i]=bins.at(i);
                //std::cout << " print the binEdges " << bins.at(i)<<std::endl;
            }
            // set first and last bin
            binning[0]=xmin;
            binning[binEdge-1]=xmax;
            TH1F* histo = new TH1F((varList[i] + "_" + sampleName).Data(), (varList[i] + "_" + sampleName).Data(),nbins,binning);
            histo->Sumw2();
            histovect.push_back(histo);
            delete [] binning;
        }
      }
      std::cout<<" var "<<varList[i] << " nbin " << nbins <<  " xmin " << xmin << " xmax " << xmax << std::endl;
    }
    //Add in some plots for met and mtw for control/fitting
    
    /*
    TH1F* histomtw = new TH1F(("mTW_" + sampleName).Data(), ("mTW_" + sampleName).Data(),20,0.,200.);
    histomtw->Sumw2();
    histovect.push_back(histomtw);
    TH1F* histomet = new TH1F(("met_" + sampleName).Data(), ("met_" + sampleName).Data(),20,0.,200.);
    histomet->Sumw2();
    histovect.push_back(histomet);
    for (int nBins = 10; nBins <= 100; nBins+=10){
      TH1F* histo = new TH1F(("MVA_ttbar_bin"+std::to_string(nBins)+"_"+sampleName).Data(),("MVA_ttbar_bin"+std::to_string(nBins)+"_"+sampleName).Data(),nBins,-0.8,0.8);
      histo->Sumw2();
      bdtVect.push_back(histo);
    }
    int nBins = 1000;
    TH1F* histo = new TH1F(("MVA_ttbar_bin"+std::to_string(nBins)+"_"+sampleName).Data(),("MVA_ttbar_bin"+std::to_string(nBins)+"_"+sampleName).Data(),nBins,-0.8,0.8);
    histo->Sumw2();
    bdtVect.push_back(histo);
    TH1F* histo2 = new TH1F(("MVA_wJets_"+sampleName).Data(),("MVA_wJets_"+sampleName).Data(),20,-0.3,0.3);
    histo2->Sumw2();
    histovect.push_back(histo2);

    TH2F* bdt2D = new TH2F(("MVA_2D_"+sampleName).Data(),("MVA_2D_"+sampleName).Data(),20,-0.8,0.8,20,-0.3,0.3);
    bdt2D->Sumw2();
    the2DHistoMap[sampleName].push_back(bdt2D);

    bdtHistoMap[sampleName].push_back(bdtVect);
    */
    theHistoMap[sampleName].push_back(histovect);
  }
  std::cout << "hist maps are this long: " << the2DHistoMap[sampleName].size() << " " << theHistoMap[sampleName].size() << " " << bdtHistoMap[sampleName].size() << std::endl;
}

void mvaTool::fillHists(TString sampleName, float* treevars, double mvaValue, double mvawJetsValue, double theweight, float met, float mtw, int theChannel){
//void mvaTool::fillHists(TString sampleName, int* treevars, double mvaValue, double mvawJetsValue, double theweight, float met, float mtw, int theChannel){

  //std::cout << "hist maps are this long: " << the2DHistoMap[sampleName].size() << " " << theHistoMap[sampleName].size() << " " << bdtHistoMap[sampleName].size() << std::endl;
  std::vector<std::vector<TH1F*> > histovect = theHistoMap[sampleName];
  //std::vector<std::vector<TH1F*> > bdtVector = bdtHistoMap[sampleName];
   
  //std::cout << "histovect are this long: " << histovect.size() << std::endl; 
  for (unsigned int i=0; i < varList.size(); i++){
      //std::cout<<" fill the histovect["<<theChannel<<"]["<<i<<"]"<<std::endl;
      //std::cout<< "Fill variable : " << varList[i] << std::endl;
      int binN = histovect[theChannel][i]->GetNbinsX();
      float minValue = histovect[theChannel][i]->GetBinLowEdge(1);
      float maxValue = histovect[theChannel][i]->GetBinLowEdge(binN+1);
      float fillValue = -999.;
      if(treevars[i] < minValue){
        //std::cout<<" taking care of underflow "<<std::endl;
        fillValue = minValue + 0.0001;
      }else if(treevars[i] > maxValue){
        //std::cout<<" taking care of overflow "<<std::endl;
        fillValue = maxValue - 0.0001;
      }else{
        //std::cout<<" fill value "<<std::endl;
        fillValue = treevars[i];
      }
      histovect[theChannel][i]->Fill(fillValue,theweight);
  }
  /*
  for (unsigned int j = 0; j < bdtVector[theChannel].size(); j++) bdtVector[theChannel][j]->Fill(mvaValue,theweight);
   
  histovect[theChannel][histovect[theChannel].size() - 3]->Fill(mtw,theweight);
  histovect[theChannel][histovect[theChannel].size() - 2]->Fill(met,theweight);

  if (histovect[theChannel].size() > 1){
    //    histovect[histovect.size()-2]->Fill(mvaValue,theweight);
     histovect[theChannel][histovect[theChannel].size()-1]->Fill(mvawJetsValue,theweight);
  }
  the2DHistoMap[sampleName][theChannel]->Fill(mvaValue,mvawJetsValue,theweight);
  */

}

void mvaTool::saveHists(std::vector<TFile*> outFile){
  for (unsigned int i = 0; i < regionNames.size(); i++){
    outFile[i]->cd();
    for (auto histoMapElement: theHistoMap){
      for (auto hist: (histoMapElement.second)[i]) hist->Write();
    }
    /*
    for (auto histoMapElement: bdtHistoMap){
      for (auto hist: (histoMapElement.second)[i]) hist->Write();
    }
    
    for (auto hist2D: the2DHistoMap){
      (hist2D.second)[i]->Write();
    }
    */
  }
}

void mvaTool::setbTagVars(TChain * theTree){
  std::cout << "[setbTagVars] Entered setbTagVars" << std::endl;
  //std::vector<TString> bTagSystNames = {"jes","hfstats1","lf","hfstats2","cferr1","hf"};
  std::vector<TString> bTagSystNames = {"jes","lf","lfstats1","lfstats2","hf","hfstats1","hfstats2","cferr1","cferr2"};
  std::vector<TString> upDown = {"up","down"};
  bTagSysts.push_back(0.);
  std::cout << "[setbTagVars] Assigned central variable " << std::endl;
  theTree->SetBranchAddress( "bWeight_central", &(bTagSysts[0]) );
  std::cout << "[setbTagVars] Assigned central variable to tree " << std::endl;
  int i = 1;
  for (auto bName: bTagSystNames){
    std::cout << "[setbTageVars] Booking " << bName << " variable: " << std::endl;
    for (auto ud: upDown){
      bTagSysts.push_back(0.);
      std::cout << ("     [setbTageVars] bWeight_"+ud+"_"+bName).Data() << std::endl;
      theTree->SetBranchAddress( ("bWeight_"+ud+"_"+bName).Data(), &(bTagSysts[i]));
      i++;
    }
  }
}

std::tuple<float,float> mvaTool::calculatebTagSyst(float bCentral, std::vector<float> bWeightsSyst){
  float systUp = 0., systDown = 0.;
  for (unsigned int i = 1; i < bWeightsSyst.size(); i++){
      if (i%2 == 0){//Down systs
	systDown += pow((bWeightsSyst[i]/bCentral)-1,2);
	//	std::cout << (bWeightsSyst[i]/bCentral)-1 << ",";
      }
      else{
	systUp += pow((bWeightsSyst[i]/bCentral)-1,2);
	//std::cout << (bWeightsSyst[i]/bCentral)-1 << ",";
      }
    }
  //  std::cout << std::endl;
  return std::make_tuple(1+sqrt(systUp),1-sqrt(systDown));
}

/*std::tuple<float,float> mvaTool::calculateMistagSyst(float bCentral, std::vector<float> bWeightsSyst){
  float systUp = 0., systDown = 0.;
  for (unsigned int i = 1; i < bWeightsSyst.size(); i++){
      if (i%2 == 0){//Down systs
	systDown += pow((bWeightsSyst[i]/bCentral)-1,2);
      }
      else{
	systUp += pow((bWeightsSyst[i]/bCentral)-1,2);
      }
    }
  return std::make_tuple(1+sqrt(systUp),1-sqrt(systDown));
  }*/
  
void mvaTool::makeStatVariationHists(TString sampleName, std::vector<TFile *> outputFile){
  for (unsigned int i = 0; i < regionNames.size(); i++){
    TH1F * theDefaultMVA = theHistoMap[sampleName][i].back(); //We only need to do this to nominal.
    outputFile[i]->cd();
    std::ostringstream histNameStream;
    std::string histName;             
    
    for (int i = 1; i <= theDefaultMVA->GetXaxis()->GetNbins();i++){
      histNameStream.str("");
      histNameStream << "MVA_" << sampleName << "_statbin"<<i<<"_up";
      histName = histNameStream.str();
      TH1F* tempMVAUp = (TH1F*)theDefaultMVA->Clone(histName.c_str());
      histNameStream.str("");
      histNameStream << "MVA_" << sampleName << "_statbin"<<i<<"_down";
      histName = histNameStream.str();
      TH1F* tempMVADown = (TH1F*)theDefaultMVA->Clone(histName.c_str());
      float binToChange = theDefaultMVA->GetBinContent(i);
      //This is the bit I'm not sure of, but can edit later with any luck.
      float uncert = sqrt(binToChange);
      tempMVAUp->SetBinContent(i,binToChange+uncert);
      tempMVADown->SetBinContent(i,binToChange-uncert);
      tempMVAUp->Write();
      tempMVADown->Write();
    }
  }
}

std::tuple<float,float,float,float> mvaTool::calculateClosSyst(float Dilep_flav ,float e_shape_ee_Up, float e_shape_ee_Down, float e_shape_em_Up, float e_shape_em_Down, float m_shape_mm_Up, float m_shape_mm_Down, float m_shape_em_Up, float m_shape_em_Down){
  float FakeRate_Clos_m_shape_up(1.), FakeRate_Clos_m_shape_down(1.);
  float FakeRate_Clos_e_shape_up(1.), FakeRate_Clos_e_shape_down(1.);
  if(fabs(Dilep_flav-3)<0.001){// ee category
    FakeRate_Clos_e_shape_up = e_shape_ee_Up;
    FakeRate_Clos_e_shape_down = e_shape_ee_Down;
  }else if(fabs(Dilep_flav-2)<0.001){// em category
    FakeRate_Clos_e_shape_up = e_shape_em_Up;
    FakeRate_Clos_e_shape_down = e_shape_em_Down;
    FakeRate_Clos_m_shape_up = m_shape_em_Up;
    FakeRate_Clos_m_shape_down = m_shape_em_Down;
  }else if(fabs(Dilep_flav-1)<0.001){// mm category
    FakeRate_Clos_m_shape_up = m_shape_mm_Up;
    FakeRate_Clos_m_shape_down = m_shape_mm_Down;
  }else{
    std::cout << " Error in calculateClosSyst , Dilep_flav should be 1,2 or 3 "<< std::endl;
  }
  return std::make_tuple(FakeRate_Clos_e_shape_up, FakeRate_Clos_e_shape_down, FakeRate_Clos_m_shape_up, FakeRate_Clos_m_shape_down);
};
void mvaTool::calculateClosNormSyst(float Dilep_flav, int nbMedium,float& e_norm_up, float& e_norm_down, float& e_bt_norm_up, float& e_bt_norm_down, float& m_norm_up, float& m_norm_down, float& m_bt_norm_up, float& m_bt_norm_down){
  if(fabs(Dilep_flav-3)<0.001){// ee category
      e_bt_norm_up = 1.;
      e_norm_up = 1.2;
  }else if(fabs(Dilep_flav-2)<0.001){// em category
      if(nbMedium>=2){//bt
        e_bt_norm_up = 1.1;
        m_bt_norm_up = 1.15;
        e_norm_up = 1.1;
        m_norm_up = 1.1;
      }else if(nbMedium>=0){//bl
        e_bt_norm_up = 1.;
        m_bt_norm_up = 1.;
        e_norm_up = 1.1;
        m_norm_up = 1.1;
      }else{
            std::cout << " Error in calculateClosNormSyst , bMediumJet is not read "<< std::endl;
      }
  }else if(fabs(Dilep_flav-1)<0.001){// mm category
      if(nbMedium>=2){//bt
        m_bt_norm_up = 1.3;
        m_norm_up = 1.2;
      }else if(nbMedium>=0){//bl
        m_bt_norm_up = 1.;
        m_norm_up = 1.2;
      }else{
            std::cout << " Error in calculateClosNormSyst , bMediumJet is not read "<< std::endl;
      }
  }else{
    std::cout << " Error in calculateClosNormSyst , Dilep_flav should be 1,2 or 3 "<< std::endl;
  }
  e_norm_down = 1./e_norm_up;
  e_bt_norm_down = 1./e_bt_norm_up;
  m_norm_down = 1./m_norm_up;
  m_bt_norm_down = 1./m_bt_norm_up;
}; 
void mvaTool::calculateLepTightEffSyst(float Dilep_flav, float& eltight_up, float& eltight_down, float& mutight_up, float& mutight_down){
  if(fabs(Dilep_flav-3)<0.001){// ee category
    eltight_up = 1.04;
  }else if(fabs(Dilep_flav-2)<0.001){// em category
    eltight_up = 1.02;
    mutight_up = 1.03;
  }else if(fabs(Dilep_flav-1)<0.001){// mm category
    mutight_up = 1.06;
  }else{
    std::cout << " Error in calculateLepTightEffSyst , Dilep_flav should be 1,2 or 3 "<< std::endl;
  }
  eltight_down = 1./eltight_up;
  mutight_down = 1./mutight_up;
};

std::vector<double> mvaTool::getBins(TFile* theBinFile, TString HistoName, float minN_total, float minN_sig, double& xmin, double& xmax){
    TH1F* h_sig = (TH1F*) theBinFile->Get(HistoName+"_Sig");
    TH1F* h_bkg =(TH1F*) theBinFile->Get(HistoName+"_Bkg");
    int binN = h_sig->GetNbinsX();
    xmin = h_sig->GetBinLowEdge(1);
    xmax = h_sig->GetBinLowEdge(binN+1);
    Float_t N_total = h_sig->Integral()+h_bkg->Integral();
    Int_t Bin = min(100, int(floor(N_total/minN_total)));
    std::cout << "Nsig, Ntot "<<h_sig->Integral()<<","<<h_bkg->Integral()<<" getBins: initial bin "<< Bin   << std::endl;
    float sig_yield = 0.;
    std::vector<double> bins;
    while(Bin>1 && sig_yield < minN_sig){
        double* XQ = new double[Bin];
        double* YQ = new double[Bin];
        double* nYQ = new double[Bin+1];
        for(int i=0; i<Bin; i++)XQ[i]=Float_t(i+1)/Bin;
        h_bkg->GetQuantiles(Bin, YQ, XQ);// now YQ contains the low bin edge
        //std::cout << " Bin Size " << Bin <<" sig_yield "<< sig_yield<<std::endl;
        for(int i=0; i<Bin; i++){
            nYQ[i+1]=YQ[i];//shift YQ
            //std::cout << " print the Quantiles " << YQ[i]<<std::endl;
        }
        // reBin h_sig
        TH1F* hnew;
        hnew = (TH1F*) h_sig->Rebin(Bin,"hnew", nYQ);
        sig_yield = hnew->GetMinimum();
        // fill vector
        bins.clear();
        for(int i=0; i <(Bin+1); i++)bins.push_back(nYQ[i]);
        Bin--;
        delete [] XQ;
        delete [] YQ;
        delete [] nYQ;
    }
    return bins;
};

std::tuple<float,float,float,float> mvaTool::get_muFmuR_factor(TString sampleName){
    /////////
    //  this function returns the factor that normalize the Renormalization/Factorization scale variations to the central values
    //  for example: 
    //  hist_nominal = 1   
    //  hist_muF2 = 1.01
    //  factor =  1/1.01
    //  return factor_muF2, factor_muF0p5, factor_muR2, factor_muR0p5
    //  all values here are calculated in advance
    /////////
    float factor_muF2(1.), factor_muF0p5(1.), factor_muR2(1.), factor_muR0p5(1.);
    if(_DataEra==2016){
        if(sampleName.Contains("TTH") || sampleName.Contains("ttH")){
            factor_muF0p5 = 66.78/67.12;
            factor_muF2 = 66.78/66.51;
            factor_muR0p5 = 66.78/65.94;
            factor_muR2 = 66.78/63.00;
        }else if(sampleName.Contains("THQ")){
            factor_muF0p5 = 1.36/1.50;
            factor_muF2 = 1.36/1.24;
            factor_muR0p5 = 1.36/1.55;
            factor_muR2 = 1.36/1.21;
        }else if(sampleName.Contains("THW")){
            factor_muF0p5 = 0.70/0.59;
            factor_muF2 = 0.70/0.75;
            factor_muR0p5 = 0.70/0.79;
            factor_muR2 = 0.70/0.62;
        }else if(sampleName=="TTW"){
            factor_muF0p5 = 199.95/204.82;
            factor_muF2 = 199.95/196.16;
            factor_muR0p5 = 199.95/218.42;
            factor_muR2 = 199.95/179.80;
        }else if(sampleName=="TTWW"){
            factor_muF0p5 = 4.49/4.92;
            factor_muF2 = 4.49/4.14;
            factor_muR0p5 = 4.49/5.44;
            factor_muR2 = 4.49/3.78;
        }else if(sampleName=="TTZ"){
            factor_muF0p5 = 67.20/70.56;
            factor_muF2 = 67.20/64.29;
            factor_muR0p5 = 67.20/77.13;
            factor_muR2 = 67.20/58.94;
        }
    }else if (_DataEra==2017){
        if(sampleName.Contains("TTH") || sampleName.Contains("ttH")){
            factor_muF0p5 = 78.66/81.68;
            factor_muF2 = 78.66/72.40;
            factor_muR0p5 = 78.66/79.79;
            factor_muR2 = 78.66/77.73;
        }else if(sampleName.Contains("THQ")){
            factor_muF0p5 = 4.81/5.31;
            factor_muF2 = 4.81/4.39;
            factor_muR0p5 = 4.81/5.48;
            factor_muR2 = 4.81/4.30;
        }else if(sampleName.Contains("THW")){
            factor_muF0p5 = 2.41/2.05;
            factor_muF2 = 2.41/2.61;
            factor_muR0p5 = 2.41/2.75;
            factor_muR2 = 2.41/2.15;
        }else if(sampleName=="TTW"){
            factor_muF0p5 = 240.70/265.91;
            factor_muF2 = 240.70/215.20;
            factor_muR0p5 = 240.70/245.58;
            factor_muR2 = 240.70/236.93;
        }else if(sampleName=="TTWW"){
            factor_muF0p5 = 5.28/5.77;
            factor_muF2 = 5.28/4.85;
            factor_muR0p5 = 5.28/6.32;
            factor_muR2 = 5.28/4.47;
        }else if(sampleName=="TTZ"){
            factor_muF0p5 = 83.63/90.41;
            factor_muF2 = 83.63/77.03;
            factor_muR0p5 = 83.63/92.23;
            factor_muR2 = 83.63/77.04;
        }
    }else if (_DataEra==2018){
        if(sampleName.Contains("TTH") || sampleName.Contains("ttH")){
            factor_muF0p5 = 112.32/116.37;
            factor_muF2 = 112.32/103.50;
            factor_muR0p5 = 112.32/112.77;
            factor_muR2 = 112.32/111.92;
        }else if(sampleName.Contains("THQ")){
            factor_muF0p5 = 7.07/7.81;
            factor_muF2 = 7.07/6.45;
            factor_muR0p5 = 7.07/8.06;
            factor_muR2 = 7.07/6.31;
        }else if(sampleName.Contains("THW")){
            factor_muF0p5 = 3.55/2.99;
            factor_muF2 = 3.55/3.85;
            factor_muR0p5 = 3.55/4.03;
            factor_muR2 = 3.55/3.17;
        }else if(sampleName=="TTW"){
            factor_muF0p5 = 349.33/385.36;
            factor_muF2 = 349.33/312.60;
            factor_muR0p5 = 349.33/356.89;
            factor_muR2 = 349.33/343.46;
        }else if(sampleName=="TTWW"){
            factor_muF0p5 = 7.87/8.62;
            factor_muF2 = 7.87/7.24;
            factor_muR0p5 = 7.87/9.44;
            factor_muR2 = 7.87/6.67;
        }else if(sampleName=="TTZ"){
            factor_muF0p5 = 124.92/135.23;
            factor_muF2 = 124.92/114.97;
            factor_muR0p5 = 124.92/137.41;
            factor_muR2 = 124.92/115.37;
        }
    }else{
        std::cout<< "_DataEra is " << _DataEra << " please check, the best I can do is to return 1 " << std::endl;
    }
  return std::make_tuple(factor_muF0p5, factor_muF2, factor_muR0p5, factor_muR2);
};
