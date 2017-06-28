package fr.labo.hackatal;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import com.fasterxml.jackson.databind.type.TypeFactory;
/**
 * Created by KDE3463 on 24/06/2017.
 */
public class StatsResourcer {
    private HashMap<String,ArrayList<String>> domain2Tokens = new HashMap<String, ArrayList<String>>();
    private HashMap<String,HashMap<String,ArrayList<String>>> year2Tokens = new HashMap<String, HashMap<String, ArrayList<String>>>();
    final static Logger logger = LoggerFactory.getLogger(StatsResourcer.class);
    private static final String VOC_LEMMA_FILEPATH = "/vocLemma.tsv";
    private static final String FILE_BY_DOMAIN = "/fileByDomain.tsv";
    private static final String FILE_BY_YEAR = "/docByYear.tsv";
    String resourceLemmas;
    ArrayList<ArrayList<Integer>> lemmaStats = new ArrayList<ArrayList<Integer>>();
    private HashMap<String,Integer> year2Occurrences = new HashMap<String, Integer>();
    private HashMap<String,Integer> domain2Occurrences = new HashMap<String, Integer>();
    private HashMap<String,Integer> domain2TotalDoc = new HashMap<String, Integer>();
    private HashMap<String,Integer> year2TotalDoc = new HashMap<String, Integer>();

    public void findLemmaInfos(String lemma){
        Pattern compile = Pattern.compile("farinage");
        //logger.info("text: " + resourceLemmas);
        Matcher matcher = compile.matcher(resourceLemmas);
        logger.info("tab[1]: " + matcher.group());

        //mettre les infos dans HashMap
        //tf-idf pour chaque classe > rank des classes
        //
    }

    public HashMap<String, Integer> getYear2Occurrences() {
        return year2Occurrences;
    }

    public HashMap<String, Integer> getDomain2Occurrences() {
        return domain2Occurrences;
    }

    public Integer getYearSize(String year){
        return year2TotalDoc.get(year);
    }

    public Integer getDomainSize(String domain){
        return domain2TotalDoc.get(domain);
    }



    public void fillYear2Occurrences(){
        ArrayList<Integer> year2Occurrences = lemmaStats.get(0);
        //logger.info("year2Occurrnces: " + year2Occurrences);
        int currentYear = 2001;
        for (int i = 0 ; i < year2Occurrences.size() ; i++){
            this.year2Occurrences.put(String.valueOf(currentYear),year2Occurrences.get(i));
            currentYear++;
        }
    }

    //Fichier Texte > String
    public String getFile(String path) throws IOException {
        String result = "";

        BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(path), StandardCharsets.UTF_8));
        String line;
        while ((line = in.readLine()) != null)
        {
            result = result + line+"\n";
        }
        in.close();
        return result;
    }

    public void fillNbreDocByDomain(){
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(StatsResourcer.class.getResourceAsStream(FILE_BY_DOMAIN), StandardCharsets.UTF_8));
            String line;
            Pattern compile = Pattern.compile("(.)\t(.+)");
            while ((line = in.readLine()) != null)
            {
                //logger.info("line: " + line);
                Matcher matcher = compile.matcher(line);
                if(matcher.find()){
                    String group = matcher.group(1);
                    Integer value = Integer.valueOf(matcher.group(2));
                    //logger.info("group: " + group);
                    //logger.info("value: " + value);
                    domain2TotalDoc.put(group,value);
                }
            }
            //String file = getFile("C:\\Users\\KDE3463\\Documents\\hackatal\\NbDocByClassSorted.tsv");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void fillDomain2Occurrences(){
        ArrayList<Integer> domain2Occurrences = lemmaStats.get(1);
        for (int i = 0 ; i < domain2Occurrences.size() ; i++){
            switch (i){
                case(0):
                    this.domain2Occurrences.put("A",domain2Occurrences.get(i));
                    break;
                case(1):
                    this.domain2Occurrences.put("B",domain2Occurrences.get(i));
                    break;
                case(2):
                    this.domain2Occurrences.put("C",domain2Occurrences.get(i));
                    break;
                case(3):
                    this.domain2Occurrences.put("D",domain2Occurrences.get(i));
                    break;
                case(4):
                    this.domain2Occurrences.put("E",domain2Occurrences.get(i));
                    break;
                case(5):
                    this.domain2Occurrences.put("F",domain2Occurrences.get(i));
                    break;
                case(6):
                    this.domain2Occurrences.put("G",domain2Occurrences.get(i));
                    break;
                case(7):
                    this.domain2Occurrences.put("H",domain2Occurrences.get(i));
                    break;
            }
        }
    }

    public ArrayList<String> pathWalker(String path) throws IOException {
        File file = new File(path);
        File[] files = file.listFiles();
        ArrayList<String> paths = new ArrayList();
        for (int i = 0; i < files.length; i++) {

            //System.out.println(files[i].getAbsolutePath());
            paths.add(files[i].getAbsolutePath());
        }
        return paths;
    }

    public HashMap<String, Integer> getDomain2TotalDoc() {
        return domain2TotalDoc;
    }

    public HashMap<String, Integer> getYear2TotalDoc() {
        return year2TotalDoc;
    }

    public void fillNbreDocByYear(){
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(StatsResourcer.class.getResourceAsStream(FILE_BY_YEAR), StandardCharsets.UTF_8));
            String line;
            Pattern compile = Pattern.compile("(\\d\\d\\d\\d)\t(.+)");
            while ((line = in.readLine()) != null)
            {
                //logger.info("line: " + line);
                Matcher matcher = compile.matcher(line);
                if(matcher.find()){
                    String group = matcher.group(1);
                    Integer value = Integer.valueOf(matcher.group(2));
                    //logger.info("group: " + group);
                    //logger.info("value: " + value);
                    year2TotalDoc.put(group,value);
                }
            }
            //String file = getFile("C:\\Users\\KDE3463\\Documents\\hackatal\\NbDocByClassSorted.tsv");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public HashMap<String, HashMap<String, ArrayList<String>>> getYear2Tokens() {
        return year2Tokens;
    }

    public HashMap<String,ArrayList<String>> getDomain2Tokens() {
        return domain2Tokens;
    }

    //Fichier Texte > String
    public int fillLemmaStats(String lemma) {
        String result = "";
        //logger.info("path: " + path);
        BufferedReader in = new BufferedReader(new InputStreamReader(StatsResourcer.class.getResourceAsStream(VOC_LEMMA_FILEPATH)));
        String line;
        Pattern compile = Pattern.compile(lemma+"\t(.+?)\t.+?(\\[.+?\\]).+");
        ObjectMapper mapper = new ObjectMapper();
        CollectionType type = TypeFactory.defaultInstance().constructCollectionType(ArrayList.class, Integer.class);
        try {
            while ((line = in.readLine()) != null)
            {
                //logger.info("line: " + line);i++;
                Matcher matcher = compile.matcher(line);
                if(matcher.find()){
                    String group1 = matcher.group(1);
                    //logger.info("group: " + group1);
                    ArrayList<Integer> yearOccurrences = mapper.readValue(group1, type);
                    String group2 = matcher.group(2);
                    //logger.info("group: " + group2);
                    ArrayList<Integer> domainOccurrences = mapper.readValue(group2, type);
                    in.close();
                    if(yearOccurrences == null || domainOccurrences == null) return 1;  //code erreur
                    else{
                        lemmaStats.add(yearOccurrences);
                        lemmaStats.add(domainOccurrences);
                        return 0;
                    }
                }
            }
        } catch (IOException e) {
            logger.error("Problème de lecture fichier de lemmes !");
            e.printStackTrace();
        }
        return 1;
    }


    public ArrayList<ArrayList<Integer>> getLemmaStats() {
        return lemmaStats;
    }
}
