package SyntaxAnalyzer;

import java.io.File;
import java.util.ArrayList;


public class JackAnalyzer {

    static ArrayList<File> jack_files = new ArrayList<File>();

    /**
     * Return all the .jack files in a directory
     * @param dir
     * @return
     */

    public static void getJackFiles(File dir){
        File[] files = dir.listFiles();
        if (files == null)
            return;
        for (File f:files){
            if(f.isDirectory()){
                getJackFiles(f);
            }
            if(f.isFile()){
                if(f.getName().endsWith(".jack")) {
                    jack_files.add(f);
                }
            }
        }
    }

    public static void main(String[] args) {
        // jack file for testing
        File jack_dir = new File("/Users/zenglezhu/code/mooc/Nand2Tetris/projects/10");
        getJackFiles(jack_dir);
        for (File f: jack_files) {
            String file_out_path = f.getAbsolutePath().substring(0, f.getAbsolutePath().lastIndexOf(".")) + ".xml";
            String token_file_out_path = f.getAbsolutePath().substring(0, f.getAbsolutePath().lastIndexOf(".")) + "T.xml";
            File file_out = new File(file_out_path);
            File token_file_out = new File(token_file_out_path);
            CompilationEngine compilationEngine = new CompilationEngine(f, file_out, token_file_out);
            compilationEngine.compileClass();
            System.out.println("File created : " + file_out_path);
            System.out.println("File created : " + token_file_out_path);
        }

    }
}
