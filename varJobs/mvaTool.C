#define mvaTool_cxx
#include "mvaTool.h"

mvaTool::mvaTool(TString regName, TString binDir, Int_t channel, TString Category, TString TreeName, std::map<Int_t, TString> channelNameMap){
  
  _channel = channel;
  subCat2l = Category;
  treeName = TreeName;
  ChannelNameMap = channelNameMap;
  BinDir = binDir;
  RegName = regName;
  theBinFile = new TFile((binDir+"/OptBin_"+regName+".root"));
  //  regionNames = {"3j1t","3j2t","2j1t","4j1t","4j2t"};
  regionNames = {""};
  //Start by initialising the list of variables we will base the MVA on

  
  baseName = "";

    varList.push_back("TrueInteractions");
    varList.push_back("nBestVTX");
    
    varList.push_back("mT_lep1");
    varList.push_back("mT_lep2");
    varList.push_back("Hj_tagger_resTop");
    varList.push_back("Hj_tagger_hadTop");
    varList.push_back("Dilep_mtWmin");

    varList.push_back("massll");
    varList.push_back("Sum2lCharge");
    varList.push_back("n_presel_jet");
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
    varList.push_back("mvaOutput_2lss_ttV");
    varList.push_back("mvaOutput_2lss_ttbar");
    varList.push_back("resTop_BDT");
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
    varList.push_back("nBJetMedium"); // please always load nBJetMedium
    varList.push_back("Bin2l");
    varList.push_back("DNN_maxval");
    varList.push_back("DNN_maxval_option2");
    //varList.push_back("DNN_maxval_option3");

  
  //At some point this should be filled out with the names of the systematics so that we can read those too
  systlist.push_back("");
  systlist.push_back("_PU_up");
  systlist.push_back("_PU_down");
  systlist.push_back("_CMS_ttHl17_trigger_up");
  systlist.push_back("_CMS_ttHl17_trigger_down");
  systlist.push_back("_CMS_ttHl16_lepEff_elloose_up");
  systlist.push_back("_CMS_ttHl16_lepEff_elloose_down");
  systlist.push_back("_CMS_ttHl16_lepEff_eltight_up");
  systlist.push_back("_CMS_ttHl16_lepEff_eltight_down");
  systlist.push_back("_CMS_ttHl16_lepEff_muloose_up");
  systlist.push_back("_CMS_ttHl16_lepEff_muloose_down");
  systlist.push_back("_CMS_ttHl16_lepEff_mutight_up");
  systlist.push_back("_CMS_ttHl16_lepEff_mutight_down");
  systlist.push_back("_CMS_ttHl17_btag_HFStats1_up"); 
  systlist.push_back("_CMS_ttHl17_btag_HFStats1_down"); 
  systlist.push_back("_CMS_ttHl17_btag_HFStats2_up"); 
  systlist.push_back("_CMS_ttHl17_btag_HFStats2_down"); 
  systlist.push_back("_CMS_ttHl17_btag_LFStats1_up"); 
  systlist.push_back("_CMS_ttHl17_btag_LFStats1_down"); 
  systlist.push_back("_CMS_ttHl17_btag_LFStats2_up"); 
  systlist.push_back("_CMS_ttHl17_btag_LFStats2_down"); 
  systlist.push_back("_CMS_ttHl16_btag_cErr1_up"); 
  systlist.push_back("_CMS_ttHl16_btag_cErr1_down"); 
  systlist.push_back("_CMS_ttHl16_btag_cErr2_up"); 
  systlist.push_back("_CMS_ttHl16_btag_cErr2_down"); 
  systlist.push_back("_bWeight_jes_up"); 
  systlist.push_back("_bWeight_jes_down"); 
  systlist.push_back("_CMS_ttHl16_btag_LF_up"); 
  systlist.push_back("_CMS_ttHl16_btag_LF_down"); 
  systlist.push_back("_CMS_ttHl16_btag_HF_up"); 
  systlist.push_back("_CMS_ttHl16_btag_HF_down"); 
  systlist.push_back("_CMS_ttHl16_FRm_norm_up");
  systlist.push_back("_CMS_ttHl16_FRm_norm_down");
  systlist.push_back("_CMS_ttHl16_FRm_pt_up");
  systlist.push_back("_CMS_ttHl16_FRm_pt_down");
  systlist.push_back("_CMS_ttHl16_FRm_be_up");
  systlist.push_back("_CMS_ttHl16_FRm_be_down");
  systlist.push_back("_CMS_ttHl17_Clos_m_shape_up");
  systlist.push_back("_CMS_ttHl17_Clos_m_shape_down");
  systlist.push_back("_CMS_ttHl17_Clos_m_norm_up");
  systlist.push_back("_CMS_ttHl17_Clos_m_norm_down");
  systlist.push_back("_CMS_ttHl17_Clos_m_bt_norm_up");
  systlist.push_back("_CMS_ttHl17_Clos_m_bt_norm_down");
  systlist.push_back("_CMS_ttHl16_FRe_norm_up");
  systlist.push_back("_CMS_ttHl16_FRe_norm_down");
  systlist.push_back("_CMS_ttHl16_FRe_pt_up");
  systlist.push_back("_CMS_ttHl16_FRe_pt_down");
  systlist.push_back("_CMS_ttHl16_FRe_be_up");
  systlist.push_back("_CMS_ttHl16_FRe_be_down");
  systlist.push_back("_CMS_ttHl17_Clos_e_shape_up");
  systlist.push_back("_CMS_ttHl17_Clos_e_shape_down");
  systlist.push_back("_CMS_ttHl17_Clos_e_norm_up");
  systlist.push_back("_CMS_ttHl17_Clos_e_norm_down");
  systlist.push_back("_CMS_ttHl17_Clos_e_bt_norm_up");
  systlist.push_back("_CMS_ttHl17_Clos_e_bt_norm_down");
  systlist.push_back("_ChargeMis_up");
  systlist.push_back("_ChargeMis_down");
  systlist.push_back("_CMS_ttHl_thu_shape_ttH_up");
  systlist.push_back("_CMS_ttHl_thu_shape_ttH_down");
  systlist.push_back("_CMS_ttHl_thu_shape_ttW_up");
  systlist.push_back("_CMS_ttHl_thu_shape_ttW_down");
  systlist.push_back("_CMS_ttHl_thu_shape_ttZ_up");
  systlist.push_back("_CMS_ttHl_thu_shape_ttZ_down");
  
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

  TString dirWithTrees = inDir+"/"+sampleName+"_"+inDir+".root";
  std::vector<TFile*> theoutputfiles;
  for (auto const regionName : regionNames){
    std::cout << "Createing file " << outDir+regionName+"/output_"+ChannelNameMap[_channel]+"_"+sampleName+".root" <<std::endl;
    TFile *theoutputfile = new TFile( (outDir+regionName+"/output_"+ChannelNameMap[_channel]+"_"+sampleName+".root").Data(), "RECREATE");
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
    if (!isData && sampleName =="FakeSub" && !(systlist[j].Contains("_FRm_") || systlist[j].Contains("_FRe_") || systlist[j].Contains("_Clos_m_") || systlist[j].Contains("_Clos_e_") || systlist[j] == "" || systlist[j].Contains("bWeight_jes")))continue;
    if (!isData && sampleName !="FakeSub" && (systlist[j].Contains("_FRm_") || systlist[j].Contains("_FRe_") || systlist[j].Contains("_Clos_m_") || systlist[j].Contains("_Clos_e_")))continue;
    if (isData && sampleName =="Flips" && !(systlist[j].Contains("ChargeMis") || systlist[j] ==""))continue;
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

  //Get the systematic weights here. We will then fill hists separately as a result of this.
  float puWeight=0., puWeightUp = 0., puWeightDown = 0.;
  float ChargeMis=0., ChargeMisUp = 0., ChargeMisDown = 0.;
  float lepSFWeight=0., elelooseSFWeight=0. , eletightSFWeight=1., mulooseSFWeight=0., mutightSFWeight=1.;
  float elelooseSFWeightUp = 0., elelooseSFWeightDown = 0., eletightSFWeightUp = 1., eletightSFWeightDown = 1., mulooseSFWeightUp = 0., mulooseSFWeightDown = 0., mutightSFWeightUp = 1., mutightSFWeightDown = 1.;

  double genWeight =0.;
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
    /*
    theTree->SetBranchAddress( "mutightSF_SysUp", &mutightSFWeightUp );
    theTree->SetBranchAddress( "mutightSF", &mutightSFWeight );
    theTree->SetBranchAddress( "mutightSF_SysDown", &mutightSFWeightDown );
    theTree->SetBranchAddress( "eletightSF_SysUp", &eletightSFWeightUp );
    theTree->SetBranchAddress( "eletightSF", &eletightSFWeight );
    theTree->SetBranchAddress( "eletightSF_SysDown", &eletightSFWeightDown );
    */
    theTree->SetBranchAddress( "TriggerSF", &trigSFWeight );
    theTree->SetBranchAddress( "TriggerSF_SysUp", &trigSFWeightUp );
    theTree->SetBranchAddress( "TriggerSF_SysDown", &trigSFWeightDown );
    
    theTree->SetBranchAddress( "EVENT_genWeight", &genWeight );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttH", &CMS_ttHl_thu_shape_ttH );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttH_SysUp", &CMS_ttHl_thu_shape_ttH_up );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttH_SysDown", &CMS_ttHl_thu_shape_ttH_down );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttW", &CMS_ttHl_thu_shape_ttW );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttW_SysUp", &CMS_ttHl_thu_shape_ttW_up );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttW_SysDown", &CMS_ttHl_thu_shape_ttW_down );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttZ", &CMS_ttHl_thu_shape_ttZ );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttZ_SysUp", &CMS_ttHl_thu_shape_ttZ_up );
    theTree->SetBranchAddress( "CMS_ttHl_thu_shape_ttZ_SysDown", &CMS_ttHl_thu_shape_ttZ_down );
    
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
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_e_shape_ee_SysUp", &FakeRate_Clos_e_shape_ee_up);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_e_shape_ee_SysDown", &FakeRate_Clos_e_shape_ee_down);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_e_shape_em_SysUp", &FakeRate_Clos_e_shape_em_up);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_e_shape_em_SysDown", &FakeRate_Clos_e_shape_em_down);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_m_shape_mm_SysUp", &FakeRate_Clos_m_shape_mm_up);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_m_shape_mm_SysDown", &FakeRate_Clos_m_shape_mm_down);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_m_shape_em_SysUp", &FakeRate_Clos_m_shape_em_up);
        theTree->SetBranchAddress( "CMS_ttHl17_Clos_m_shape_em_SysDown", &FakeRate_Clos_m_shape_em_down);
        std::cout << "[loopInSample] Finished assigning FakeRate Closure weights" << std::endl;
   
  
    //}
    
  
  //  std::vector<float> bTagSysts;
  //  setbTagVars(theTree);
  
  if (theTree ==0) cout << "No TTree found for " << sampleName << "!" << std::endl;

  std::tuple<float,float> bSysts (std::make_pair(1.,1.));
  std::tuple<float,float> mistagSysts (std::make_pair(1.,1.));

  //Loop over the events
  std::cout << theTree->GetEntries() << " events in loop for sample " << sampleName << std::endl; 
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

    fillHists(sampleName,treevars,mvaValue,mvawJetsValue,theweight,met,mtw,theChannel);
    
    //std::cout << " now fill the weight-based systematic histograms "<<std::endl; 
    //Now fill the weight-based systematic histograms
   if(theweight!=0){
    if (!isData){
      if(sampleName.Contains("FakeSub")){
        std::tie(FakeRate_Clos_e_shape_up, FakeRate_Clos_e_shape_down, FakeRate_Clos_m_shape_up, FakeRate_Clos_m_shape_down)=calculateClosSyst(Dilepton_flav , FakeRate_Clos_e_shape_ee_up, FakeRate_Clos_e_shape_ee_down, FakeRate_Clos_e_shape_em_up, FakeRate_Clos_e_shape_em_down, FakeRate_Clos_m_shape_mm_up, FakeRate_Clos_m_shape_mm_down, FakeRate_Clos_m_shape_em_up, FakeRate_Clos_m_shape_em_down);
        calculateClosNormSyst(Dilepton_flav, nbJet, FakeRate_Clos_e_norm_up, FakeRate_Clos_e_norm_down, FakeRate_Clos_e_bt_norm_up, FakeRate_Clos_e_bt_norm_down, FakeRate_Clos_m_norm_up, FakeRate_Clos_m_norm_down, FakeRate_Clos_m_bt_norm_up, FakeRate_Clos_m_bt_norm_down);
        fillHists(sampleName+"_CMS_ttHl17_Clos_e_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_norm_up/FakeRate_Clos_e_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_e_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_norm_down/FakeRate_Clos_e_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_e_bt_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_bt_norm_up/FakeRate_Clos_e_bt_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_e_bt_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_bt_norm_down/FakeRate_Clos_e_bt_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_e_shape_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_shape_up/FakeRate_Clos_e_shape) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_e_shape_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_shape_down/FakeRate_Clos_e_shape) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_m_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_norm_up/FakeRate_Clos_m_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_m_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_norm_down/FakeRate_Clos_m_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_m_bt_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_bt_norm_up/FakeRate_Clos_m_bt_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_m_bt_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_bt_norm_down/FakeRate_Clos_m_bt_norm) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_m_shape_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_shape_up/FakeRate_Clos_m_shape) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_Clos_m_shape_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_shape_down/FakeRate_Clos_m_shape) ,met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRm_norm_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_normUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRm_norm_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_normDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRm_pt_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_ptUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRm_pt_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_ptDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRm_be_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_beUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRm_be_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_beDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRe_norm_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_normUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRe_norm_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_normDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRe_pt_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_ptUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRe_pt_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_ptDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRe_be_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_beUp/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_FRe_be_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_beDown/FakeRateWeight),met,mtw,theChannel);
        fillHists(sampleName+"_bWeight_jes_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightjerUp/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_bWeight_jes_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightjerDown/bWeight),met,mtw,theChannel);
      }else{
        calculateLepTightEffSyst(Dilepton_flav,  eletightSFWeightUp,  eletightSFWeightDown,  mutightSFWeightUp,  mutightSFWeightDown);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttH_up",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttH_up/CMS_ttHl_thu_shape_ttH),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttH_down",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttH_down/CMS_ttHl_thu_shape_ttH),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttW_up",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttW_up/CMS_ttHl_thu_shape_ttW),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttW_down",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttW_down/CMS_ttHl_thu_shape_ttW),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttZ_up",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttZ_up/CMS_ttHl_thu_shape_ttZ),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl_thu_shape_ttZ_down",treevars,mvaValue,mvawJetsValue,theweight * (CMS_ttHl_thu_shape_ttZ_down/CMS_ttHl_thu_shape_ttZ),met,mtw,theChannel);
        fillHists(sampleName+"_PU_up",treevars,mvaValue,mvawJetsValue,theweight * (puWeightUp/puWeight),met,mtw,theChannel);
        fillHists(sampleName+"_PU_down",treevars,mvaValue,mvawJetsValue,theweight * (puWeightDown/puWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_trigger_up",treevars,mvaValue,mvawJetsValue,theweight * (trigSFWeightUp/trigSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_trigger_down",treevars,mvaValue,mvawJetsValue,theweight * (trigSFWeightDown/trigSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_lepEff_elloose_up",treevars,mvaValue,mvawJetsValue,theweight * (elelooseSFWeightUp/elelooseSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_lepEff_elloose_down",treevars,mvaValue,mvawJetsValue,theweight * (elelooseSFWeightDown/elelooseSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_lepEff_eltight_up",treevars,mvaValue,mvawJetsValue,theweight * (eletightSFWeightUp/eletightSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_lepEff_eltight_down",treevars,mvaValue,mvawJetsValue,theweight * (eletightSFWeightDown/eletightSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_lepEff_muloose_up",treevars,mvaValue,mvawJetsValue,theweight * (mulooseSFWeightUp/mulooseSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_lepEff_muloose_down",treevars,mvaValue,mvawJetsValue,theweight * (mulooseSFWeightDown/mulooseSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_lepEff_mutight_up",treevars,mvaValue,mvawJetsValue,theweight * (mutightSFWeightUp/mutightSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_lepEff_mutight_down",treevars,mvaValue,mvawJetsValue,theweight * (mutightSFWeightDown/mutightSFWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_HFStats1_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs1Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_HFStats1_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs1Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_HFStats2_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs2Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_HFStats2_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfs2Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_LFStats1_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs1Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_LFStats1_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs1Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_LFStats2_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs2Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl17_btag_LFStats2_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfs2Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_cErr1_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightcferr1Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_cErr1_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightcferr1Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_cErr2_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightcferr2Up/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_cErr2_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightcferr2Down/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_bWeight_jes_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightjerUp/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_bWeight_jes_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightjerDown/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_LF_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfUp/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_LF_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeightlfDown/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_HF_up",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfUp/bWeight),met,mtw,theChannel);
        fillHists(sampleName+"_CMS_ttHl16_btag_HF_down",treevars,mvaValue,mvawJetsValue,theweight * (bWeighthfDown/bWeight),met,mtw,theChannel);
      }
    }else if(sampleName.Contains("Flips")){
      fillHists(sampleName+"_ChargeMis_up",treevars,mvaValue,mvawJetsValue,theweight * (ChargeMisUp/ChargeMis),met,mtw,theChannel);
      fillHists(sampleName+"_ChargeMis_down",treevars,mvaValue,mvawJetsValue,theweight * (ChargeMisDown/ChargeMis),met,mtw,theChannel);
    }else if(sampleName.Contains("Fakes")){
      std::tie(FakeRate_Clos_e_shape_up, FakeRate_Clos_e_shape_down, FakeRate_Clos_m_shape_up, FakeRate_Clos_m_shape_down)=calculateClosSyst(Dilepton_flav , FakeRate_Clos_e_shape_ee_up, FakeRate_Clos_e_shape_ee_down, FakeRate_Clos_e_shape_em_up, FakeRate_Clos_e_shape_em_down, FakeRate_Clos_m_shape_mm_up, FakeRate_Clos_m_shape_mm_down, FakeRate_Clos_m_shape_em_up, FakeRate_Clos_m_shape_em_down);
      calculateClosNormSyst(Dilepton_flav, nbJet, FakeRate_Clos_e_norm_up, FakeRate_Clos_e_norm_down, FakeRate_Clos_e_bt_norm_up, FakeRate_Clos_e_bt_norm_down, FakeRate_Clos_m_norm_up, FakeRate_Clos_m_norm_down, FakeRate_Clos_m_bt_norm_up, FakeRate_Clos_m_bt_norm_down);
      fillHists(sampleName+"_CMS_ttHl17_Clos_e_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_norm_up/FakeRate_Clos_e_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_e_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_norm_down/FakeRate_Clos_e_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_e_bt_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_bt_norm_up/FakeRate_Clos_e_bt_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_e_bt_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_bt_norm_down/FakeRate_Clos_e_bt_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_e_shape_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_shape_up/FakeRate_Clos_e_shape) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_e_shape_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_e_shape_down/FakeRate_Clos_e_shape) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_m_shape_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_shape_up/FakeRate_Clos_m_shape) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_m_shape_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_shape_down/FakeRate_Clos_m_shape) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_m_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_norm_up/FakeRate_Clos_m_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_m_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_norm_down/FakeRate_Clos_m_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_m_bt_norm_up",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_bt_norm_up/FakeRate_Clos_m_bt_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl17_Clos_m_bt_norm_down",treevars,mvaValue,mvawJetsValue,theweight*(FakeRate_Clos_m_bt_norm_down/FakeRate_Clos_m_bt_norm) ,met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRm_norm_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_normUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRm_norm_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_normDown/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRm_pt_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_ptUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRm_pt_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_ptDown/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRm_be_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_beUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRm_be_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_m_beDown/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRe_norm_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_normUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRe_norm_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_normDown/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRe_pt_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_ptUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRe_pt_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_ptDown/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRe_be_up",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_beUp/FakeRateWeight),met,mtw,theChannel);
      fillHists(sampleName+"_CMS_ttHl16_FRe_be_down",treevars,mvaValue,mvawJetsValue,theweight * (FakeRateWeight_e_beDown/FakeRateWeight),met,mtw,theChannel);
    }
   }else{
    std::cout<< sampleName<< " :  EventWeight is 0 , please Check !!! "<<std::endl; 
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
      if(varList[i]== "Hj_tagger_hadTop") {nbins= 20; xmin= -1.01; xmax= 1.01;};
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
      
      TString histoName = subCat2l+"_"+varList[i]+"_"+ChannelNameMap[_channel];
      TH1F* h_sig = (TH1F*) theBinFile->Get(histoName+"_Sig");
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
        TH1F* histo = new TH1F((varList[i] + "_" + sampleName).Data(), (varList[i] + "_" + sampleName).Data(),nbins,xmin,xmax);
        histo->Sumw2();
        histovect.push_back(histo);
      }else{
        std::vector<double> bins;
        bins.clear();
        bins=getBins(theBinFile, histoName, 5 , 0.1, xmin, xmax);
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
    Int_t Bin = floor(N_total/minN_total);
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
