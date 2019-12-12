def check_command_line_arguments(in_arg):
    print("-----------------------------------------------------------------------------------------------------------------")
    print("COMMAND LINE ARGUMENTS:  DIRECTORY =", in_arg.dir, #Directory For Images
          "ARCHITECTURE =", in_arg.arch, "LOCATION =", in_arg.dogfile) #Net And Location Of Text File To Write To
    print("-----------------------------------------------------------------------------------------------------------------")

#Prints 10 Key-Value Pairs And Checks There Are 40 Valid Pairs.
def check_creating_pet_image_labels(petlabels_dic):
    print("-----------------------------------------------------------------------------------------------------------------")
    print("PET IMAGE LABEL DICTIONARY HAS", len(petlabels_dic),
          "KEY-VALUE PAIRS. EXAMPLES INCLUDE:")
    print("") #Break

    n = 0 #Initial Value
    #Iterate Through The Dictionary
    for key in petlabels_dic:
 
        #Prints Only First 10 Labels With Alignments
        if n < 10:
            print("%2d KEY: %-30s  VALUE: %-26s" % 
                  (n+1, key, petlabels_dic[key]) )

            #Increment Counter
            n += 1

        #Exit After 10 
        else:
            break
    print("-----------------------------------------------------------------------------------------------------------------")

#Checks Matches And Not Matches For Correct Dog Breed Are Classified As A Match Or Not A Match
def check_classifying_images(results_dic):
    
    #Default To 0
    n_match = 0
    n_notmatch = 0
    
    #Prints All Matches First
    print("-----------------------------------------------------------------------------------------------------------------")
    print("     MATCH: (CORRECT BREED)")
    for key in results_dic:

        #Prints Only If A Match Index 2 == 1 i.e True
        if results_dic[key][2] == 1: #3 Columns (Key, Actual, Classifier) -> If Classifier == 'True' (1) == Correct Breed

            #Increments Match Counter
            n_match += 1
            #Prints Results
            print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0],
                                                       results_dic[key][1]))
    print("-----------------------------------------------------------------------------------------------------------------")
    #Prints All Non-Matches Next
    print("-----------------------------------------------------------------------------------------------------------------")
    print("     NOT A MATCH: (INCORRECT BREED)")
    for key in results_dic:
    
        #Prints Only If Not A Match Index 2 == 0 i.e False (See Logic Above)
        if results_dic[key][2] == 0:
 
            # Increments Not A Match Counter
            n_notmatch += 1
            #Print Results
            print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0],
                                                   results_dic[key][1]))

    #Prints Total Number of Images - Expects 40 From pet_images Folder
    print("")
    print("Total Images",n_match + n_notmatch, "# Matches:",n_match , #Display
          "# NOT Matches:",n_notmatch)
    print("-----------------------------------------------------------------------------------------------------------------")

#Checks Classifying Of Dogs Is Correct, Either Being A "Dog" or "Not A Dog"
def check_classifying_labels_as_dogs(results_dic):
    
    #Default To 0
    n_match = 0
    n_notmatch = 0
    
    #Prints All Matches First
    print("-----------------------------------------------------------------------------------------------------------------")
    print("     MATCH: (IS A DOG)")
    for key in results_dic:

        #Prints Only If A Match Index 2 == 1 i.e True (Classifier Column == 'True')
        if results_dic[key][2] == 1:

            #Increments Match counter
            n_match += 1
            #Print Results
            print("Real: %-26s   Classifier: %-30s  PetLabelDog: %1d  ClassLabelDog: %1d"
                  % (results_dic[key][0], results_dic[key][1], 
                     results_dic[key][3], results_dic[key][4]))
    print("-----------------------------------------------------------------------------------------------------------------")

    #Prints All Not A Matches Next
    print("-----------------------------------------------------------------------------------------------------------------")
    print("     NOT A MATCH: (ISN'T A DOG)")
    for key in results_dic:
        
        #Prints Only If Not A Match Index 2 == 0  i.e False (Opposite Logic)
        if results_dic[key][2] == 0:
 
            #Increments Not A Match Counter
            n_notmatch += 1
            #Print Results
            print("Real: %-26s   Classifier: %-30s  PetLabelDog: %1d  ClassLabelDog: %1d"
                  % (results_dic[key][0], results_dic[key][1], 
                     results_dic[key][3], results_dic[key][4]))

    #Prints Total Number Of Images - Expects 40 From pet_images Folder
    print("")
    print("\n# Total Images",n_match + n_notmatch, "# Matches:",n_match ,
          "# NOT Matches:",n_notmatch)
    print("-----------------------------------------------------------------------------------------------------------------")

#Checks Calculations Of Counts And Percentages By Using Dictionaries To Compare Values
def check_calculating_results(results_dic, results_stats):

    #Initialise Counters To 0 And Number Of Images Total
    n_images = len(results_dic)
    n_pet_dog = 0
    n_class_cdog = 0
    n_class_cnotd = 0
    n_match_breed = 0
    
    #Iterates Through results_dic Dictionary To Recompute The Statistics
    for key in results_dic:

        #Match (If Dog Then Breed Match)
        if results_dic[key][2] == 1:

            #Is A Dog (Pet Label) & Breed Match
            if results_dic[key][3] == 1:
                n_pet_dog += 1

                #Is A Dog (Classifier Label) & Breed Match
                if results_dic[key][4] == 1:
                    n_class_cdog += 1
                    n_match_breed += 1

            #Not A Dog (Pet_Label)
            else:
                #Not A Dog (Classifier Label)
                if results_dic[key][4] == 0:
                    n_class_cnotd += 1

        #Not A Match (Not A Breed Match If A Dog)
        else:
            #Not A Match, Is A Dog (Pet Label) 
            if results_dic[key][3] == 1:
                n_pet_dog += 1

                #Is A Dog (Classifier Label)
                if results_dic[key][4] == 1:
                    n_class_cdog += 1

            #Not A Dog (Pet Label)
            else:
                #Not A Dog (Classifier Label)
                if results_dic[key][4] == 0:
                    n_class_cnotd += 1

                    
    #Calculates Statistics Based Upon Counters From Above
    n_pet_notd = n_images - n_pet_dog
    pct_corr_dog = ( n_class_cdog / n_pet_dog )*100
    pct_corr_notdog = ( n_class_cnotd / n_pet_notd )*100
    pct_corr_breed = ( n_match_breed / n_pet_dog )*100
    
    #Prints Calculated Statistics
    print("-----------------------------------------------------------------------------------------------------------------")
    print("\n ** Statistics from calculates_results_stats() function:")
    print("N Images: %2d  N Dog Images: %2d  N NotDog Images: %2d \nPct Corr dog: %5.1f Pct Corr NOTdog: %5.1f  Pct Corr Breed: %5.1f"
          % (results_stats['n_images'], results_stats['n_dogs_img'],
             results_stats['n_notdogs_img'], results_stats['pct_correct_dogs'],
             results_stats['pct_correct_notdogs'],
             results_stats['pct_correct_breed']))
    print("-----------------------------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------------------------")
    print("\n ** Check Statistics - calculated from this function as a check:")
    print("N Images: %2d  N Dog Images: %2d  N NotDog Images: %2d \nPct Corr dog: %5.1f  Pct Corr NOTdog: %5.1f  Pct Corr Breed: %5.1f"
          % (n_images, n_pet_dog, n_pet_notd, pct_corr_dog, pct_corr_notdog,
             pct_corr_breed))
    print("-----------------------------------------------------------------------------------------------------------------")