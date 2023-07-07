# This Code is Written and Managed By | Himanshu Mahajan | himanshumahajan138@gmail.com |

###########################################################################################
#   COMPILATION TIME OF THIS PROGRAM DEPENDS DIRECTLY ON YOUR INTERNET CONNECTION SPEED   #
###########################################################################################
import sys                                  # import for installing  all required libraries(HERE)
import requests                             # import requests for url calling
from bs4 import BeautifulSoup as bs         # import bs4 for  web scraping 
import pandas as pd                         # import pandas for handelling data frames
import os                                   # import os for getting current directory (HERE)
from pandas.core.common import flatten      # import flatten for flatten lists during result calculations
import nltk                                 # import nltk for all NLP processes
from nltk import word_tokenize,sent_tokenize# import tokenization libraries for tokenization
from inflect import engine                  # import inflect engine for converting numbers to words 
nltk.download('punkt')                      # download punkt for word tokenization
import string                               # import string for advance string functions 
import re                                   # import regex library for regular expressions calculations
import syllables                            # import syllables library for calculating syllables in words

#####################################################################################################################################################
#                                                    SCRAPING PART STARTS HERE                                                                      #
#####################################################################################################################################################

# Function for Scrapping Articles
def scrap(url_id,url):

    # if File with url_id as name already exists in directory then means that url is already scraped 
    if os.path.isfile(f"{os.getcwd()}\scraped_files\\{url_id}.txt"): return None

    # if File with url_id as name doesn't exists in directory means need to scrap that url
    else:
        
        # Getting the response from URL 
        response = requests.get(url=url)
    
        # Checking Whether page exsists or not
        if response.status_code == 200 :        
            
            # storing content as beautifulsoup object
            soup = bs(response.content, 'html.parser')
            
            # scraping the title of the page 
            title = soup.find("title")
            
            # scraping article block
            in_div = soup.find("div" , attrs={"class":"td-post-content"})
            
            # scraping all the paragraphs in article block
            paragraphs = in_div.find_all("p")
            
            # creating and writing files with """URL_ID""" as file name
            with open(f"{os.getcwd()}\scraped_files\\{url_id}.txt" , "w" , encoding="utf-8") as file:
                
                # writing title to file 
                file.write(f"{title.get_text(strip=True)}\n")
                
                # using for loop to write different paragraphs to file 
                for x in paragraphs:
                    file.write(f"{x.get_text(strip=True)}\n")
        
        # if url page doesn't exsists on website then do nothing      
        else : return None

# scraping function for calling scrap function
def scraping():

    # start process Message
    print("\nSCRAPING PROCESS IS RUNNING PLEASE WAIT TILL THIS PART GETS FINISHED , SEE scraped_files FOLDER FOR PROGRESS\n")
    
    # Reading And Storing  """input.xlsx"""  to a variable 
    in_file = pd.read_excel(io=f"{os.getcwd()}\input.xlsx",sheet_name='Sheet1')

    # if folder that conatins all scraped files already exists 
    if os.path.isdir(f"{os.getcwd()}\scraped_files"):
        #using for loop to run scrap function to all indexes in """input.xlsx"""
        for x,y in in_file.values:    
            # calling the function with first parameter as """URL_ID""" and second as """URL"""
            scrap(x,y)

    else : 
        # creating folder named scraped_files for storing all scraped files 
        os.mkdir(f"{os.getcwd()}\scraped_files")
        #using for loop to run scrap function to all indexes in """input.xlsx"""
        for x,y in in_file.values:    
            # calling the function with first parameter as """URL_ID""" and second as """URL"""
            scrap(x,y)
    
    # finished process message 
    print("SCRAPING IS FINISHED AND FILES ARE CREATED IN scraped_files FOLDER\n")

#####################################################################################################################################################
#                                                    SCRAPING PART FINISHED HERE                                                                    #
#####################################################################################################################################################


#####################################################################################################################################################
#                                                    NLP ANALYSIS PART STARTS HERE                                                                  #
#####################################################################################################################################################

##################################################################### CLASS STARTS HERE #############################################################

# class for preprocessing every file and TEXT PRE-PROCESSING
class Text_Preprocessing:

    # lambda function for removing punctuation
    pun_remove = lambda x : str(x).translate(str.maketrans(" "," ",string.punctuation))
    
    # lambda function for replacing \xa0 from scraped file
    replace_xa0  = lambda x : x.replace(u'\xa0',u' ')
    
    # lambda function for replacing hyphen from text
    replace_hyphen  = lambda x : x.replace(u'-',u' ') 
    
    # lambda function for converting numbers to words 
    num_2_word = lambda x : str(engine().number_to_words(x)) if x.isdigit() else x
    
    # lmabda function for removing any extra element rather than alphabet
    remove_extra = lambda x : "" if not x.isalpha() else x

    # lambda function for removing stop words from text
    remove_stop_words = lambda x : x if x not in stopwords else ""
    
    # lambda function for checking complex words 
    complex_check = lambda x : True if syllables.estimate(x)>2 else False
    
    # lambda function for calculating personal pronouns from text
    personal_pronouns = lambda x : re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I).findall(x)
    
    # constructor for applying text preprocessing to every file 
    def __init__(self,file):

        #openig and reading file for preprocessing
        with open(file=file , mode='r',encoding="UTF-8") as f :
            # reading file and storing to a variable 
            self.f = f.read().splitlines()
            
            # applying preprocessing to file text
            self.sentence_list = list(flatten(list(map(sent_tokenize,self.f))))
            self.single_line = " ".join(self.f)
            self.personal_pronouns_list = Text_Preprocessing.personal_pronouns(self.single_line)
            self.f = Text_Preprocessing.replace_hyphen(self.single_line)
            self.f = Text_Preprocessing.pun_remove(self.f)
            self.f = Text_Preprocessing.replace_xa0(self.f)
            self.f = str(self.f).split(" ")
            self.f = " ".join(list(map(Text_Preprocessing.num_2_word,self.f)))
            self.f = Text_Preprocessing.replace_hyphen(self.f)
            self.f = str.lower(self.f)
            self.f = word_tokenize(self.f)
            self.f = list(map(Text_Preprocessing.remove_extra,self.f))
            self.f = list(flatten(list(map(word_tokenize,self.f))))
            self.words_list = self.f
            self.syllable_list = list(filter(Text_Preprocessing.complex_check,self.f))
            self.syllable_per_word_list  = []
            self.syllable_per_word_count_formula = lambda x : self.syllable_per_word_list.append(syllables.estimate(x))
            self.syllable_per_word_count_apply = list(map(self.syllable_per_word_count_formula,self.f))
            self.f = list(map(Text_Preprocessing.remove_stop_words,self.f))
            self.f = list(flatten(list(map(word_tokenize,self.f))))
            # here preprocessing ends and useful results are ready to use

    # method for returning all the result parameters         
    def result(self):
        # returning all important results after preprocessing 
        return self.f , self.sentence_list , self.words_list , self.syllable_list , self.syllable_per_word_list , self.personal_pronouns_list

##################################################################### CLASS ENDS HERE ############################################################

# function for creating stop_word list 
def stop_words_file_creation(folder_name):
        # initiate empty list for storing stop words 
        sw_list = []
        # accessing the files from stop_word folder 
        for file_name in os.listdir(f"{os.getcwd()}\{folder_name}"):
            # opening each file in stop_words folder 
            with open(f"{os.getcwd()}\{folder_name}\{file_name}") as f:
                # appending every word from file to sw_list
                sw_list += list(map(str.lower,f.read().splitlines()))
        # after appending all words to sw_list removing duplicate words from stop_words list 
        return list(set(sw_list))

# function for creating positive and negative word list 
def positive_negative_words_creation(folder_name):
    # initaite two empty lists for positive and negative words 
    positive,negative = [],[] 
    # opening both files from folder and reading them
    with open(f"{os.getcwd()}\{folder_name}\\positive-words.txt" , 'r') as pos , open(f"{os.getcwd()}\{folder_name}\\negative-words.txt" , 'r') as neg :
         # storing positive and neagtive words to respective lists
         positive += pos.read().splitlines()
         negative += neg.read().splitlines()
    # returning both the lists after creation     
    return positive,negative

# Function for extracting the final results from input data 
def result_extraction():
    try:
        # printing result extraction start message 
        print("RESULT EXTRACTION IS GOING ON PLEASE WAIT UNTIL COMPLETION \n")
        # opening and reading sample output excel file for getting all columns name for reference 
        df = pd.read_excel(io=f"{os.getcwd()}\Output-Data-Structure.xlsx",sheet_name='Sheet1')
        # getting all scraped files from scraped_files folder for further analysis
        for file in sorted(os.listdir(f"{os.getcwd()}\scraped_files")):
            # creating object of the class Text_Preprocessing with each file as parameter 
            obj = Text_Preprocessing(f"{os.getcwd()}\scraped_files\\{file}")
            # getting all text pre-processing calculations and storing to respective variables 
            result , sen_list , word_list_before , syllable_list , syllable_per_word_count_list , personal_pronoun_list= obj.result()
            # iniatlize all required variables for further calculations
            positive_score , negative_score , total_length , avg_word_len = 0 , 0 , len(result) , 0
            
            # calculating positive and negative score
            for x in result:
                positive_score += 1 if x in positive_words else 0
                negative_score += 1 if x in negative_words else 0
            
            # storing positive and negative score and getting current url id from file name
            url_id , pos_sc , neg_sc  = int(file.split(".")[0]),positive_score,negative_score
            
            #  calculating polarity score 
            pol_sc = (pos_sc-neg_sc)/((pos_sc+neg_sc)+0.000001)
            
            # caculating sbjectivity score
            subj_sc = (pos_sc+neg_sc)/(total_length+0.000001)

            # calculating average sentence length and average number of words per sentence
            avg_sen_len , avg_num_words_per_sen = len(word_list_before)/len(sen_list) , len(word_list_before)/len(sen_list)

            # calculating complex word percentage and complex word count 
            complex_word_perc , complex_word_count = len(syllable_list)/len(word_list_before) , len(syllable_list)

            # calculating fog index 
            fog_index = 0.4*(avg_sen_len+complex_word_perc)

            # calculating average syllable per word 
            avg_syllable_per_word = sum(syllable_per_word_count_list)/len(syllable_per_word_count_list)
            
            # calculating average word length 
            avg_word_len_list = list(map(lambda x : len(x) , word_list_before))
            avg_word_len = sum(avg_word_len_list )/len(word_list_before)
            
            # getting particular index where to insert all calculations
            indx = df[df["URL_ID"]==url_id].index.values[0]
            
            # inserting respective values to respective index in data frame
            df.at[indx,"POSITIVE SCORE"] = pos_sc
            df.at[indx,"NEGATIVE SCORE"] = neg_sc
            df.at[indx,"POLARITY SCORE"] = pol_sc
            df.at[indx,"SUBJECTIVITY SCORE"] = subj_sc
            df.at[indx,"AVG SENTENCE LENGTH"] = avg_sen_len
            df.at[indx,"PERCENTAGE OF COMPLEX WORDS"] = complex_word_perc
            df.at[indx,"FOG INDEX"] = fog_index
            df.at[indx,"AVG NUMBER OF WORDS PER SENTENCE"] = avg_num_words_per_sen
            df.at[indx,"COMPLEX WORD COUNT"] = complex_word_count
            df.at[indx,"WORD COUNT"] = len(result)
            df.at[indx,"SYLLABLE PER WORD"] = avg_syllable_per_word
            df.at[indx,"PERSONAL PRONOUNS"] = len(personal_pronoun_list)
            df.at[indx,"AVG WORD LENGTH"] = avg_word_len

        # saving result to csv file 
        df.to_csv(path_or_buf=f"{os.getcwd()}/OUTPUT.csv")
        
        # saving result to excel file 
        df.to_excel(excel_writer=f"{os.getcwd()}/OUTPUT.xlsx")
        
        # printing message for completion of result extraction process
        print("RESULTS ARE CALCULATED CHECK '''OUTPUT.csv''' AND '''OUTPUT.xlsx''' FILES FOR RESULT")

    # if any error occured
    except Exception as e :
        # returning error 
        print(e)

##########################################################################################################################################################
#                                                          NLP ANALYSIS ENDS HERE                                                                        #
##########################################################################################################################################################

# if every things gone right 
if __name__ == "__main__":
    try:    
        os.system(f"{sys.executable} -m  pip install -r {os.getcwd()}\\requirements.txt")
        # first of all scrapping all the files 
        scraping()
        # creating stopwords list
        stopwords = stop_words_file_creation("StopWords")
        # creating positive and negative word list 
        positive_words , negative_words = positive_negative_words_creation("MasterDictionary")
        # finally extracting results and storing results 
        result_extraction()
    except  Exception as e:
        print(e)

####################################################################### END HERE THANKS ##################################################################