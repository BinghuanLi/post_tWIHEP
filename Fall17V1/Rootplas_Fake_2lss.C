// Input : 
// the output skim root file of tWIHEPFramework
// Function: 
// select datafake  events according to Regions/Postfix and save/reconstruct only interested branches
// same sign lepton : fabs(Sum2lCharge)==2 
// dilep are tight tight: Dilep_nTight <2 
//      Region cuts : 
//      SigRegion: n_presel_jets >=4
//      ttWctrl: n_presel_jets ==3
//      DiLepRegion: ""
// Output:
// rootplas for plotting and statistics study

#include "function.C"



void Rootplas_Fake_2lss(TString InputDir, TString OutputDir, TString FileName, TString Postfix){

    if(Postfix!="SigRegion" && Postfix!="ttWctrl" && Postfix!="DiLepRegion"){
        std::cout<< " ##################  ERROR ############ "<<std::endl;
        std::cout<< " Postfix must be SigRegion,ttWctrl or DiLepRegion, please pass a correct Postfix "<< std::endl;
        return;
    }
    TString Input = InputDir +"/"+ FileName + "Skim.root";
    TString Output = OutputDir  +"/"+FileName+ "_Fake2lss_"+Postfix+".root";
    std::cout <<" inpupt file is " << Input << std::endl;
    std::cout <<" outpupt file is " << Output << std::endl;
    TFile *oldfile = new TFile(Input);
    TTree *oldtree = (TTree*)oldfile->Get("TNT/BOOM");


    Long64_t nentries = oldtree->GetEntries(); 
    
    float nLooseJet=0;
    float nLightJet=0;
    float nBJetLoose=0;
    float nBJetMedium=0;
    double rtrueInteractions=0;
    int rnBestVtx=0;
    Long64_t nEvt = 0;
    Long64_t nEvent = 0;
   
    float lep1_pdgId(0.), lep2_pdgId(0.), lep3_pdgId(0.);
    float lep1_conept(0.), lep2_conept(0.);// lep3_conept(0.);
    float lep1_eta(0.), lep2_eta(0.), lep3_eta(0.);
    float lep1_phi(0.), lep2_phi(0.), lep3_phi(0.);
    float lep1_E(0.), lep2_E(0.), lep3_E(0.);
    float Sum2lCharge(0.), Dilep_nTight(0.), massL_SFOS(0.), Trilep_nTight(0.), Dilep_pdgId(0.), Sum3LCharge(0.);
    float xsec_rwgt(0.);
    float cpodd_rwgt(0.);
    float mvaOutput_2lss_ttV(0.), mvaOutput_2lss_ttbar(0.);
    
    std::vector<double>* Jet25_pt =0;
    std::vector<double>* Jet25_eta =0;
    std::vector<double>* Jet25_phi =0;
    std::vector<double>* Jet25_energy =0;
    std::vector<double>* Jet25_bDiscriminator =0;
   
    

    oldtree->SetBranchAddress("trueInteractions", &rtrueInteractions);
    oldtree->SetBranchAddress("nBestVtx", &rnBestVtx);
    oldtree->SetBranchAddress("n_presel_jet", &nLooseJet);
    oldtree->SetBranchAddress("nBJetLoose", &nBJetLoose);
    oldtree->SetBranchAddress("nBJetMedium", &nBJetMedium);
    oldtree->SetBranchAddress("nLightJet", &nLightJet);
    oldtree->SetBranchAddress("lep1_pdgId", &lep1_pdgId);
    oldtree->SetBranchAddress("lep2_pdgId", &lep2_pdgId);
    oldtree->SetBranchAddress("lep3_pdgId", &lep3_pdgId);
    oldtree->SetBranchAddress("leadLep_corrpt", &lep1_conept);
    oldtree->SetBranchAddress("secondLep_corrpt", &lep2_conept);
    oldtree->SetBranchAddress("lep1_eta", &lep1_eta);
    oldtree->SetBranchAddress("lep2_eta", &lep2_eta);
    oldtree->SetBranchAddress("lep3_eta", &lep3_eta);
    oldtree->SetBranchAddress("lep1_phi", &lep1_phi);
    oldtree->SetBranchAddress("lep2_phi", &lep2_phi);
    oldtree->SetBranchAddress("lep3_phi", &lep3_phi);
    oldtree->SetBranchAddress("lep1_E", &lep1_E);
    oldtree->SetBranchAddress("lep2_E", &lep2_E);
    oldtree->SetBranchAddress("lep3_E", &lep3_E);
    oldtree->SetBranchAddress("Jet25_pt", &Jet25_pt);
    oldtree->SetBranchAddress("Jet25_eta", &Jet25_eta);
    oldtree->SetBranchAddress("Jet25_phi", &Jet25_phi);
    oldtree->SetBranchAddress("Jet25_energy", &Jet25_energy);
    oldtree->SetBranchAddress("Jet25_bDiscriminator", &Jet25_bDiscriminator);
    oldtree->SetBranchAddress("Sum2lCharge", &Sum2lCharge);
    oldtree->SetBranchAddress("Sum3LCharge", &Sum3LCharge);
    oldtree->SetBranchAddress("Dilep_nTight", &Dilep_nTight);
    oldtree->SetBranchAddress("Dilep_pdgId", &Dilep_pdgId);
    oldtree->SetBranchAddress("massL_SFOS", &massL_SFOS);
    oldtree->SetBranchAddress("Trilep_nTight", &Trilep_nTight);
    oldtree->SetBranchAddress("nEvent", &nEvent);
    oldtree->SetBranchAddress("mvaOutput_2lss_ttV", &mvaOutput_2lss_ttV);
    oldtree->SetBranchAddress("mvaOutput_2lss_ttbar", &mvaOutput_2lss_ttbar);

    SetOldTreeBranchStatus(oldtree);
    
    //TFile *newfile = new TFile("IHEP_test.root","recreate");
    TFile *newfile = new TFile(Output,"recreate");
    TTree *newtree = new TTree("syncTree","syncTree");
    

    float trueInteractions=0;
    float nBestVtx=0;
    float n_presel_jet=0;
    // angles
    float angle_bbpp_highest2b(-99);
    float cosa_bbpp_highest2b(-99);
    float acuteangle_bbpp_highest2b(-99);
    float deta_highest2b(-99);
    float cosa_highest2b(-99);
    // shape theoretical uncertainties 
    float CMS_ttHl_thu_shape_ttH(0.), CMS_ttHl_thu_shape_ttH_SysUp(0.), CMS_ttHl_thu_shape_ttH_SysDown(0.);
    float CMS_ttHl_thu_shape_ttW(0.), CMS_ttHl_thu_shape_ttW_SysUp(0.), CMS_ttHl_thu_shape_ttW_SysDown(0.);
    float CMS_ttHl_thu_shape_ttZ(0.), CMS_ttHl_thu_shape_ttZ_SysUp(0.), CMS_ttHl_thu_shape_ttZ_SysDown(0.);
    // closure shape uncertainties
    float CMS_ttHl17_Clos_e_shape_ee(0.), CMS_ttHl17_Clos_e_shape_ee_SysUp(0.), CMS_ttHl17_Clos_e_shape_ee_SysDown(0.);
    float CMS_ttHl17_Clos_e_shape_em(0.), CMS_ttHl17_Clos_e_shape_em_SysUp(0.), CMS_ttHl17_Clos_e_shape_em_SysDown(0.);
    float CMS_ttHl17_Clos_m_shape_mm(0.), CMS_ttHl17_Clos_m_shape_mm_SysUp(0.), CMS_ttHl17_Clos_m_shape_mm_SysDown(0.);
    float CMS_ttHl17_Clos_m_shape_em(0.), CMS_ttHl17_Clos_m_shape_em_SysUp(0.), CMS_ttHl17_Clos_m_shape_em_SysDown(0.);
    // cut flags 
    float is_tH_like_and_not_ttH_like=0.;

    newtree = oldtree->CloneTree(0);
    newtree->Branch("TrueInteractions", &trueInteractions);
    newtree->Branch("nBestVTX", &nBestVtx);
    newtree->Branch("nEvt", &nEvt);
    newtree->Branch("xsec_rwgt", &xsec_rwgt);
    newtree->Branch("cpodd_rwgt", &cpodd_rwgt);
    newtree->Branch("nLooseJet", &n_presel_jet);
    newtree->Branch("angle_bbpp_highest2b", &angle_bbpp_highest2b);
    newtree->Branch("cosa_bbpp_highest2b", &cosa_bbpp_highest2b);
    newtree->Branch("acuteangle_bbpp_highest2b", &acuteangle_bbpp_highest2b);
    newtree->Branch("deta_highest2b", &deta_highest2b);
    newtree->Branch("cosa_highest2b", &cosa_highest2b);
    newtree->Branch("is_tH_like_and_not_ttH_like", &is_tH_like_and_not_ttH_like);
    newtree->Branch("CMS_ttHl_thu_shape_ttH", &CMS_ttHl_thu_shape_ttH);
    newtree->Branch("CMS_ttHl_thu_shape_ttH_SysUp", &CMS_ttHl_thu_shape_ttH_SysUp);
    newtree->Branch("CMS_ttHl_thu_shape_ttH_SysDown", &CMS_ttHl_thu_shape_ttH_SysDown);
    newtree->Branch("CMS_ttHl_thu_shape_ttW", &CMS_ttHl_thu_shape_ttW);
    newtree->Branch("CMS_ttHl_thu_shape_ttW_SysUp", &CMS_ttHl_thu_shape_ttW_SysUp);
    newtree->Branch("CMS_ttHl_thu_shape_ttW_SysDown", &CMS_ttHl_thu_shape_ttW_SysDown);
    newtree->Branch("CMS_ttHl_thu_shape_ttZ", &CMS_ttHl_thu_shape_ttZ);
    newtree->Branch("CMS_ttHl_thu_shape_ttZ_SysUp", &CMS_ttHl_thu_shape_ttZ_SysUp);
    newtree->Branch("CMS_ttHl_thu_shape_ttZ_SysDown", &CMS_ttHl_thu_shape_ttZ_SysDown);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_ee", &CMS_ttHl17_Clos_e_shape_ee);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_ee_SysUp", &CMS_ttHl17_Clos_e_shape_ee_SysUp);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_ee_SysDown", &CMS_ttHl17_Clos_e_shape_ee_SysDown);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_em", &CMS_ttHl17_Clos_e_shape_em);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_em_SysUp", &CMS_ttHl17_Clos_e_shape_em_SysUp);
    newtree->Branch("CMS_ttHl17_Clos_e_shape_em_SysDown", &CMS_ttHl17_Clos_e_shape_em_SysDown);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_mm", &CMS_ttHl17_Clos_m_shape_mm);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_mm_SysUp", &CMS_ttHl17_Clos_m_shape_mm_SysUp);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_mm_SysDown", &CMS_ttHl17_Clos_m_shape_mm_SysDown);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_em", &CMS_ttHl17_Clos_m_shape_em);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_em_SysUp", &CMS_ttHl17_Clos_m_shape_em_SysUp);
    newtree->Branch("CMS_ttHl17_Clos_m_shape_em_SysDown", &CMS_ttHl17_Clos_m_shape_em_SysDown);
    
    // lwtnn additional vars 
    float jet1_pt(0.), jet2_pt(0.), jet3_pt(0.), jet4_pt(0.);
    float jet1_eta(0.), jet2_eta(0.), jet3_eta(0.), jet4_eta(0.);
    float jet1_phi(0.), jet2_phi(0.), jet3_phi(0.), jet4_phi(0.);
    float jet1_E(0.), jet2_E(0.), jet3_E(0.), jet4_E(0.);
    float jetFwd1_pt(0.), jetFwd1_eta(0.), n_presel_jetFwd(0.);
    float mT_lep1(0.), resTop_BDT(0.), massL(0.), lep1_charge(0.), avg_dr_jet(0.), mT_lep2(0.), maxeta(0.);
    float mindr_lep2_jet(0.), mindr_lep1_jet(0.), mbb(0.), Hj_tagger_resTop(0.), metLD(0.);
    
    oldtree->SetBranchAddress("lep1_charge", &lep1_charge);
    oldtree->SetBranchAddress("jetFwd1_pt", &jetFwd1_pt);
    oldtree->SetBranchAddress("jetFwd1_eta", &jetFwd1_eta);
    oldtree->SetBranchAddress("n_presel_jetFwd", &n_presel_jetFwd);
    oldtree->SetBranchAddress("mT_lep1", &mT_lep1);
    oldtree->SetBranchAddress("mT_lep2", &mT_lep2);
    oldtree->SetBranchAddress("avg_dr_jet", &avg_dr_jet);
    oldtree->SetBranchAddress("maxeta", &maxeta);
    oldtree->SetBranchAddress("mindr_lep1_jet", &mindr_lep1_jet);
    oldtree->SetBranchAddress("mindr_lep2_jet", &mindr_lep2_jet);
    oldtree->SetBranchAddress("mbb", &mbb);
    oldtree->SetBranchAddress("Hj_tagger_resTop", &Hj_tagger_resTop);
    oldtree->SetBranchAddress("metLD", &metLD);
    oldtree->SetBranchAddress("massL", &massL);
    oldtree->SetBranchAddress("resTop_BDT", &resTop_BDT);
    oldtree->SetBranchAddress("jet1_pt", &jet1_pt);
    oldtree->SetBranchAddress("jet1_eta", &jet1_eta);
    oldtree->SetBranchAddress("jet1_phi", &jet1_phi);
    oldtree->SetBranchAddress("jet1_E", &jet1_E);
    oldtree->SetBranchAddress("jet2_pt", &jet2_pt);
    oldtree->SetBranchAddress("jet2_eta", &jet2_eta);
    oldtree->SetBranchAddress("jet2_phi", &jet2_phi);
    oldtree->SetBranchAddress("jet2_E", &jet2_E);
    oldtree->SetBranchAddress("jet3_pt", &jet3_pt);
    oldtree->SetBranchAddress("jet3_eta", &jet3_eta);
    oldtree->SetBranchAddress("jet3_phi", &jet3_phi);
    oldtree->SetBranchAddress("jet3_E", &jet3_E);
    oldtree->SetBranchAddress("jet4_pt", &jet4_pt);
    oldtree->SetBranchAddress("jet4_eta", &jet4_eta);
    oldtree->SetBranchAddress("jet4_phi", &jet4_phi);
    oldtree->SetBranchAddress("jet4_E", &jet4_E);
    
    float DNN_maxval=0.;
    float DNNCat=0.;
    float DNNSubCat1_option1=0.;
    float DNNSubCat2_option1=0.;
    float DNN_ttHnode_all=0.;
    float DNN_ttJnode_all=0.;
    float DNN_ttWnode_all=0.;
    float DNN_ttZnode_all=0.;
    float DNN_tHQnode_all=0.;
    
    newtree->Branch("DNN_maxval", &DNN_maxval);
    newtree->Branch("DNNCat", &DNNCat);
    newtree->Branch("DNNSubCat1_option1", &DNNSubCat1_option1);
    newtree->Branch("DNNSubCat2_option1", &DNNSubCat2_option1);
    newtree->Branch("DNN_ttHnode_all", &DNN_ttHnode_all);
    newtree->Branch("DNN_ttJnode_all", &DNN_ttJnode_all);
    newtree->Branch("DNN_ttWnode_all", &DNN_ttWnode_all);
    newtree->Branch("DNN_ttZnode_all", &DNN_ttZnode_all);
    newtree->Branch("DNN_tHQnode_all", &DNN_tHQnode_all);
    
    std::map<std::string,double> inputs;
    create_lwtnn(input_json_file, nn_instance);
    
    
    //newtree = oldtree->CopyTree("jet4_pt>=30");
    
    for (Long64_t i=0;i<nentries; i++) {
        trueInteractions = -999;
        n_presel_jet = -999;
        acuteangle_bbpp_highest2b = -9.;
        angle_bbpp_highest2b = -9.;
        cosa_bbpp_highest2b = -9.;
        deta_highest2b = -9.;
        cosa_highest2b = -9.;
        is_tH_like_and_not_ttH_like =0;
        nBestVtx = -999;
        nEvt = -999;
        xsec_rwgt = 1.;
        cpodd_rwgt = 1.;
        oldtree->GetEntry(i);
        Bool_t pass2LMatchRightCharge = kTRUE;
        Bool_t pass2LPromptFS = kTRUE;
        Bool_t pass2LCharge = kTRUE;
        Bool_t pass2LTightID = kTRUE;
        Bool_t pass2LRegionCut = kTRUE;
        Bool_t passTHSelectionCut = kFALSE;
        Bool_t passCut = kFALSE;
        if(!(fabs(Sum2lCharge)==2))pass2LCharge = kFALSE;
        if(!(Dilep_nTight <2))pass2LTightID = kFALSE;
        if(Postfix=="SigRegion" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet <4))pass2LRegionCut = kFALSE;
        if(Postfix=="ttWctrl" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet !=3))pass2LRegionCut = kFALSE;
        if(Postfix=="DiLepRegion" && ( (nBJetLoose < 2 && nBJetMedium < 1) || nLooseJet <3))pass2LRegionCut = kFALSE;
        if(nBJetMedium >0 && nLightJet >0)passTHSelectionCut=kTRUE;
        passCut = pass2LMatchRightCharge && pass2LPromptFS && pass2LCharge && pass2LTightID && (pass2LRegionCut || passTHSelectionCut);
    
        if(passCut){
            trueInteractions = rtrueInteractions;
            nBestVtx = rnBestVtx;
            nEvt = nEvent;
            xsec_rwgt = get_rewgtlumi(FileName);
            n_presel_jet = nLooseJet;
            is_tH_like_and_not_ttH_like = (passTHSelectionCut && !pass2LRegionCut)? 1:0;
            if (nEvent <0) nEvt = nEvent + 4294967296; // 4294967296 = 2^32, this is to fix the problem saving EVENT_event as a wrong type
            else nEvt = nEvent;
            // fill lnN1D_p1()
            // https://github.com/peruzzim/cmgtools-lite/blob/94X_dev_ttH/TTHAnalysis/python/plotter/ttH-multilepton/systsUnc.txt
            CMS_ttHl_thu_shape_ttH = 1.;
            CMS_ttHl_thu_shape_ttH_SysUp = lnN1D_p1(1.05, mvaOutput_2lss_ttbar, -1, 1) * lnN1D_p1(1.02, mvaOutput_2lss_ttV, -1, 1)/1.04;
            CMS_ttHl_thu_shape_ttH_SysDown = 1./CMS_ttHl_thu_shape_ttH_SysUp;
            CMS_ttHl_thu_shape_ttW = 1.;
            CMS_ttHl_thu_shape_ttW_SysUp = lnN1D_p1(1.02, mvaOutput_2lss_ttbar, -1, 1) * lnN1D_p1(1.03, mvaOutput_2lss_ttV, -1, 1)/1.04;
            CMS_ttHl_thu_shape_ttW_SysDown = 1./CMS_ttHl_thu_shape_ttW_SysUp;
            CMS_ttHl_thu_shape_ttZ = 1.;
            CMS_ttHl_thu_shape_ttZ_SysUp = lnN1D_p1(1.06, mvaOutput_2lss_ttbar, -1, 1) * lnN1D_p1(1.06, mvaOutput_2lss_ttV, -1, 1)/1.04;
            CMS_ttHl_thu_shape_ttZ_SysDown = 1./CMS_ttHl_thu_shape_ttZ_SysUp;
            CMS_ttHl17_Clos_e_shape_ee = 1.;
            CMS_ttHl17_Clos_e_shape_ee_SysUp = lnN1D_p1(1.5, mvaOutput_2lss_ttbar, -1, 1)/1.2;
            CMS_ttHl17_Clos_e_shape_ee_SysDown = 1./CMS_ttHl17_Clos_e_shape_ee_SysUp;
            CMS_ttHl17_Clos_e_shape_em = 1.;
            CMS_ttHl17_Clos_e_shape_em_SysUp = lnN1D_p1(1.25, mvaOutput_2lss_ttbar, -1, 1)/1.1;
            CMS_ttHl17_Clos_e_shape_em_SysDown = 1./CMS_ttHl17_Clos_e_shape_em_SysUp;
            CMS_ttHl17_Clos_m_shape_mm = 1.;
            CMS_ttHl17_Clos_m_shape_mm_SysUp = lnN1D_p1(1.5, mvaOutput_2lss_ttV, -1, 1)/1.24;
            CMS_ttHl17_Clos_m_shape_mm_SysDown = 1./CMS_ttHl17_Clos_m_shape_mm_SysUp;
            CMS_ttHl17_Clos_m_shape_em = 1.;
            CMS_ttHl17_Clos_m_shape_em_SysUp = lnN1D_p1(1.8, mvaOutput_2lss_ttV, -1, 1)/1.35;
            CMS_ttHl17_Clos_m_shape_em_SysDown = 1./CMS_ttHl17_Clos_m_shape_em_SysUp;
            
            // calculate lorentz angle
            TLorentzVector Lep1_CMS, Lep2_CMS, p1_CMS, p2_CMS;
            Lep1_CMS.SetPtEtaPhiE(lep1_conept,lep1_eta,lep1_phi,lep1_E);
            Lep2_CMS.SetPtEtaPhiE(lep2_conept,lep2_eta,lep2_phi,lep2_E);
            p1_CMS.SetXYZM(0,0,-1,0.938); // proton mass 938MeV
            p2_CMS.SetXYZM(0,0,1,0.938); 
            TLorentzVector  bJet1, bJet2;
            double b1_CSV= -99;
            double b2_CSV= -999;
            for(uint jet_en=0; jet_en < Jet25_pt->size(); jet_en++){
               // deep CSV value ordered
               if(Jet25_bDiscriminator->at(jet_en)>b1_CSV){
                   // set b2 to old b1
                   b2_CSV = b1_CSV;
                   bJet2 = bJet1;
                   // set b1 to current jet
                   b1_CSV = Jet25_bDiscriminator->at(jet_en);
                   bJet1.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en),Jet25_phi->at(jet_en),Jet25_energy->at(jet_en));
               } else if(Jet25_bDiscriminator->at(jet_en)>b2_CSV){
                   // set b1 to current jet
                   b2_CSV = Jet25_bDiscriminator->at(jet_en);
                   bJet2.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en),Jet25_phi->at(jet_en),Jet25_energy->at(jet_en));
               }
            }
            if(fabs(bJet2.Pt())>0.0001){
                angle_bbpp_highest2b = get_boostedAngle( Lep1_CMS, Lep2_CMS, p1_CMS, p2_CMS, bJet1, bJet2, cosa_bbpp_highest2b);
                deta_highest2b = bJet1.Eta() - bJet2.Eta();
                double temp_angle_2b = getAngleOfVecs(bJet1, bJet2, cosa_highest2b);
            }
            acuteangle_bbpp_highest2b = TMath::Pi()/2.-fabs(angle_bbpp_highest2b-TMath::Pi()/2.);
            
            //lwtnn    
            inputs["lep1_conePt"]=lep1_conept;    
            inputs["lep1_eta"]=lep1_eta;    
            inputs["lep1_phi"]=lep1_phi;    
            inputs["lep1_E"]=lep1_E;    
            inputs["lep2_conePt"]=lep2_conept;    
            inputs["lep2_eta"]=lep2_eta;    
            inputs["lep2_phi"]=lep2_phi;    
            inputs["lep2_E"]=lep2_E;    
            inputs["jet1_pt"]=jet1_pt;    
            inputs["jet1_eta"]=jet1_eta;    
            inputs["jet1_phi"]=jet1_phi;    
            inputs["jet1_E"]=jet1_E;    
            inputs["jet2_pt"]=jet2_pt;    
            inputs["jet2_eta"]=jet2_eta;    
            inputs["jet2_phi"]=jet2_phi;    
            inputs["jet2_E"]=jet2_E;    
            inputs["jet3_pt"]=jet3_pt;    
            inputs["jet3_eta"]=jet3_eta;    
            inputs["jet3_phi"]=jet3_phi;    
            inputs["jet3_E"]=jet3_E;    
            inputs["jet4_pt"]=jet4_pt;    
            inputs["jet4_eta"]=jet4_eta;    
            inputs["jet4_phi"]=jet4_phi;    
            inputs["jet4_E"]=jet4_E;    
            inputs["n_presel_jet"]=n_presel_jet;
            inputs["nBJetLoose"]=nBJetLoose;
            inputs["nBJetMedium"]=nBJetMedium;
            inputs["n_presel_jetFwd"]=n_presel_jetFwd;
            inputs["jetFwd1_pt"]=jetFwd1_pt;
            inputs["jetFwd1_eta"]=jetFwd1_eta;
            inputs["lep1_charge"]=lep1_charge;
            inputs["mT_lep1"]=mT_lep1;
            inputs["mT_lep2"]=mT_lep2;
            inputs["mindr_lep1_jet"]=mindr_lep1_jet;
            inputs["mindr_lep2_jet"]=mindr_lep2_jet;
            inputs["massL"]=massL;
            inputs["resTop_BDT"]=resTop_BDT;
            inputs["Hj_tagger_resTop"]=Hj_tagger_resTop;
            inputs["avg_dr_jet"]=avg_dr_jet;
            inputs["maxeta"]=maxeta;
            inputs["mbb"]=mbb;
            inputs["Dilep_pdgId"]=Dilep_pdgId;
            inputs["metLD"]=metLD;

            for (const auto& in_var: inputs) {
                float input_value = in_var.second;
                //std::cout<< " input NN " << in_var.first << " = " << input_value << std::endl;
            }
            double output_value;
            auto out_vals = nn_instance->compute(inputs);
            for (const auto& out: out_vals) {
                output_value = out.second;
                if (out.first=="predictions_ttH")DNN_ttHnode_all=out.second;
                if (out.first=="predictions_ttJ")DNN_ttJnode_all=out.second;
                if (out.first=="predictions_ttW")DNN_ttWnode_all=out.second;
                if (out.first=="predictions_ttZ")DNN_ttZnode_all=out.second;
                if (out.first=="predictions_tHq")DNN_tHQnode_all=out.second;
            }
            std::vector<double> DNN_vals;
            DNN_vals.push_back(DNN_ttHnode_all);
            DNN_vals.push_back(DNN_ttJnode_all);
            DNN_vals.push_back(DNN_ttWnode_all);
            DNN_vals.push_back(DNN_ttZnode_all);
            DNN_vals.push_back(DNN_tHQnode_all);

            setDNNflag(DNN_vals, DNN_maxval, DNNCat, DNNSubCat1_option1, DNNSubCat2_option1 , Dilep_pdgId, lep1_charge);
            
            newtree->Fill();
        }
        //lwtnn
        jet1_pt=0;
        jet2_pt=0; 
        jet3_pt=0; 
        jet4_pt=0;
        jet1_eta=0; 
        jet2_eta=0; 
        jet3_eta=0; 
        jet4_eta=0;
        jet1_phi=0; 
        jet2_phi=0; 
        jet3_phi=0; 
        jet4_phi=0;
        jet1_E=0; 
        jet2_E=0; 
        jet3_E=0; 
        jet4_E=0;
        jetFwd1_pt=0; 
        jetFwd1_eta=0; 
        n_presel_jetFwd=0;
        mT_lep1=0; 
        resTop_BDT=0; 
        massL=0; 
        lep1_charge=0; 
        avg_dr_jet=0; 
        mT_lep2=0; 
        maxeta=0;
        mindr_lep2_jet=0; 
        mindr_lep1_jet=0; 
        mbb=0; 
        Hj_tagger_resTop=0; 
        Dilep_pdgId=0; 
        lep1_pdgId=0;
        lep2_pdgId=0;
        lep3_pdgId=0;
        lep1_conept=0;
        lep2_conept=0;
        lep1_eta=0;
        lep2_eta=0;
        lep3_eta=0;
        lep1_phi=0;
        lep2_phi=0;
        lep3_phi=0;
        lep1_E=0;
        lep2_E=0;
        lep3_E=0;
        nLooseJet = 0;
        Sum2lCharge =0;
        Dilep_nTight =0;
        Dilep_pdgId =0;
        massL_SFOS =0;
        Trilep_nTight =0;
        mvaOutput_2lss_ttV=0;
        mvaOutput_2lss_ttbar=0;
    }

    newtree->SetName("syncTree");
    newtree->SetTitle("syncTree");
    //newtree->Write();
    newtree->AutoSave();
    gDirectory->Delete("BOOM;*");
    
    delete oldfile;    
    delete newfile;
}

