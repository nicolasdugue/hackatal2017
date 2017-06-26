package fr.labo.hackatal;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by KDE3463 on 24/06/2017.
 */
public class Main {
    final static Logger logger = LoggerFactory.getLogger(Main.class);

    /*
    arg1: args[0], rootPath
    out: classement par année   /spécificité
     */
    public static void main(String... args){
        StatsResourcer statsResourcer = new StatsResourcer();
        //statsResourcer.loadTexts("C:\\Users\\KDE3463\\Documents\\hackatal\\hasIpcCorr\\hasIpcCorr");
        //statsResourcer.fillDomain2Token("C:\\Users\\KDE3463\\Documents\\hackatal\\hasIpcCorr\\hasIpcCorr");
        //List<String> domain

        Specificity specificity = new Specificity();
        //Set<String> classes = statsResourcer.getDomain2Tokens().keySet();
        String term = args[0];    //année //?domaine
        //classe : année
        //classe : domaine
        //sortie terme > rank(année) |rank(domaine)
        //Calcul de tf-idf pour chaque domaine, année
        logger.info("term: " + term);
        int retour = statsResourcer.fillLemmaStats(term);//dans StatsResourcer
        if(retour == 1) return;
        else{
            ArrayList<ArrayList<Integer>> resourceLemmas = statsResourcer.getLemmaStats();
            //logger.info("lemmaYearStats: " + resourceLemmas.get(0));
            //logger.info("lemmaDomainStats: " + resourceLemmas.get(1));
        }
        statsResourcer.fillYear2Occurrences();  //String,Integer    //double!!!!
        statsResourcer.fillDomain2Occurrences();
        statsResourcer.fillNbreDocByDomain();   //String,Integer
        statsResourcer.fillNbreDocByYear();

        //calcul    /année
        logger.info("Classement des années");
        HashMap<String, Double> yearRank = specificity.yearRanking(statsResourcer);
        for(String key : yearRank.keySet()){
            System.out.println(key + "\t" + yearRank.get(key));
        }

        //calcul    /domaine
        logger.info("Classement des domaines");
        HashMap<String, Double> domainRank = specificity.domainRanking(statsResourcer);
        for(String key : domainRank.keySet()){
            System.out.println(key + "\t" + domainRank.get(key));
        }

        //informatique : tf-idf = 0 en 2001 ; idf = 0
        //karaoké : tf-idf = 0 en 2001 ; tf = 0
        //p2o5 : tf-idf = 2.1469829230312202E-7 ; tf = 2.1889466657307704E-7, idf = 0.9808292530117262
    }

}
