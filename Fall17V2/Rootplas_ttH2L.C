int skimType = 0;
void SetOldTreeBranchStatus(TTree* readtree);
double getMTlepmet(double phi1, double phi2, double pt1, double pt2);
double deltaPhi(double phi1, double phi2);

void Rootplas_ttH2L(TString InputDir, TString OutputDir, TString FileName, TString Postfix, Int_t skimtype=0, Int_t HiggsFilter= 0){
 
    TString Input = InputDir +"/"+ FileName + "Skim.root";
    TString Output = OutputDir  +"/"+FileName+ Postfix+".root";
    std::cout <<" inpupt file is " << Input << std::endl;
    std::cout <<" outpupt file is " << Output << std::endl;
    TFile *oldfile = new TFile(Input);
    TTree *oldtree = (TTree*)oldfile->Get("TNT/BOOM");

    skimType = skimtype;

    Long64_t nentries = oldtree->GetEntries(); 
    std::vector<double>* pvertex_ndof =0;
    std::vector<double>* pvertex_z= 0;
    std::vector<double>* pvertex_dxy= 0;
    std::vector<double>* FakeLep_corrpt =0;
    std::vector<double>* FakeLep_pt =0;
    std::vector<double>* FakeLep_eta =0;
    std::vector<double>* FakeLep_phi =0;
    std::vector<double>* FakeLep_energy =0;
    std::vector<double>* FakeLep_isFromH =0;
    std::vector<double>* Jet25_pt =0;
    std::vector<double>* Jet25_eta =0;
    std::vector<double>* Jet25_phi =0;
    std::vector<double>* Jet25_energy =0;
    std::vector<double>* Jet25_isFromH =0;
    std::vector<double>* Jet25_isFromLepTop =0;
    std::vector<double>* Jet25_HjBDT =0;
    std::vector<double>* Gen_pt =0;
    std::vector<double>* Gen_eta =0;
    std::vector<double>* Gen_phi =0;
    std::vector<double>* Gen_energy =0;
    std::vector<double>* Gen_pdg_id =0;
    
    float nLooseJet=0;
    float rPFMET = 0.;
    float rPFMETphi = 0.;
    int HiggsDecay=0;
    double rtrueInteractions=0;
    int rnBestVtx=0;
    Long64_t nEvt = 0;
    Long64_t nEvent = 0;
   
    float firstLep_mcPromptGamma(0.), secondLep_mcPromptGamma(0.), thirdLep_mcPromptGamma(0.);
    float firstLep_mcPromptFS(0.), secondLep_mcPromptFS(0.), thirdLep_mcPromptFS(0.);
    float lep1_pdgId(0.), lep2_pdgId(0.), lep3_pdgId(0.);
    float Sum2lCharge(0.), Dilep_nTight(0.), massL_SFOS(0.), Trilep_nTight(0.), Dilep_pdgId(0.), Sum3LCharge(0.);
   
    float gen_lvTop_px(0.), gen_lvTop_py(0.), Hj1_score(0.), Hj2_score(0.);
    

    oldtree->SetBranchAddress("PFMET", &rPFMET);
    oldtree->SetBranchAddress("PFMETphi", &rPFMETphi);
    oldtree->SetBranchAddress("trueInteractions", &rtrueInteractions);
    oldtree->SetBranchAddress("nBestVtx", &rnBestVtx);
    //oldtree->SetBranchAddress("pvertex_ndof", &pvertex_ndof);
    //oldtree->SetBranchAddress("pvertex_z", &pvertex_z);
    //oldtree->SetBranchAddress("pvertex_dxy", &pvertex_dxy);
    oldtree->SetBranchAddress("n_presel_jet", &nLooseJet);
    oldtree->SetBranchAddress("HiggsDecay", &HiggsDecay);
    oldtree->SetBranchAddress("lep1_pdgId", &lep1_pdgId);
    oldtree->SetBranchAddress("lep2_pdgId", &lep2_pdgId);
    oldtree->SetBranchAddress("lep3_pdgId", &lep3_pdgId);
    oldtree->SetBranchAddress("leadLep_mcPromptGamma", &firstLep_mcPromptGamma);
    oldtree->SetBranchAddress("secondLep_mcPromptGamma", &secondLep_mcPromptGamma);
    oldtree->SetBranchAddress("thirdLep_mcPromptGamma", &thirdLep_mcPromptGamma);
    oldtree->SetBranchAddress("leadLep_mcPromptFS", &firstLep_mcPromptFS);
    oldtree->SetBranchAddress("secondLep_mcPromptFS", &secondLep_mcPromptFS);
    oldtree->SetBranchAddress("thirdLep_mcPromptFS", &thirdLep_mcPromptFS);
    oldtree->SetBranchAddress("Sum2lCharge", &Sum2lCharge);
    oldtree->SetBranchAddress("Sum3LCharge", &Sum3LCharge);
    oldtree->SetBranchAddress("Dilep_nTight", &Dilep_nTight);
    oldtree->SetBranchAddress("Dilep_pdgId", &Dilep_pdgId);
    oldtree->SetBranchAddress("massL_SFOS", &massL_SFOS);
    oldtree->SetBranchAddress("Trilep_nTight", &Trilep_nTight);
    oldtree->SetBranchAddress("nEvent", &nEvent);
    oldtree->SetBranchAddress("FakeLep_corrpt", &FakeLep_corrpt);
    oldtree->SetBranchAddress("FakeLep_pt", &FakeLep_pt);
    oldtree->SetBranchAddress("FakeLep_eta", &FakeLep_eta);
    oldtree->SetBranchAddress("FakeLep_phi", &FakeLep_phi);
    oldtree->SetBranchAddress("FakeLep_energy", &FakeLep_energy);
    oldtree->SetBranchAddress("FakeLep_isFromH", &FakeLep_isFromH);
    oldtree->SetBranchAddress("Jet25_pt", &Jet25_pt);
    oldtree->SetBranchAddress("Jet25_HjBDT", &Jet25_HjBDT);
    oldtree->SetBranchAddress("Jet25_eta", &Jet25_eta);
    oldtree->SetBranchAddress("Jet25_phi", &Jet25_phi);
    oldtree->SetBranchAddress("Jet25_energy", &Jet25_energy);
    oldtree->SetBranchAddress("Jet25_isFromH", &Jet25_isFromH);
    oldtree->SetBranchAddress("Jet25_isFromLepTop", &Jet25_isFromLepTop);
    oldtree->SetBranchAddress("gen_lvTop_px", &gen_lvTop_px);
    oldtree->SetBranchAddress("gen_lvTop_py", &gen_lvTop_py);
    oldtree->SetBranchAddress("Hj1_score", &Hj1_score);
    oldtree->SetBranchAddress("Hj2_score", &Hj2_score);
    oldtree->SetBranchAddress("Gen_pt", &Gen_pt);
    oldtree->SetBranchAddress("Gen_eta", &Gen_eta);
    oldtree->SetBranchAddress("Gen_phi", &Gen_phi);
    oldtree->SetBranchAddress("Gen_energy", &Gen_energy);
    oldtree->SetBranchAddress("Gen_pdg_id", &Gen_pdg_id);

    SetOldTreeBranchStatus(oldtree);
    
    //TFile *newfile = new TFile("IHEP_test.root","recreate");
    TFile *newfile = new TFile(Output,"recreate");
    TTree *newtree = new TTree("syncTree","syncTree");
    

    float trueInteractions=0;
    float nBestVtx=0;
    float n_presel_jet=0;
    float PFMETpx=0;
    float PFMETpy=0;
    float n_bjets_fromLepTop =0;
    float Mt_matched_ljMet =0;
    float Mt_lMet =0;
    float Mt_jlMet =0;
    float Mt_jjlMet =0;
    float Mt_Hjscore_jlMet =0;
    float genH_pt=0;
    float genH_eta=0;
    float genH_phi=0;
    float genH_energy=0;

    newtree = oldtree->CloneTree(0);
    newtree->Branch("TrueInteractions", &trueInteractions);
    newtree->Branch("nBestVTX", &nBestVtx);
    newtree->Branch("PFMETpx", &PFMETpx);
    newtree->Branch("PFMETpy", &PFMETpy);
    newtree->Branch("nEvt", &nEvt);
    newtree->Branch("nLooseJet", &n_presel_jet);
    newtree->Branch("n_bjets_fromLepTop", &n_bjets_fromLepTop);
    newtree->Branch("Mt_matched_ljMet", &Mt_matched_ljMet);
    newtree->Branch("Mt_lMet", &Mt_lMet);
    newtree->Branch("Mt_jlMet", &Mt_jlMet);
    newtree->Branch("Mt_jjlMet", &Mt_jjlMet);
    newtree->Branch("Mt_Hjscore_jlMet", &Mt_Hjscore_jlMet);
    newtree->Branch("genH_pt", &genH_pt);
    newtree->Branch("genH_eta", &genH_eta);
    newtree->Branch("genH_phi", &genH_phi);
    newtree->Branch("genH_energy", &genH_energy);
    
    
    //newtree = oldtree->CopyTree("jet4_pt>=30");
    
    for (Long64_t i=0;i<nentries; i++) {
        trueInteractions = -999;
        nBestVtx = -999;
        PFMETpy = -999;
        PFMETpx = -999;
        n_presel_jet = -999;
        nEvt = -999;
        genH_pt = -999;
        genH_eta = -999;
        genH_phi = -999;
        genH_energy = -999;
        n_bjets_fromLepTop = -999;
        Mt_matched_ljMet = -999;
        Mt_lMet = -999;
        Mt_jlMet = -999;
        Mt_jjlMet = -999;
        Mt_Hjscore_jlMet = -999;
        oldtree->GetEntry(i);
        Bool_t hasPV = kFALSE;
        Bool_t pass2LPromptGamma = kTRUE;
        Bool_t pass2LPromptFS = kTRUE;
        Bool_t pass3LPromptGamma = kTRUE;
        Bool_t pass3LPromptFS = kTRUE;
        Bool_t passHiggsDecay = kTRUE;
        Bool_t passCut = kFALSE;
        // cut for primary vertex
        /*
        for (unsigned int  en = 0; en <pvertex_ndof->size() ; en++){
            if (pvertex_ndof->at(en) <=4 ) continue;
            if (TMath::Abs(pvertex_z->at(en)) >=24) continue;
            if (pvertex_dxy->at(en) >=2) continue;
            //std::cout << pvertex_ndof->at(en) << " " << pvertex_z->at(en) <<" "  <<pvertex_dxy->at(en)<< std::endl;
            hasPV = kTRUE;
            continue;
        }
        */
        if(!((firstLep_mcPromptGamma==1 && fabs(lep1_pdgId)==11)|| (secondLep_mcPromptGamma==1 && fabs(lep2_pdgId)==11)))pass2LPromptGamma = kFALSE;
        if(!((firstLep_mcPromptGamma==1 && fabs(lep1_pdgId)==11)|| (secondLep_mcPromptGamma==1 && fabs(lep2_pdgId)==11)|| (thirdLep_mcPromptGamma==1 && fabs(lep3_pdgId)==11)  ) )pass3LPromptGamma = kFALSE;
        if(!(firstLep_mcPromptFS==1 && secondLep_mcPromptFS==1))pass2LPromptFS = kFALSE;
        if(!(firstLep_mcPromptFS==1 && secondLep_mcPromptFS==1 && thirdLep_mcPromptFS==1) )pass3LPromptFS = kFALSE;
        if(HiggsFilter>0 && HiggsFilter<999 && HiggsFilter!=HiggsDecay )passHiggsDecay = kFALSE;//hzz,ww,tt,mm
        if(HiggsFilter==999 && (HiggsDecay==2 || HiggsDecay==3 || HiggsDecay==6 || HiggsDecay==11))passHiggsDecay = kFALSE; // hot
        if(skimType == 0) passCut= passHiggsDecay ; // only HiggsDecay cut, no any further cuts, suitable for MVATrain
        if(skimType == 1) passCut = passHiggsDecay && pass2LPromptFS && fabs(Sum2lCharge)==2 && Dilep_nTight ==2 && nLooseJet >=4 ; // 2lss prompt 
        if(skimType == 2) passCut =  pass2LPromptGamma && fabs(Sum2lCharge)==2 && Dilep_nTight ==2 && nLooseJet >=4 ; // 2lss Conv
        if(skimType == 3) passCut = passHiggsDecay && pass2LPromptFS && fabs(Sum2lCharge)==2 && Dilep_nTight ==2 && nLooseJet ==3 ; // 2l ttW prompt 
        if(skimType == 4) passCut =  pass2LPromptGamma && fabs(Sum2lCharge)==2 && Dilep_nTight ==2 && nLooseJet ==3 ; // 2l ttW Conv
        if(skimType == 5) passCut =  fabs(Sum2lCharge)==2 && Dilep_nTight ==2 && nLooseJet >=4 ; // 2lss data 
        if(skimType == 6) passCut =  fabs(Sum2lCharge)==2 && Dilep_nTight <2 && nLooseJet >=4 ; // 2lss fakes 
        if(skimType == 7) passCut =  fabs(Sum2lCharge)==0 && Dilep_nTight ==2 && nLooseJet >=4 && Dilep_pdgId >1 ; // 2l flips 
        if(skimType == 8) passCut =  fabs(Sum2lCharge)==2 && Dilep_nTight ==2 && nLooseJet ==3 ; // 2lttW data 
        if(skimType == 9) passCut =  fabs(Sum2lCharge)==2 && Dilep_nTight <2 && nLooseJet ==3 ; // 2lttW fakes 
        if(skimType == 10) passCut =  fabs(Sum2lCharge)==0 && Dilep_nTight ==2 && nLooseJet ==3 && Dilep_pdgId >1 ; // 2lttW flips 
        if(skimType == 11) passCut = passHiggsDecay && pass3LPromptFS && Trilep_nTight ==3 && fabs(massL_SFOS - 91.2) <10 ; // 3L prompt 
        if(skimType == 12) passCut = pass3LPromptGamma && Trilep_nTight ==3 && fabs(massL_SFOS - 91.2) <10 ; // 3L Conv 
        if(skimType == 13) passCut = passHiggsDecay && pass3LPromptFS && Trilep_nTight ==3 && fabs(massL_SFOS - 91.2) > 10 ; // 3L ttZ prompt 
        if(skimType == 14) passCut = pass3LPromptGamma && Trilep_nTight ==3 && fabs(massL_SFOS - 91.2) >10 ; // 3L ttZ Conv 
        if(skimType == 15) passCut = Trilep_nTight ==3 && fabs(massL_SFOS - 91.2) <10 ; // 3L data 
        if(skimType == 16) passCut = Trilep_nTight <3 && fabs(massL_SFOS - 91.2) <10 ; // 3L fakes
        if(skimType == 17) passCut = Trilep_nTight ==3 && fabs(massL_SFOS - 91.2) >10 ; // 3LttZ data
        if(skimType == 18) passCut = Trilep_nTight <3 && fabs(massL_SFOS - 91.2) >10 ; // 3LttZ fakes
        if(skimType == 21) passCut = passHiggsDecay && pass2LPromptFS && fabs(Sum2lCharge)==2 && Dilep_nTight ==2 ; // 2lss prompt without CutJetN
        if(skimType == 22) passCut =  pass2LPromptGamma && fabs(Sum2lCharge)==2 && Dilep_nTight ==2 ; // 2lss Conv without CutJetN
        if(skimType == 25) passCut =  fabs(Sum2lCharge)==2 && Dilep_nTight ==2; // 2lss data  without CutJetN
        if(skimType == 26) passCut =  fabs(Sum2lCharge)==2 && Dilep_nTight <2 ; // 2lss fakes  without CutJetN
        if(skimType == 27) passCut =  fabs(Sum2lCharge)==0 && Dilep_nTight ==2  && Dilep_pdgId >1 ; // 2l flips  without CutJetN
        
    
        if(passCut){
            trueInteractions = rtrueInteractions;
            nBestVtx = rnBestVtx;
            n_presel_jet = nLooseJet;
            PFMETpx = rPFMET * TMath::Cos(rPFMETphi);
            PFMETpy = rPFMET * TMath::Sin(rPFMETphi);
            nEvt = nEvent;
            TLorentzVector LepH = {0,0,0,0};
            TLorentzVector LepHtagger = {0,0,0,0};
            TLorentzVector Jet1H = {0,0,0,0};
            TLorentzVector Jet2H = {0,0,0,0};
            TLorentzVector Jet1Htagger = {0,0,0,0};
            TLorentzVector Jet2Htagger = {0,0,0,0};
            TLorentzVector METH = {0,0,0,0};
            float MET_nonTop_px = PFMETpx - gen_lvTop_px;
            float MET_nonTop_py = PFMETpy - gen_lvTop_py;
            float MET_nonTop_pz = 0 ;
            METH.SetXYZM(MET_nonTop_px, MET_nonTop_py, MET_nonTop_pz, 0);
            for(uint lep_en=0; lep_en < FakeLep_pt->size(); lep_en++){
                if(lep_en >=2 ) break;
                if(lep_en ==1){
                    LepHtagger.SetPtEtaPhiE(FakeLep_corrpt->at(lep_en),FakeLep_eta->at(lep_en), FakeLep_phi->at(lep_en), FakeLep_energy->at(lep_en));
                }
                if(FakeLep_isFromH->at(lep_en)==1){
                    LepH.SetPtEtaPhiE(FakeLep_corrpt->at(lep_en),FakeLep_eta->at(lep_en), FakeLep_phi->at(lep_en), FakeLep_energy->at(lep_en));
                }
            }
            int n_bjets_fromleptop =0;
            int n_jetH = 0;
            for(uint jet_en=0; jet_en < Jet25_pt->size(); jet_en++){
                if(Jet25_isFromLepTop->at(jet_en)==1)n_bjets_fromleptop ++;
                if(Jet25_isFromH->at(jet_en)==1){
                    if( n_jetH ==0 ){
                        Jet1H.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en), Jet25_phi->at(jet_en), Jet25_energy->at(jet_en));
                    }else if (n_jetH==1){
                        Jet2H.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en), Jet25_phi->at(jet_en), Jet25_energy->at(jet_en));
                    }
                    n_jetH ++; 
                }
                if(abs(Jet25_HjBDT->at(jet_en)-Hj1_score)<0.001){
                    Jet1Htagger.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en), Jet25_phi->at(jet_en), Jet25_energy->at(jet_en));
                }
                if(abs(Jet25_HjBDT->at(jet_en)-Hj2_score)<0.001){
                    Jet2Htagger.SetPtEtaPhiE(Jet25_pt->at(jet_en),Jet25_eta->at(jet_en), Jet25_phi->at(jet_en), Jet25_energy->at(jet_en));
                }
            }
            for(uint gen_en=0; gen_en < Gen_pt->size(); gen_en++){
                if(Gen_pdg_id->at(gen_en)==25){
                    genH_pt = Gen_pt->at(gen_en);
                    genH_eta = Gen_eta->at(gen_en);
                    genH_phi = Gen_phi->at(gen_en);
                    genH_energy = Gen_energy->at(gen_en);
                    break;
                }
            }
            n_bjets_fromLepTop = n_bjets_fromleptop;
            Mt_matched_ljMet = (LepH + Jet1H + Jet2H + METH).Mt();
            Mt_lMet = (LepHtagger + METH).Mt();
            Mt_jlMet = (LepHtagger + METH + Jet1Htagger ).Mt();
            Mt_jjlMet = (LepHtagger + METH + Jet1Htagger + Jet2Htagger ).Mt();
            if(Hj2_score >0.5){
                Mt_Hjscore_jlMet = (LepHtagger + METH + Jet1Htagger + Jet2Htagger ).Mt();
            }else if(Hj1_score>0.3){
                Mt_Hjscore_jlMet = (LepHtagger + METH + Jet1Htagger).Mt();
            }else{
                Mt_Hjscore_jlMet = (LepHtagger + METH).Mt();
            }

            newtree->Fill();
        }
        //pvertex_ndof->clear();
        //pvertex_z->clear();
        //pvertex_dxy->clear();
        FakeLep_corrpt->clear();
        FakeLep_pt->clear();
        FakeLep_eta->clear();
        FakeLep_phi->clear();
        FakeLep_energy->clear();
        FakeLep_isFromH->clear();
        Gen_pt->clear();
        Gen_eta->clear();
        Gen_phi->clear();
        Gen_energy->clear();
        Gen_pdg_id->clear();
        Jet25_pt->clear();
        Jet25_HjBDT->clear();
        Jet25_eta->clear();
        Jet25_phi->clear();
        Jet25_energy->clear();
        Jet25_isFromH->clear();
        Jet25_isFromLepTop->clear();
        HiggsDecay =0;
        lep1_pdgId=0;
        lep2_pdgId=0;
        lep3_pdgId=0;
        firstLep_mcPromptGamma=0;
        secondLep_mcPromptGamma=0;
        thirdLep_mcPromptGamma=0;
        firstLep_mcPromptFS=0;
        secondLep_mcPromptFS=0;
        thirdLep_mcPromptFS=0;
        nLooseJet = 0;
        Sum2lCharge =0;
        Dilep_nTight =0;
        Dilep_pdgId =0;
        massL_SFOS =0;
        Trilep_nTight =0;
        gen_lvTop_px = 0;
        gen_lvTop_py = 0;
        Hj2_score = 0;
        Hj1_score = 0;
    }

    newtree->SetName("syncTree");
    newtree->SetTitle("syncTree");
    //newtree->Write();
    newtree->AutoSave();
    gDirectory->Delete("BOOM;*");
    
    delete oldfile;    
    delete newfile;
}

void SetOldTreeBranchStatus(TTree* readtree){
   readtree->SetBranchStatus("*",0);
   /*
   //readtree->SetBranchStatus("pvertex_ndof",1);
   //readtree->SetBranchStatus("pvertex_z",1);
   //readtree->SetBranchStatus("pvertex_dxy",1);
   readtree->SetBranchStatus("mu1_pt",1);
   readtree->SetBranchStatus("mu1_conept",1);
   readtree->SetBranchStatus("mu1_eta",1);
   readtree->SetBranchStatus("mu1_phi",1);
   readtree->SetBranchStatus("mu1_E",1);
   readtree->SetBranchStatus("mu1_miniRelIso",1);
   readtree->SetBranchStatus("mu1_miniIsoCharged",1);
   readtree->SetBranchStatus("mu1_miniIsoNeutral",1);
   readtree->SetBranchStatus("mu1_jetPtRel",1);
   readtree->SetBranchStatus("mu1_jetPtRatio",1);
   readtree->SetBranchStatus("mu1_jetCSV",1);
   readtree->SetBranchStatus("mu1_sip3D",1);
   readtree->SetBranchStatus("mu1_dxyAbs",1);
   readtree->SetBranchStatus("mu1_dz",1);
   readtree->SetBranchStatus("mu1_segmentCompatibility",1);
   readtree->SetBranchStatus("mu1_leptonMVA",1);
   readtree->SetBranchStatus("mu1_dpt_div_pt",1);
   readtree->SetBranchStatus("mu2_pt",1);
   readtree->SetBranchStatus("mu2_conept",1);
   readtree->SetBranchStatus("mu2_eta",1);
   readtree->SetBranchStatus("mu2_phi",1);
   readtree->SetBranchStatus("mu2_E",1);
   readtree->SetBranchStatus("mu2_miniRelIso",1);
   readtree->SetBranchStatus("mu2_miniIsoCharged",1);
   readtree->SetBranchStatus("mu2_miniIsoNeutral",1);
   readtree->SetBranchStatus("mu2_jetPtRel",1);
   readtree->SetBranchStatus("mu2_jetPtRatio",1);
   readtree->SetBranchStatus("mu2_jetCSV",1);
   readtree->SetBranchStatus("mu2_sip3D",1);
   readtree->SetBranchStatus("mu2_dxyAbs",1);
   readtree->SetBranchStatus("mu2_dz",1);
   readtree->SetBranchStatus("mu2_segmentCompatibility",1);
   readtree->SetBranchStatus("mu2_leptonMVA",1);
   readtree->SetBranchStatus("mu2_dpt_div_pt",1);
   readtree->SetBranchStatus("ele1_pt",1);
   readtree->SetBranchStatus("ele1_conept",1);
   readtree->SetBranchStatus("ele1_eta",1);
   readtree->SetBranchStatus("ele1_phi",1);
   readtree->SetBranchStatus("ele1_E",1);
   readtree->SetBranchStatus("ele1_miniRelIso",1);
   readtree->SetBranchStatus("ele1_miniIsoCharged",1);
   readtree->SetBranchStatus("ele1_miniIsoNeutral",1);
   readtree->SetBranchStatus("ele1_jetPtRel",1);
   readtree->SetBranchStatus("ele1_jetPtRatio",1);
   readtree->SetBranchStatus("ele1_jetCSV",1);
   readtree->SetBranchStatus("ele1_sip3D",1);
   readtree->SetBranchStatus("ele1_dxyAbs",1);
   readtree->SetBranchStatus("ele1_dz",1);
   readtree->SetBranchStatus("ele1_ntMVAeleID",1);
   readtree->SetBranchStatus("ele1_leptonMVA",1);
   readtree->SetBranchStatus("ele2_pt",1);
   readtree->SetBranchStatus("ele2_conept",1);
   readtree->SetBranchStatus("ele2_eta",1);
   readtree->SetBranchStatus("ele2_phi",1);
   readtree->SetBranchStatus("ele2_E",1);
   readtree->SetBranchStatus("ele2_miniRelIso",1);
   readtree->SetBranchStatus("ele2_miniIsoCharged",1);
   readtree->SetBranchStatus("ele2_miniIsoNeutral",1);
   readtree->SetBranchStatus("ele2_jetPtRel",1);
   readtree->SetBranchStatus("ele2_jetPtRatio",1);
   readtree->SetBranchStatus("ele2_jetCSV",1);
   readtree->SetBranchStatus("ele2_sip3D",1);
   readtree->SetBranchStatus("ele2_dxyAbs",1);
   readtree->SetBranchStatus("ele2_dz",1);
   readtree->SetBranchStatus("ele2_ntMVAeleID",1);
   readtree->SetBranchStatus("ele2_leptonMVA",1);
   readtree->SetBranchStatus("mu1_mediumID",1);
   readtree->SetBranchStatus("mu1_isfakeablesel",1);
   readtree->SetBranchStatus("mu1_ismvasel",1);
   readtree->SetBranchStatus("mu2_mediumID",1);
   readtree->SetBranchStatus("mu2_isfakeablesel",1);
   readtree->SetBranchStatus("mu2_ismvasel",1);
   readtree->SetBranchStatus("ele1_isfakeablesel",1);
   readtree->SetBranchStatus("ele1_ismvasel",1);
   readtree->SetBranchStatus("ele1_isChargeConsistent",1);
   readtree->SetBranchStatus("ele1_passesConversionVeto",1);
   readtree->SetBranchStatus("ele2_isfakeablesel",1);
   readtree->SetBranchStatus("ele2_ismvasel",1);
   readtree->SetBranchStatus("ele2_isChargeConsistent",1);
   readtree->SetBranchStatus("ele2_passesConversionVeto",1);
   readtree->SetBranchStatus("mu1_charge",1);
   readtree->SetBranchStatus("mu1_jetNDauChargedMVASel",1);
   readtree->SetBranchStatus("mu2_charge",1);
   readtree->SetBranchStatus("mu2_jetNDauChargedMVASel",1);
   readtree->SetBranchStatus("ele1_charge",1);
   readtree->SetBranchStatus("ele1_jetNDauChargedMVASel",1);
   readtree->SetBranchStatus("ele1_nMissingHits",1);
   readtree->SetBranchStatus("ele2_charge",1);
   readtree->SetBranchStatus("ele2_jetNDauChargedMVASel",1);
   readtree->SetBranchStatus("ele2_nMissingHits",1);
   readtree->SetBranchStatus("mu1_PFRelIso04",1);
   readtree->SetBranchStatus("mu2_PFRelIso04",1);
   readtree->SetBranchStatus("ele1_PFRelIso04",1);
   readtree->SetBranchStatus("ele1_sigmaEtaEta",1);
   readtree->SetBranchStatus("ele1_HoE",1);
   readtree->SetBranchStatus("ele1_deltaEta",1);
   readtree->SetBranchStatus("ele1_deltaPhi",1);
   readtree->SetBranchStatus("ele1_OoEminusOoP",1);
   readtree->SetBranchStatus("ele2_PFRelIso04",1);
   readtree->SetBranchStatus("ele2_sigmaEtaEta",1);
   readtree->SetBranchStatus("ele2_HoE",1);
   readtree->SetBranchStatus("ele2_deltaEta",1);
   readtree->SetBranchStatus("ele2_deltaPhi",1);
   readtree->SetBranchStatus("ele2_OoEminusOoP",1);
   */
   readtree->SetBranchStatus("HiggsDecay",1);
   readtree->SetBranchStatus("tau1_pt",1);
   readtree->SetBranchStatus("tau1_eta",1);
   readtree->SetBranchStatus("tau1_phi",1);
   readtree->SetBranchStatus("tau1_E",1);
   readtree->SetBranchStatus("tau1_dxy",1);
   readtree->SetBranchStatus("tau1_dz",1);
   readtree->SetBranchStatus("tau1_byVLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_byLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_rawMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_decayModeFindingOldDMs",1);
   readtree->SetBranchStatus("tau2_pt",1);
   readtree->SetBranchStatus("tau2_eta",1);
   readtree->SetBranchStatus("tau2_phi",1);
   readtree->SetBranchStatus("tau2_E",1);
   readtree->SetBranchStatus("tau2_dxy",1);
   readtree->SetBranchStatus("tau2_dz",1);
   readtree->SetBranchStatus("tau2_byVLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_byLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_rawMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("jet8_pt",1);
   readtree->SetBranchStatus("jet8_eta",1);
   readtree->SetBranchStatus("jet8_phi",1);
   readtree->SetBranchStatus("jet8_E",1);
   readtree->SetBranchStatus("jet8_CSV",1);
   readtree->SetBranchStatus("jet7_pt",1);
   readtree->SetBranchStatus("jet7_eta",1);
   readtree->SetBranchStatus("jet7_phi",1);
   readtree->SetBranchStatus("jet7_E",1);
   readtree->SetBranchStatus("jet7_CSV",1);
   readtree->SetBranchStatus("jet6_pt",1);
   readtree->SetBranchStatus("jet6_eta",1);
   readtree->SetBranchStatus("jet6_phi",1);
   readtree->SetBranchStatus("jet6_E",1);
   readtree->SetBranchStatus("jet6_CSV",1);
   readtree->SetBranchStatus("jet5_pt",1);
   readtree->SetBranchStatus("jet5_eta",1);
   readtree->SetBranchStatus("jet5_phi",1);
   readtree->SetBranchStatus("jet5_E",1);
   readtree->SetBranchStatus("jet5_CSV",1);
   readtree->SetBranchStatus("tau2_decayModeFindingOldDMs",1);
   readtree->SetBranchStatus("jet4_pt",1);
   readtree->SetBranchStatus("jet4_eta",1);
   readtree->SetBranchStatus("jet4_phi",1);
   readtree->SetBranchStatus("jet4_E",1);
   readtree->SetBranchStatus("jet4_CSV",1);
   readtree->SetBranchStatus("jet1_pt",1);
   readtree->SetBranchStatus("jet1_eta",1);
   readtree->SetBranchStatus("jet1_phi",1);
   readtree->SetBranchStatus("jet1_E",1);
   readtree->SetBranchStatus("jet1_CSV",1);
   readtree->SetBranchStatus("jet2_pt",1);
   readtree->SetBranchStatus("jet2_eta",1);
   readtree->SetBranchStatus("jet2_phi",1);
   readtree->SetBranchStatus("jet2_E",1);
   readtree->SetBranchStatus("jet2_CSV",1);
   readtree->SetBranchStatus("jet3_pt",1);
   readtree->SetBranchStatus("jet3_eta",1);
   readtree->SetBranchStatus("jet3_phi",1);
   readtree->SetBranchStatus("jet3_E",1);
   readtree->SetBranchStatus("jet3_CSV",1);
   readtree->SetBranchStatus("PFMET",1);
   readtree->SetBranchStatus("PFMETphi",1);
   readtree->SetBranchStatus("MHT",1);
   readtree->SetBranchStatus("metLD",1);
   readtree->SetBranchStatus("mht",1);
   readtree->SetBranchStatus("mhtT",1);
   readtree->SetBranchStatus("mhtT_met",1);
   readtree->SetBranchStatus("mht_met",1);
   readtree->SetBranchStatus("lep1_conePt",1);
   readtree->SetBranchStatus("lep2_conePt",1);
   readtree->SetBranchStatus("lep3_conePt",1);
   readtree->SetBranchStatus("mindr_lep1_jet",1);
   readtree->SetBranchStatus("mindr_lep2_jet",1);
   readtree->SetBranchStatus("mindr_lep3_jet",1);
   readtree->SetBranchStatus("mT_lep1",1);
   readtree->SetBranchStatus("mT_lep2",1);
   readtree->SetBranchStatus("min_dr_lep_jet",1);
   readtree->SetBranchStatus("dr_leps",1);
   readtree->SetBranchStatus("max_lep_eta",1);
   readtree->SetBranchStatus("mbb",1);
   readtree->SetBranchStatus("mbb_loose",1);
   readtree->SetBranchStatus("Hj_tagger_resTop",1);
   readtree->SetBranchStatus("Hj_tagger_hadTop",1);
   readtree->SetBranchStatus("HTT",1);
   readtree->SetBranchStatus("nBJetLoose",1);
   readtree->SetBranchStatus("nBJetMedium",1);
   readtree->SetBranchStatus("FR_weight",1);
   readtree->SetBranchStatus("triggerSF_weight",1);
   readtree->SetBranchStatus("bTagSF_weight",1);
   readtree->SetBranchStatus("PU_weight",1);
   readtree->SetBranchStatus("MC_weight",1);
   readtree->SetBranchStatus("mvaOutput_2lss_ttV",1);
   readtree->SetBranchStatus("mvaOutput_2lss_ttbar",1);
   readtree->SetBranchStatus("avg_dr_jet",1);
   readtree->SetBranchStatus("nEvent",1);
   readtree->SetBranchStatus("ls",1);
   readtree->SetBranchStatus("run",1);
   readtree->SetBranchStatus("n_presel_mu",1);
   readtree->SetBranchStatus("n_fakeablesel_mu",1);
   readtree->SetBranchStatus("n_mvasel_mu",1);
   readtree->SetBranchStatus("n_presel_ele",1);
   readtree->SetBranchStatus("n_fakeablesel_ele",1);
   readtree->SetBranchStatus("n_mvasel_ele",1);
   readtree->SetBranchStatus("n_presel_tau",1);
   readtree->SetBranchStatus("n_presel_jet",1);
   readtree->SetBranchStatus("tau1_charge",1);
   readtree->SetBranchStatus("tau1_decayModeFindingOldDMs",1);
   readtree->SetBranchStatus("tau1_decayModeFindingNewDMs",1);
   readtree->SetBranchStatus("tau1_byLooseCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau1_byMediumCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau1_byTightCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau1_byLooseCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau1_byMediumCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau1_byTightCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau1_byLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_byMediumIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_byTightIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau1_byVTightIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_charge",1);
   readtree->SetBranchStatus("tau2_decayModeFindingOldDMs",1);
   readtree->SetBranchStatus("tau2_decayModeFindingNewDMs",1);
   readtree->SetBranchStatus("tau2_byLooseCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau2_byMediumCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau2_byTightCombinedIsolationDeltaBetaCorr3Hits",1);
   readtree->SetBranchStatus("tau2_byLooseCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau2_byMediumCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau2_byTightCombinedIsolationDeltaBetaCorr3HitsdR03",1);
   readtree->SetBranchStatus("tau2_byLooseIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_byMediumIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_byTightIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("tau2_byVTightIsolationMVArun2v1DBdR03oldDMwLT",1);
   readtree->SetBranchStatus("maxeta",1);
   readtree->SetBranchStatus("massL",1);
   readtree->SetBranchStatus("massll",1);
   readtree->SetBranchStatus("massL_SFOS",1);
   readtree->SetBranchStatus("mass_diele",1);
   readtree->SetBranchStatus("Bin2l",1);
   readtree->SetBranchStatus("SubCat2l",1);
   readtree->SetBranchStatus("Sum2lCharge",1);
   readtree->SetBranchStatus("Dilep_bestMVA",1);
   readtree->SetBranchStatus("Dilep_worseMVA",1);
   readtree->SetBranchStatus("Dilep_pdgId",1);
   readtree->SetBranchStatus("Dilep_htllv",1);
   readtree->SetBranchStatus("Dilep_mtWmin",1);
   readtree->SetBranchStatus("Dilep_nTight",1);
   readtree->SetBranchStatus("HighestJetCSV",1);
   readtree->SetBranchStatus("HtJet",1);
   readtree->SetBranchStatus("nBestVtx",1);
   readtree->SetBranchStatus("minMllAFAS",1);
   readtree->SetBranchStatus("minMllAFOS",1);
   readtree->SetBranchStatus("minMllSFOS",1);
   readtree->SetBranchStatus("leadLep_isMatchRightCharge",1);
   readtree->SetBranchStatus("leadLep_mcMatchId",1);
   readtree->SetBranchStatus("leadLep_isFromTop",1);
   readtree->SetBranchStatus("leadLep_isFromH",1);
   readtree->SetBranchStatus("leadLep_isFromB",1);
   readtree->SetBranchStatus("leadLep_isFromC",1);
   readtree->SetBranchStatus("leadLep_mcPromptGamma",1);
   readtree->SetBranchStatus("leadLep_mcPromptFS",1);
   readtree->SetBranchStatus("secondLep_isMatchRightCharge",1);
   readtree->SetBranchStatus("secondLep_mcMatchId",1);
   readtree->SetBranchStatus("secondLep_isFromTop",1);
   readtree->SetBranchStatus("secondLep_isFromH",1);
   readtree->SetBranchStatus("secondLep_isFromB",1);
   readtree->SetBranchStatus("secondLep_isFromC",1);
   readtree->SetBranchStatus("secondLep_mcPromptGamma",1);
   readtree->SetBranchStatus("secondLep_mcPromptFS",1);
   readtree->SetBranchStatus("leadLep_corrpt",1);
   readtree->SetBranchStatus("secondLep_corrpt",1);
   readtree->SetBranchStatus("leadLep_jetdr",1);
   readtree->SetBranchStatus("leadLep_jetcsv",1);
   readtree->SetBranchStatus("secondLep_jetdr",1);
   readtree->SetBranchStatus("secondLep_jetcsv",1);
   readtree->SetBranchStatus("Mt_metleadlep",1);
   //readtree->SetBranchStatus("hadTop_BDT",1);
   readtree->SetBranchStatus("leadLep_BDT",1);
   readtree->SetBranchStatus("secondLep_BDT",1);
   readtree->SetBranchStatus("thirdLep_jetcsv",1);
   readtree->SetBranchStatus("nLepTight",1);
   readtree->SetBranchStatus("trueInteractions",1);
   readtree->SetBranchStatus("nLepFO",1);
   //readtree->SetBranchStatus("Hj1_BDT",1);
   //if(skimType ==0){
       /*
       readtree->SetBranchStatus("HadTop_Dr_leph_bfromlTop",1);
       readtree->SetBranchStatus("HadTop_bjet_lepTop_csv",1);
       readtree->SetBranchStatus("HadTop_bjet_hadTop_csv",1);
       readtree->SetBranchStatus("HadTop_reco_hadTop_pt",1);
       readtree->SetBranchStatus("HadTop_reco_hadTop_mass",1);
       readtree->SetBranchStatus("HadTop_reco_WhadTop_mass",1);
       readtree->SetBranchStatus("HadTop_PtRatio_leptOverleph",1);
       readtree->SetBranchStatus("HadTop_Dr_lept_bfromlTop",1);
       readtree->SetBranchStatus("HadTop_Dr_lept_bfromhTop",1);
       readtree->SetBranchStatus("Jet25_isToptag",1);
       */
       readtree->SetBranchStatus("resTop_BDT",1);
       readtree->SetBranchStatus("bjet_resTop_index",1);
       readtree->SetBranchStatus("wjet1_resTop_index",1);
       readtree->SetBranchStatus("wjet2_resTop_index",1);
       readtree->SetBranchStatus("Jet25_isResToptag",1);
       readtree->SetBranchStatus("Jet25_axis2",1);
       readtree->SetBranchStatus("Jet25_qg",1);
       readtree->SetBranchStatus("Jet25_bDiscriminator",1);
       readtree->SetBranchStatus("Jet25_pfCombinedInclusiveSecondaryVertexV2BJetTags",1);
       readtree->SetBranchStatus("Jet25_pfCombinedMVAV2BJetTags",1);
       readtree->SetBranchStatus("Jet25_pfJetProbabilityBJetTags",1);
       readtree->SetBranchStatus("Jet25_pfDeepCSVCvsLJetTags",1);
       readtree->SetBranchStatus("Jet25_pfDeepCSVCvsBJetTags",1);
       readtree->SetBranchStatus("Jet25_pfDeepFlavourBJetTags",1);
       readtree->SetBranchStatus("Jet25_ptD",1);
       readtree->SetBranchStatus("Jet25_mult",1);
       readtree->SetBranchStatus("Jet25_pfCombinedCvsLJetTags",1);
       readtree->SetBranchStatus("Jet25_pfCombinedCvsBJetTags",1);
       readtree->SetBranchStatus("Jet25_pt",1);
       readtree->SetBranchStatus("Jet25_eta",1);
       readtree->SetBranchStatus("Jet25_phi",1);
       readtree->SetBranchStatus("Jet25_energy",1);
       readtree->SetBranchStatus("Jet25_px",1);
       readtree->SetBranchStatus("Jet25_py",1);
       readtree->SetBranchStatus("Jet25_pz",1);
       readtree->SetBranchStatus("Jet25_mass",1);
       readtree->SetBranchStatus("Jet25_isFromH",1);
       readtree->SetBranchStatus("Jet25_isFromTop",1);
       readtree->SetBranchStatus("Jet25_matchId",1);
       readtree->SetBranchStatus("Jet25_neutralHadEnergyFraction",1);
       //readtree->SetBranchStatus("Jet25_neutralEmEnergyFraction",1);
       readtree->SetBranchStatus("Jet25_chargedHadronEnergyFraction",1);
       readtree->SetBranchStatus("Jet25_chargedEmEnergyFraction",1);
       readtree->SetBranchStatus("Jet25_muonEnergyFraction",1);
       readtree->SetBranchStatus("Jet25_electronEnergy",1);
       readtree->SetBranchStatus("Jet25_photonEnergy",1);
       //readtree->SetBranchStatus("Jet25_emEnergyFraction",1);
       readtree->SetBranchStatus("Jet25_numberOfConstituents",1);
       readtree->SetBranchStatus("Jet25_chargedMultiplicity",1);
       readtree->SetBranchStatus("Jet25_metptratio",1);
       readtree->SetBranchStatus("Jet25_dilepmetptratio",1);
       readtree->SetBranchStatus("Jet25_nonjdr",1);
       readtree->SetBranchStatus("Jet25_nonjdilepdr",1);
       readtree->SetBranchStatus("Jet25_lepdrmin",1);
       readtree->SetBranchStatus("Jet25_lepdrmax",1);
       readtree->SetBranchStatus("Jet25_dilepdr",1);
       readtree->SetBranchStatus("Jet25_bjdr",1);
       readtree->SetBranchStatus("Jet25_nonjdeta",1);
       readtree->SetBranchStatus("Jet25_nonjdilepdeta",1);
       readtree->SetBranchStatus("Jet25_lepdetamin",1);
       readtree->SetBranchStatus("Jet25_lepdetamax",1);
       readtree->SetBranchStatus("Jet25_dilepdeta",1);
       readtree->SetBranchStatus("Jet25_bjdeta",1);
       readtree->SetBranchStatus("Jet25_nonjdphi",1);
       readtree->SetBranchStatus("Jet25_nonjdilepdphi",1);
       readtree->SetBranchStatus("Jet25_lepdphimin",1);
       readtree->SetBranchStatus("Jet25_lepdphimax",1);
       readtree->SetBranchStatus("Jet25_dilepdphi",1);
       readtree->SetBranchStatus("Jet25_bjdphi",1);
       readtree->SetBranchStatus("Jet25_nonjptratio",1);
       readtree->SetBranchStatus("Jet25_nonjdilepptratio",1);
       readtree->SetBranchStatus("Jet25_lepptratiomin",1);
       readtree->SetBranchStatus("Jet25_lepptratiomax",1);
       readtree->SetBranchStatus("Jet25_dilepptratio",1);
       readtree->SetBranchStatus("Jet25_bjptratio",1);
       readtree->SetBranchStatus("Jet25_HjBDT",1);
       readtree->SetBranchStatus("Jet25_isLooseBdisc",1);
       readtree->SetBranchStatus("Jet25_isMediumBdisc",1);
       readtree->SetBranchStatus("Jet25_isTightBdisc",1);
       readtree->SetBranchStatus("Jet25_isFromLepTop",1);
       readtree->SetBranchStatus("Hj1_score",1);
       readtree->SetBranchStatus("Hj2_score",1);
       readtree->SetBranchStatus("FakeLep_corrpt",1);
       readtree->SetBranchStatus("FakeLep_ismvasel",1);
       readtree->SetBranchStatus("FakeLep_charge",1);
       readtree->SetBranchStatus("FakeLep_mvaId",1);
       readtree->SetBranchStatus("FakeLep_minIso",1);
       readtree->SetBranchStatus("FakeLep_minIsoCh",1);
       readtree->SetBranchStatus("FakeLep_minIsoNeu",1);
       readtree->SetBranchStatus("FakeLep_ptratio",1);
       readtree->SetBranchStatus("FakeLep_ptrel",1);
       readtree->SetBranchStatus("FakeLep_sig3d",1);
       readtree->SetBranchStatus("FakeLep_segment",1);
       readtree->SetBranchStatus("FakeLep_lostHits",1);
       readtree->SetBranchStatus("FakeLep_relIso04",1);
       readtree->SetBranchStatus("FakeLep_relIsoRhoEA",1);
       readtree->SetBranchStatus("FakeLep_TightCharge",1);
       readtree->SetBranchStatus("FakeLep_passConv",1);
       readtree->SetBranchStatus("FakeLep_jetdr",1);
       readtree->SetBranchStatus("FakeLep_jetCSV",1);
       readtree->SetBranchStatus("FakeLep_dxyAbs",1);
       readtree->SetBranchStatus("FakeLep_dz",1);
       readtree->SetBranchStatus("FakeLep_leptonMVA",1);
       readtree->SetBranchStatus("FakeLep_jetNDauChargedMVASel",1);
       readtree->SetBranchStatus("FakeLep_isFromB",1);
       readtree->SetBranchStatus("FakeLep_isFromC",1);
       readtree->SetBranchStatus("FakeLep_isFromH",1);
       readtree->SetBranchStatus("FakeLep_isFromTop",1);
       readtree->SetBranchStatus("FakeLep_matchId",1);
       readtree->SetBranchStatus("FakeLep_PdgId",1);
       readtree->SetBranchStatus("FakeLep_matchIndex",1);
       readtree->SetBranchStatus("FakeLep_pt",1);
       readtree->SetBranchStatus("FakeLep_eta",1);
       readtree->SetBranchStatus("FakeLep_phi",1);
       readtree->SetBranchStatus("FakeLep_energy",1);
   //}
   readtree->SetBranchStatus("EventWeight",1);
   readtree->SetBranchStatus("Prefire",1);
   readtree->SetBranchStatus("Prefire_SysUp",1);
   readtree->SetBranchStatus("Prefire_SysDown",1);
   readtree->SetBranchStatus("EVENT_originalXWGTUP",1);
   readtree->SetBranchStatus("EVENT_psWeights",1);
   readtree->SetBranchStatus("EVENT_rWeights",1);
   readtree->SetBranchStatus("EVENT_genWeight",1);
   readtree->SetBranchStatus("EVENT_genWeights",1);
   readtree->SetBranchStatus("bWeight",1);
   readtree->SetBranchStatus("puWeight",1);
   readtree->SetBranchStatus("lepSF",1);
   readtree->SetBranchStatus("ChargeMis",1);
   readtree->SetBranchStatus("FakeRate",1);
   readtree->SetBranchStatus("TriggerSF",1);
   readtree->SetBranchStatus("puWeight_SysUp",1);
   readtree->SetBranchStatus("lepSF_SysUp",1);
   readtree->SetBranchStatus("ChargeMis_SysUp",1);
   //readtree->SetBranchStatus("FakeRate_SysUp",1);
   readtree->SetBranchStatus("TriggerSF_SysUp",1);
   readtree->SetBranchStatus("puWeight_SysDown",1);
   readtree->SetBranchStatus("lepSF_SysDown",1);
   readtree->SetBranchStatus("ChargeMis_SysDown",1);
   //readtree->SetBranchStatus("FakeRate_SysDown",1);
   readtree->SetBranchStatus("TriggerSF_SysDown",1);
   readtree->SetBranchStatus("bWeight_central",1);
   readtree->SetBranchStatus("bWeight_up_jes",1);
   readtree->SetBranchStatus("bWeight_up_lf",1);
   readtree->SetBranchStatus("bWeight_up_hf",1);
   readtree->SetBranchStatus("bWeight_up_hfstats1",1);
   readtree->SetBranchStatus("bWeight_up_hfstats2",1);
   readtree->SetBranchStatus("bWeight_up_lfstats1",1);
   readtree->SetBranchStatus("bWeight_up_lfstats2",1);
   readtree->SetBranchStatus("bWeight_up_cferr1",1);
   readtree->SetBranchStatus("bWeight_up_cferr2",1);
   readtree->SetBranchStatus("bWeight_down_jes",1);
   readtree->SetBranchStatus("bWeight_down_lf",1);
   readtree->SetBranchStatus("bWeight_down_hf",1);
   readtree->SetBranchStatus("bWeight_down_hfstats1",1);
   readtree->SetBranchStatus("bWeight_down_hfstats2",1);
   readtree->SetBranchStatus("bWeight_down_lfstats1",1);
   readtree->SetBranchStatus("bWeight_down_lfstats2",1);
   readtree->SetBranchStatus("bWeight_down_cferr1",1);
   readtree->SetBranchStatus("bWeight_down_cferr2",1);
   readtree->SetBranchStatus("TTHLep_3L",1);
   readtree->SetBranchStatus("Trig_1Ele",1);
   readtree->SetBranchStatus("Trig_2Ele",1);
   readtree->SetBranchStatus("Trig_3Ele",1);
   readtree->SetBranchStatus("Trig_1Mu",1);
   readtree->SetBranchStatus("Trig_1Mu1Ele",1);
   readtree->SetBranchStatus("Trig_1Mu2Ele",1);
   readtree->SetBranchStatus("Trig_2Mu",1);
   readtree->SetBranchStatus("Trig_2Mu1Ele",1);
   readtree->SetBranchStatus("Trig_3Mu",1);
   readtree->SetBranchStatus("Dilep_worseIso",1);
   readtree->SetBranchStatus("Dilep_worseSip",1);
   readtree->SetBranchStatus("mass3L",1);
   readtree->SetBranchStatus("Trilep_mtWmin",1);
   readtree->SetBranchStatus("SubCat3L",1);
   readtree->SetBranchStatus("Sum3LCharge",1);
   readtree->SetBranchStatus("Trilep_n_mu",1);
   readtree->SetBranchStatus("Trilep_nTight",1);
   readtree->SetBranchStatus("Trilep_n_ele",1);
   readtree->SetBranchStatus("Trilep_bestMVA",1);
   readtree->SetBranchStatus("Trilep_worseIso",1);
   readtree->SetBranchStatus("Trilep_worseMVA",1);
   readtree->SetBranchStatus("Trilep_worseSip",1);
   readtree->SetBranchStatus("Dilep_worsedz",1);
   readtree->SetBranchStatus("thirdLep_isMatchRightCharge",1);
   readtree->SetBranchStatus("thirdLep_mcMatchId",1);
   readtree->SetBranchStatus("thirdLep_isFromTop",1);
   readtree->SetBranchStatus("thirdLep_isFromH",1);
   readtree->SetBranchStatus("thirdLep_isFromB",1);
   readtree->SetBranchStatus("thirdLep_isFromC",1);
   readtree->SetBranchStatus("thirdLep_mcPromptGamma",1);
   readtree->SetBranchStatus("thirdLep_mcPromptFS",1);
   readtree->SetBranchStatus("lep3_BDT",1);
   readtree->SetBranchStatus("lep1_charge",1);
   readtree->SetBranchStatus("lep1_dxy",1);
   readtree->SetBranchStatus("lep1_dz",1);
   readtree->SetBranchStatus("lep1_mvaId",1);
   readtree->SetBranchStatus("lep1_eta",1);
   readtree->SetBranchStatus("lep1_minIso",1);
   readtree->SetBranchStatus("lep1_minIsoCh",1);
   readtree->SetBranchStatus("lep1_minIsoNeu",1);
   readtree->SetBranchStatus("lep1_pdgId",1);
   readtree->SetBranchStatus("lep1_pt",1);
   readtree->SetBranchStatus("lep1_phi",1);
   readtree->SetBranchStatus("lep1_ptratio",1);
   readtree->SetBranchStatus("lep1_ptrel",1);
   readtree->SetBranchStatus("lep1_segment",1);
   readtree->SetBranchStatus("lep1_sig3d",1);
   readtree->SetBranchStatus("lep1_lostHits",1);
   readtree->SetBranchStatus("lep1_relIso04",1);
   readtree->SetBranchStatus("lep1_relIso03",1);
   readtree->SetBranchStatus("lep1_TightCharge",1);
   readtree->SetBranchStatus("lep1_passConv",1);
   readtree->SetBranchStatus("lep2_charge",1);
   readtree->SetBranchStatus("lep2_dxy",1);
   readtree->SetBranchStatus("lep2_dz",1);
   readtree->SetBranchStatus("lep2_mvaId",1);
   readtree->SetBranchStatus("lep2_eta",1);
   readtree->SetBranchStatus("lep2_minIso",1);
   readtree->SetBranchStatus("lep2_minIsoCh",1);
   readtree->SetBranchStatus("lep2_minIsoNeu",1);
   readtree->SetBranchStatus("lep2_pdgId",1);
   readtree->SetBranchStatus("lep2_pt",1);
   readtree->SetBranchStatus("lep2_phi",1);
   readtree->SetBranchStatus("lep2_ptratio",1);
   readtree->SetBranchStatus("lep2_ptrel",1);
   readtree->SetBranchStatus("lep2_segment",1);
   readtree->SetBranchStatus("lep2_sig3d",1);
   readtree->SetBranchStatus("lep2_lostHits",1);
   readtree->SetBranchStatus("lep2_relIso04",1);
   readtree->SetBranchStatus("lep2_relIso03",1);
   readtree->SetBranchStatus("lep2_TightCharge",1);
   readtree->SetBranchStatus("lep2_passConv",1);
   readtree->SetBranchStatus("lep3_charge",1);
   readtree->SetBranchStatus("lep3_dxy",1);
   readtree->SetBranchStatus("lep3_dz",1);
   readtree->SetBranchStatus("lep3_mvaId",1);
   readtree->SetBranchStatus("lep3_eta",1);
   readtree->SetBranchStatus("lep3_minIso",1);
   readtree->SetBranchStatus("lep3_minIsoCh",1);
   readtree->SetBranchStatus("lep3_minIsoNeu",1);
   readtree->SetBranchStatus("lep3_pdgId",1);
   readtree->SetBranchStatus("lep3_pt",1);
   readtree->SetBranchStatus("lep3_phi",1);
   readtree->SetBranchStatus("lep3_ptratio",1);
   readtree->SetBranchStatus("lep3_ptrel",1);
   readtree->SetBranchStatus("lep3_segment",1);
   readtree->SetBranchStatus("lep3_sig3d",1);
   readtree->SetBranchStatus("lep3_lostHits",1);
   readtree->SetBranchStatus("lep3_relIso04",1);
   readtree->SetBranchStatus("lep3_relIso03",1);
   readtree->SetBranchStatus("lep3_TightCharge",1);
   readtree->SetBranchStatus("lep3_passConv",1);
   readtree->SetBranchStatus("lep1_E",1);
   readtree->SetBranchStatus("lep1_isfakeablesel",1);
   readtree->SetBranchStatus("lep1_ismvasel",1);
   readtree->SetBranchStatus("lep2_E",1);
   readtree->SetBranchStatus("lep2_isfakeablesel",1);
   readtree->SetBranchStatus("lep2_ismvasel",1);
   readtree->SetBranchStatus("lep3_E",1);
   readtree->SetBranchStatus("lep3_isfakeablesel",1);
   readtree->SetBranchStatus("lep3_ismvasel",1);
   readtree->SetBranchStatus("genWeight_muF2",1);
   readtree->SetBranchStatus("genWeight_muF0p5",1);
   readtree->SetBranchStatus("genWeight_muR2",1);
   readtree->SetBranchStatus("genWeight_muR0p5",1);
   readtree->SetBranchStatus("elelooseSF_SysUp",1);
   readtree->SetBranchStatus("elelooseSF",1);
   readtree->SetBranchStatus("elelooseSF_SysDown",1);
   readtree->SetBranchStatus("eletightSF_SysUp",1);
   readtree->SetBranchStatus("eletightSF",1);
   readtree->SetBranchStatus("eletightSF_SysDown",1);
   readtree->SetBranchStatus("mulooseSF_SysUp",1);
   readtree->SetBranchStatus("mulooseSF",1);
   readtree->SetBranchStatus("mulooseSF_SysDown",1);
   readtree->SetBranchStatus("mutightSF_SysUp",1);
   readtree->SetBranchStatus("mutightSF",1);
   readtree->SetBranchStatus("mutightSF_SysDown",1);
   readtree->SetBranchStatus("FakeRate_m_central",1);
   readtree->SetBranchStatus("FakeRate_m_up",1);
   readtree->SetBranchStatus("FakeRate_m_down",1);
   readtree->SetBranchStatus("FakeRate_m_pt1",1);
   readtree->SetBranchStatus("FakeRate_m_pt2",1);
   readtree->SetBranchStatus("FakeRate_m_be1",1);
   readtree->SetBranchStatus("FakeRate_m_be2",1);
   readtree->SetBranchStatus("FakeRate_m_QCD",1);
   readtree->SetBranchStatus("FakeRate_m_TT",1);
   readtree->SetBranchStatus("FakeRate_e_central",1);
   readtree->SetBranchStatus("FakeRate_e_up",1);
   readtree->SetBranchStatus("FakeRate_e_down",1);
   readtree->SetBranchStatus("FakeRate_e_pt1",1);
   readtree->SetBranchStatus("FakeRate_e_pt2",1);
   readtree->SetBranchStatus("FakeRate_e_be1",1);
   readtree->SetBranchStatus("FakeRate_e_be2",1);
   readtree->SetBranchStatus("FakeRate_e_QCD",1);
   readtree->SetBranchStatus("FakeRate_e_TT",1);
   // Hmass variables
   readtree->SetBranchStatus("Gen_pt",1);
   readtree->SetBranchStatus("Gen_eta",1);
   readtree->SetBranchStatus("Gen_phi",1);
   readtree->SetBranchStatus("Gen_energy",1);
   readtree->SetBranchStatus("Gen_pdg_id",1);
   readtree->SetBranchStatus("gen_lvTop_px",1);
   readtree->SetBranchStatus("gen_lvTop_py",1);
   readtree->SetBranchStatus("gen_lvTop_pz",1);
   readtree->SetBranchStatus("gen_lvTop_E",1);
   readtree->SetBranchStatus("gen_lvTop_Index",1);
   readtree->SetBranchStatus("gen_lvH_px",1);
   readtree->SetBranchStatus("gen_lvH_py",1);
   readtree->SetBranchStatus("gen_lvH_pz",1);
   readtree->SetBranchStatus("gen_lvH_E",1);
   readtree->SetBranchStatus("gen_lvH_Index",1);
   readtree->SetBranchStatus("gen_miss_px",1);
   readtree->SetBranchStatus("gen_miss_py",1);
   readtree->SetBranchStatus("Met_Fake_px",1);
   readtree->SetBranchStatus("Met_Fake_py",1);
   readtree->SetBranchStatus("Met_missFake_px",1);
   readtree->SetBranchStatus("Met_missFake_py",1);
   readtree->SetBranchStatus("n_leptons_fromH",1);
   readtree->SetBranchStatus("n_leptons_fromTop",1);
   readtree->SetBranchStatus("n_leptons_fromB",1);
   readtree->SetBranchStatus("n_jets_fromH",1);
   readtree->SetBranchStatus("n_jets_fromTop",1);
   readtree->SetBranchStatus("jjl_fromH_lvH_mass",1);
   readtree->SetBranchStatus("genWs_fromH_mass",1);
   readtree->SetBranchStatus("genWs_fromTop_mass",1);
   readtree->SetBranchStatus("genZs_fromH_mass",1);
   readtree->SetBranchStatus("genTaus_fromH_mass",1);
   readtree->SetBranchStatus("genWs_fromH_pt",1);
   readtree->SetBranchStatus("genWs_fromTop_pt",1);
   readtree->SetBranchStatus("genZs_fromH_pt",1);
   readtree->SetBranchStatus("genTaus_fromH_pt",1);
   readtree->SetBranchStatus("genWs_fromH_eta",1);
   readtree->SetBranchStatus("genWs_fromTop_eta",1);
   readtree->SetBranchStatus("genZs_fromH_eta",1);
   readtree->SetBranchStatus("genTaus_fromH_eta",1);
   readtree->SetBranchStatus("genWs_fromH_phi",1);
   readtree->SetBranchStatus("genWs_fromTop_phi",1);
   readtree->SetBranchStatus("genZs_fromH_phi",1);
   readtree->SetBranchStatus("genTaus_fromH_phi",1);
   readtree->SetBranchStatus("genWs_fromH_index",1);
   readtree->SetBranchStatus("genWs_fromTop_index",1);
   readtree->SetBranchStatus("genZs_fromH_index",1);
   readtree->SetBranchStatus("genTaus_fromH_index",1);
   readtree->SetBranchStatus("Gen_type1PF_px",1);
   readtree->SetBranchStatus("Gen_type1PF_py",1);
};
// utils
double deltaPhi(double phi1, double phi2){
    double result = phi1 - phi2;
    while (result > M_PI) result -= 2*M_PI;
    while (result <= -M_PI) result += 2*M_PI;
    return result;
}

double getMTlepmet(double phi1, double phi2, double pt1, double pt2){
    double Mass =0;
    Mass = sqrt(2*pt1*pt2*(1-cos(deltaPhi(phi1,phi2))));
    return Mass;
}
