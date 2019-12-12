import argparse
from time import time, sleep
from os import listdir

#Imports Classifier Function For Using Neural To Classify Images 
from classifier import classifier 

#Imports Print Functions To Print Out Results
from print_functions import *

def main():
    #Measures Total Runtime By Collecting Start Time To Later Compare To End Time
    start_time = time()
    
    #Creates And Gets Command Line Arguments
    in_arg = get_input_args()

    #Checks Command Line Arguments Using in_arg 
    check_command_line_arguments(in_arg)

    #Creates Pet Image Labels By Creating A Dictionary 
    answers_dic = get_pet_labels(in_arg.dir)

    #Checks Pet Images Dictionary    
    check_creating_pet_image_labels(answers_dic)

    #Creates Classifier Labels With Classifier Function, Compares Labels, And Creates A Results Dictionary 
    result_dic = classify_images(in_arg.dir, answers_dic, in_arg.arch)

    #Function That Checks Results Dictionary  
    check_classifying_images(result_dic)    

    #Adjusts The Results Dictionary To Determine If Classifier Correctly Classified Images As 'A Dog' Or 'Not A Dog'. This Demonstrates If The Model Can Correctly Classify Dog Images As Dogs
    adjust_results4_isadog(result_dic, in_arg.dogfile)

    #Function that checks Results Dictionary for is-a-dog adjustment - result_dic  
    check_classifying_labels_as_dogs(result_dic)

    #Calculates Results Of Run And Puts Statistics In results_stats_dic
    results_stats_dic = calculates_results_stats(result_dic)

    #Function That Checks Results Stats Dictionary 
    check_calculating_results(result_dic, results_stats_dic)

    #Prints Summary Results, Incorrect Classifications Of Dogs And Breeds If Required
    print_results(result_dic, results_stats_dic, in_arg.arch, True, True)
    
    end_time = time()
    
    #Computes Overall Runtime In Seconds And Prints It Nn hh:mm:ss Format
    tot_time = end_time - start_time
    
    print("Total Elapsed Runtime:",
          str(int((tot_time/3600)))+":"+str(int((tot_time%3600)/60))+":"
          +str(int((tot_time%3600)%60)) )
    print("-----------------------------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------------------------")


def get_input_args():
    parser = argparse.ArgumentParser()

    #Creates 3 Command Line Arguments args.dir For Path To Image Files, args.arch Which Net Model To Use For Classification, args.labels Path To Text File With Names Of Dogs.
    parser.add_argument('--dir', type=str, default='pet_images/', help='path to folder of images')
    parser.add_argument('--arch', type=str, default='vgg', help='chosen model')
    parser.add_argument('--dogfile', type=str, default='dognames.txt', help='text file that has dognames')

    #Returns Parsed Argument Collection
    return parser.parse_args()

def get_pet_labels(image_dir):
    #Creates List Of Files In Directory
    in_files = listdir(image_dir)
    
    #Processes Each Of The Files To Create A Dictionary Where The Key Is The Filename And The Value Is The Picture Label.
    #Creates Empty Dictionary For The Labels
    petlabels_dic = dict()
   
    #Processes Through Each File In The Directory, Extracting Only The Words Of The File That Contain The Pet Image Label.
    for idx in range(0, len(in_files), 1):
       
       # Skips file if starts with . 
       if in_files[idx][0] != ".":
           
           #Uses Split To Extract Words Of Filename Into List image_name 
           image_name = in_files[idx].split("_")
       
           #Creates Temporary Label Variable To Hold Pet Label Name Extracted 
           pet_label = ""
           
           #Processes Each Of The Character Strings Split By '_' In List image_name By Processing Each Word
           for word in image_name:
               
               #Only Add To pet_label If Word Is All Letters Add Blank At End
               if word.isalpha():
                   pet_label += word.lower() + " "
                   
           #Strips Off Trailing Whitespace
           pet_label = pet_label.strip()
           
           #If Filename Doesn't Already Exist In Dictionary Add It And It's Pet Label
           if in_files[idx] not in petlabels_dic:
              petlabels_dic[in_files[idx]] = pet_label
              
           else:
               print("Warning: Duplicate files exist in directory", 
                     in_files[idx])
 
    #Returns Dictionary Of Labels
    return(petlabels_dic)

def classify_images(images_dir, petlabel_dic, model):
    #Creates Dictionary That Will Have All The Results, Key = Filename, Value = List [Pet Label, Classifier Label, Match(1=yes,0=no)]
    results_dic = dict()

    #Process All Files In The petlabels_dic
    for key in petlabel_dic:
       
       # Runs Classifier Function To Classify The Images Classifier Function 
       model_label = classifier(images_dir+key, model)
       
       #Processes The Results So They Can Be Compared With Pet Image Labels
       model_label = model_label.lower()
       model_label = model_label.strip()
       
       #Defines Truth As Pet Image Label And Trys To Find It Using find() 
       truth = petlabel_dic[key]
       found = model_label.find(truth)
       
       # If Found (0 Or Greater) Then Make Sure True Answer Wasn't Found Within Another Word And Thus Not Really Found, If Truely Found Then Add To Results Dictionary And Set match=1(yes) Otherwise As match=0(no)
       if found >= 0:
           if ( (found == 0 and len(truth)==len(model_label)) or
                (  ( (found == 0) or (model_label[found - 1] == " ") )  and
                   ( (found + len(truth) == len(model_label)) or   
                      (model_label[found + len(truth): found+len(truth)+1] in 
                     (","," ") ) 
                   )      
                )
              ):
               #Found Label As Stand-Alone Term
               if key not in results_dic:
                   results_dic[key] = [truth, model_label, 1]
                   
           #Found Within A Word/Term Not A Label Existing On Its Own 
           else:
               if key not in results_dic:
                   results_dic[key] = [truth, model_label, 0]
                   
       #If Not Found Set Results Dictionary With match=0(no)
       else:
           if key not in results_dic:
               results_dic[key] = [truth, model_label, 0]
               
    #Return Results Dictionary
    return(results_dic)

def adjust_results4_isadog(results_dic, dogsfile):         
    #Creates Dognames Dictionary For Quick Matching To results_dic Labels From Real Answer And Classifier's Answer
    dognames_dic = dict()

    #Reads In Dognames From File, 1 Name Per Line And Automatically Closes File
    with open(dogsfile, "r") as infile:
        #Reads In Dognames From First Line In File
        line = infile.readline()

        #Processes Each Line In File Until Reaching EOF By Processing Line And Adding Dognames To dognames_dic With While Loop
        while line != "":

            #Process Line By Striping Newline From Line
            line = line.rstrip()

            #Adds Dogname To dogsnames_dic If It Doesn't Already Exist In dic
            if line not in dognames_dic:
                dognames_dic[line] = 1
            else:
                print("**Warning: Duplicate dognames", line)            

            #Reads In Next Line In File To Be Processed With While Loop If This Line Isn't Empty
            line = infile.readline()
    
    for key in results_dic:

        #Pet Image Label IS Of Dog
        if results_dic[key][0] in dognames_dic:
            
            #Classifier Label IS Image Of Dog (e.g. Found In dognames_dic) Appends (1, 1) Because Both Labels Are Dogs
            if results_dic[key][1] in dognames_dic:
                results_dic[key].extend((1, 1))
                
            #Classifier Label IS NOT Image Of Dog (e.g. NOT In dognames_dic) Appends (1,0) Because Only Pet Label Is A Dog
            else:
                results_dic[key].extend((1, 0))
            
        #Pet Image Label IS NOT A Dog Image (e.g. NOT Found In dognames_dic)
        else:
            #Classifier Label IS image Of Dog (e.g. Found In dognames_dic) Appends (0, 1) Because Only Classifier Label Is A Dog
            if results_dic[key][1] in dognames_dic:
                results_dic[key].extend((0, 1))
                
            #Classifier Label IS NOT Image Of Dog (e.g. NOT In dognames_dic) Appends (0, 0) Because Both Labels Aren't Dogs
            else:
                results_dic[key].extend((0, 0))

def calculates_results_stats(results_dic):
    #Creates Empty Dictionary For results_stats
    results_stats=dict()
    
    #Sets All Counters To Initial Values Of Zero So That They Can Be Incremented While Processing Through The Images In results_dic 
    results_stats['n_dogs_img'] = 0
    results_stats['n_match'] = 0
    results_stats['n_correct_dogs'] = 0
    results_stats['n_correct_notdogs'] = 0
    results_stats['n_correct_breed'] = 0       
    
    #Process Through The Results Dictionary
    for key in results_dic:
        #Labels Match Exactly
        if results_dic[key][2] == 1:
            results_stats['n_match'] += 1
            
        #Pet Image Label Is A Dog AND Labels Match - Counts Correct Breed
        if sum(results_dic[key][2:]) == 3:
                results_stats['n_correct_breed'] += 1
        
        #Pet Image Label Is A Dog - Counts Number Of Dog Images
        if results_dic[key][3] == 1:
            results_stats['n_dogs_img'] += 1
            
            #Classifier Classifies Image As Dog (And Pet Image Is A Dog) Counts Number Of Correct Dog Classifications
            if results_dic[key][4] == 1:
                results_stats['n_correct_dogs'] += 1
                
        #Pet Image Label Is NOT A Dog
        else:
            #Classifier Classifies Image As NOT A Dog(And Pet Image Isn't A Dog) Counts Number Of Correct NOT Dog Clasifications
            if results_dic[key][4] == 0:
                results_stats['n_correct_notdogs'] += 1

    #Calculates Run Statistics (Counts And Percentages) Below That Are Calculated Using Counters From Above
    #Calculates Number Of Total Images
    results_stats['n_images'] = len(results_dic)

    #Calculates Number Of Not-A-Dog Images Using - Images And Dog Images Counts
    results_stats['n_notdogs_img'] = (results_stats['n_images'] - 
                                      results_stats['n_dogs_img']) 

    #Calculates % Correct For Matches
    results_stats['pct_match'] = (results_stats['n_match'] / 
                                  results_stats['n_images'])*100.0
    
    #Calculates % Correct Dogs
    results_stats['pct_correct_dogs'] = (results_stats['n_correct_dogs'] / 
                                         results_stats['n_dogs_img'])*100.0    

    #Calculates % Correct Breed Of Dog
    results_stats['pct_correct_breed'] = (results_stats['n_correct_breed'] / 
                                          results_stats['n_dogs_img'])*100.0

    #Calculates % Correct Not-A-Dog Images
    #Uses Conditional Statement For When No 'Not A Dog' Images Were Submitted 
    if results_stats['n_notdogs_img'] > 0:
        results_stats['pct_correct_notdogs'] = (results_stats['n_correct_notdogs'] /
                                                results_stats['n_notdogs_img'])*100.0
    else:
        results_stats['pct_correct_notdogs'] = 0.0
        
    return results_stats

def print_results(results_dic, results_stats, model, 
                  print_incorrect_dogs = False, print_incorrect_breed = False):   
    #Prints Summary Statistics Over The Run
    print("-----------------------------------------------------------------------------------------------------------------")
    print("\n\n*** Results Summary for CNN Model Architecture",model.upper(), 
          "***")
    print("%20s: %3d" % ('N Images', results_stats['n_images']))
    print("%20s: %3d" % ('N Dog Images', results_stats['n_dogs_img']))
    print("%20s: %3d" % ('N Not-Dog Images', results_stats['n_notdogs_img']))

    #Prints Summary Statistics (Percentages) On Model Run
    print(" ")
    for key in results_stats:
        if key[0] == "p":
            print("%20s: %5.1f" % (key, results_stats[key]))
    print("-----------------------------------------------------------------------------------------------------------------")

    # IF print_incorrect_dogs == True AND There Were Images Incorrectly Classified As Dogs Or Vice Versa - Print Out These Cases
    if (print_incorrect_dogs and 
        ( (results_stats['n_correct_dogs'] + results_stats['n_correct_notdogs'])
          != results_stats['n_images'] ) 
       ):
        print("-----------------------------------------------------------------------------------------------------------------")
        print("\nINCORRECT Dog/NOT Dog Assignments:")

        #Process Through results dict, Printing Incorrectly Classified Dogs
        for key in results_dic:

            #Pet Image Label Is A Dog - Classified As NOT-A-DOG OR Pet Image Label Is NOT-A-Dog - Classified As A-DOG
            if sum(results_dic[key][3:]) == 1:
                print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0],
                                                          results_dic[key][1]))
        print("-----------------------------------------------------------------------------------------------------------------")

    # IF print_incorrect_breed == True AND There Were Dogs Whose Breeds Were Incorrectly Classified - Print Out These Cases                    
    if (print_incorrect_breed and 
        (results_stats['n_correct_dogs'] != results_stats['n_correct_breed']) 
       ):
        print("-----------------------------------------------------------------------------------------------------------------")
        print("\nINCORRECT Dog Breed Assignment:")

        #Process Through results_dict, Printing Incorrectly Classified Breeds
        for key in results_dic:

            # Pet Image Label Is-A-Dog, Classified As-A-Dog But Is WRONG Breed
            if ( sum(results_dic[key][3:]) == 2 and
                results_dic[key][2] == 0 ):
                print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0],
                                                          results_dic[key][1]))
        print("-----------------------------------------------------------------------------------------------------------------")
        print("-----------------------------------------------------------------------------------------------------------------")
                
#Call To Main Function To Run The Program
if __name__ == "__main__":
    main()
