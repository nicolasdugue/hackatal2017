package fr.labo.hackatal;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Created by KDE3463 on 25/06/2017.
 */
public class Specificity {
    final static Logger logger = LoggerFactory.getLogger(Specificity.class);
    HashMap<String,Double> year2Score = new HashMap<String, Double>();
    HashMap<String,Double> domain2Score = new HashMap<String, Double>();

    public double tf(double result, Integer total) {
        double tf = result / total;         //result :
        //logger.info("tf: " + tf);
        return result / total;
    }

    public HashMap<String,Double> yearRanking(StatsResourcer statsResourcer){
        HashMap<String, Integer> year2Occurrences = statsResourcer.getYear2Occurrences();
        HashMap<String, Integer> year2TotalDoc = statsResourcer.getYear2TotalDoc();
        HashMap<String,Double> index = new HashMap<String, Double>();
        for(String year : year2Occurrences.keySet()){
            //logger.info("year: " + year);
            double result = statsResourcer.getYear2Occurrences().get(year);
            Integer domainSize = statsResourcer.getYear2TotalDoc().get(year);
            double totalCat = 15;
            double totalCatOccur = 0;
            for(String cat : year2Occurrences.keySet()){
                if(year2Occurrences.get(cat)!=0)totalCatOccur++;
            }
            double tfidf = tfIdf(result, domainSize, totalCat, totalCatOccur);
            //logger.info("tfidf: " + tfIdf(result,domainSize,totalCat,totalCatOccur));
            index.put(year,tfidf);
            index = index.entrySet()
                    .stream()
                    .sorted(Map.Entry.comparingByValue(Collections.reverseOrder()))
                    .collect(Collectors.toMap(
                            Map.Entry::getKey,
                            Map.Entry::getValue,
                            (e1, e2) -> e1,
                            LinkedHashMap::new
                    ));
        }
        return index;
    }

    public HashMap<String,Double> domainRanking(StatsResourcer statsResourcer){
        HashMap<String, Integer> domain2Occurrences = statsResourcer.getDomain2Occurrences();
        HashMap<String, Integer> domain2TotalDoc = statsResourcer.getDomain2TotalDoc();
        HashMap<String,Double> index = new HashMap<String, Double>();
        for(String domain : domain2Occurrences.keySet()){
            //logger.info("year: " + year);
            double result = statsResourcer.getDomain2Occurrences().get(domain);
            Integer domainSize = statsResourcer.getDomain2TotalDoc().get(domain);
            double totalCat = 8;
            double totalCatOccur = 0;
            for(String cat : domain2Occurrences.keySet()){
                if(domain2Occurrences.get(cat)!=0)totalCatOccur++;
            }
            double tfidf = tfIdf(result, domainSize, totalCat, totalCatOccur);
            //logger.info("tfidf: " + tfIdf(result,domainSize,totalCat,totalCatOccur));
            index.put(domain,tfidf);
            index = index.entrySet()
                    .stream()
                    .sorted(Map.Entry.comparingByValue(Collections.reverseOrder()))
                    .collect(Collectors.toMap(
                            Map.Entry::getKey,
                            Map.Entry::getValue,
                            (e1, e2) -> e1,
                            LinkedHashMap::new
                    ));
        }
        return index;
    }

    /*
    nul si apparait (rien qu'une seule fois) dans toutes les classes
    //nombre d'années total    /classe  /nombre d'années porteusees
     */
    public double idf(double totalCat,double totalCatOccur){
        //logger.info("totalCat: " + totalCat);
        //logger.info("totalCatOccur: " + totalCatOccur);
        return Math.log(totalCat / totalCatOccur);
    }

    public double tfIdf(double result, Integer domainSize, double totalCat, double totalCatOccur) {
        double idf = tf(result, domainSize) * idf(totalCat, totalCatOccur);
        //logger.info("idf: " + idf);
        return idf;
    }


}
