import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle as p
import test_model

"""      
        ***Module Description***

        Call the mighty_plot function. It has to get a dictionary with the model results (at the moment called 'output').
        Further the plot-function needs a 'plotword', which has to be a string, and a list of strings (list is called 'keywords').
        You can use the following plotwords: time_course, sequence_dependence, correlation, species_mean or mass_distribution.
        'keywords' has to be a list of strings! The strings inside 'keywords' define which species are plotted.
        'keywords': You can put each model species name (like MRNA_11) as a string in 'keywords'.
                    If you want to plot a group of species, like all mRNA you can just put 'MRNA' in 'keywords'.
                    With 'keywords' = [''] you call all model species.
        
        time_course: If you choose time_course as your 'plotword' the visualization module plots a timecourse for each string in 'keywords'.
                     If 'Protein' is a string in 'keywords' you plot timecourses (number of proteins over time) for all Proteins.
                     To obtain timecourses for all model species it is sufficient to call the function with 'keywords' = ['']. 

        sequence_dependence: Plots the concentrations of model species at the latest timepoint over its sequence length.
                             Here you have to be a little bit careful. 'keywords' has to be a list with a single string inside. 
                             Otherwise it would not work. (Right : 'keywords' = ['MRNA'], Wrong: 'keywords' = ['MRNA', 'Protein'])

        correlation: Gives a correlation heatmap between all species defined by 'keywords'.

        species_mean: For each string in 'keywords' one gets a mean timecourse with standard deviation. 
                      A senseful keyword (a string in 'keywords') would be 'Protein', which gives the mean number of proteins at each timepoint.
                      It doesn't make sense to use 'Protein_11' as a keyword, because one would get the mean and standard deviation of one species.

        mass_distribution: Gives mass distribution (for species in 'keywords') at last timepoint of simulation as pie-chart. 

"""

output = {}
with open('output.p', 'rb') as f:
    output = p.load(f)

def dict_to_dframe(res_dict):
    """ Takes result dict and return a DataFrame with timecourses for each model species."""
    s = pd.DataFrame()
    key_list = []

    for i, key in enumerate(res_dict):
        s[i] = pd.DataFrame(res_dict[key]['timecourse'], columns = [key])
        key_list.append(key)

    s.columns = key_list
    return s

def timecourse_by_column(res_dict, keywords):
    """ Takes result dictionary and list of keywords(strings), which define the model species which should be plottet.
        e.g.: keywords = ['MRNA', 'Protein'], stores timecourses of all mRNAs and all Proteins in a DataFrame, which is returned.
    """
    r = dict_to_dframe(res_dict)
    wished_cols = []
    for kw in keywords:
        wished_cols += [x for x in r.columns if kw in x]

    r_mod = r[wished_cols]
    return r_mod
    

def seq_dependence(res_dict, keyword):
    """ Takes result dictionary and returns species sequence lengths as well as each final concentration. """
    seq_lengths = []
    last_conc = []
    for key in res_dict.keys():
        if keyword in key:
            seq_lengths.append(len(res_dict[key]['sequence']))
            last_conc.append(res_dict[key]['timecourse'][-1])
        else:
            continue
    return seq_lengths, last_conc



def mean_timecourse(res_dict, keywords):
    """ Calculates mean timecourse with standard deviation for each element in keywords.
        e.g.: If 'mrna' is an element keywords mean_timecourse returns mean timecourse for all mRNAs + std. """
    all_mean_time_courses = {}
    all_std_time_courses = {}
    for kw in keywords:
        all_mean_time_courses[kw] = timecourse_by_column(res_dict, [kw]).mean(axis = 1)
        all_std_time_courses[kw] = timecourse_by_column(res_dict, [kw]).std(axis = 1)
    all_mean_df = pd.DataFrame(all_mean_time_courses)
    all_std_df = pd.DataFrame(all_std_time_courses)
    return all_mean_df, all_std_df  
    #return all_mean_time_courses
    
def mean_species_mass(res_dict, keywords):
    """ Takes model dictionary and 'keywords', returns mean mass of each string in 'keywords' as dict."""
    mass_dict = {}
    kw_count = {}
    mean_mass_dict = {}
    for kw in keywords:
        mass_dict[kw] = 0
        kw_count[kw] = 0
        for key in res_dict.keys():
            if kw in key:
                mass_dict[kw] += res_dict[key]['mass']
                kw_count[kw] += 1
    
    #for key in mass_dict.keys():
    #    mean_mass_dict[key] = 0 
    #    mean_mass_dict[key] = mean_mass_dict[key]/kw_count[key]
    
    return mass_dict



def mighty_plot(res_dict, plotword, keywords):
    """ Plots dependent on plotword and keywords. See module description. """
     
    if plotword == 'time_course':
        p = timecourse_by_column(res_dict, keywords) #p is DataFrame
        p.plot(linewidth = 1.5)
        plt.legend(loc='best',bbox_to_anchor=(1, 1), fontsize = 7, ncol = 3)
        plt.xlabel('time[s]')
        plt.ylabel('number of molecules')
        plt.title('Timecourses')
        plt.show()
    elif plotword == 'sequence_dependence':
        if len(keywords) > 1:
            print "If you want to plot sequence length dependent concentrations, 'keywords' has to have only one string."
        else:
            x,y = seq_dependence(res_dict, keywords[0])
            plt.scatter(x,y)
            plt.xlabel('Sequence length[nt;aa]')
            plt.ylabel('Number of molecules at last timepoint')
            plt.title('Sequence dependence')
            plt.show()
    elif plotword == 'correlation':
        c_df = timecourse_by_column(res_dict,keywords)
        c = c_df.corr()
        plt.pcolor(c, cmap = 'Blues')
        plt.yticks(np.arange(0.5,len(c.index),1), c.index, fontsize = 7)
        plt.xticks(np.arange(0.5,len(c.columns),1), c.columns, rotation = 'vertical', fontsize = 7)
        plt.title('Correlation heatmap')
        plt.colorbar()
        plt.show()
    elif plotword == 'species_mean':
        a, b = mean_timecourse(res_dict,keywords) #be careful with keywords
        a.plot(subplots=False, yerr=b, cmap = 'brg') 
        plt.xlabel('time[s]')
        plt.ylabel('number of molecules')
        plt.title('Means of Moleculeclass')
        plt.show()
    elif plotword == 'mass_distribution':
        mass_dict = mean_species_mass(res_dict,keywords)
        fig = plt.figure(1, figsize = [8,8])
        colors = ['sandybrown', 'yellowgreen', 'lightskyblue', 'lightcoral', 'seagreen', 'lightblue', 'violet', 'dodgerblue', 'salmon', 'magenta', 'crimson']
        plt.pie(mass_dict.values(), labels =mass_dict.keys(), shadow=True, colors = colors)
        plt.title('Mass distribution')
        plt.show()




#mighty_plot(output, 'mass_distribution', ['Protein','MRNA', 'DNA'])

