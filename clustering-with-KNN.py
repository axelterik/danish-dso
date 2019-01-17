# Prediction tests # 
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def make_some_timeseries(file): ## import dataset
    # Read file and create a time series object
    dateparse = lambda dates: pd.datetime.strptime(dates, '%d-%m-%Y %H:%M')
    df = pd.read_csv(file, sep=',', na_values=".",
            parse_dates=['datetime'],
            index_col= ['datetime'],
            date_parser=dateparse)
    df.index = pd.to_datetime(df.index, utc=True)
    #print(df)
    df = df.fillna('Inget',axis = 1) # putting a string at the empty places to be able to refer to it
    #print(df)
    return df

def describe(df_object): #### use this for statistics
    print("\n")
    print("Showing basic statistics.")
    file = open("../meter_id.txt","r")
    file = file.read().strip().split("\n")
    df_object = df_object.groupby('meter_no')
    df_stats = pd.DataFrame()
    for meter in file:
        meter = int(meter)
        try:
            df = df_object.get_group(meter)
            df_describe = df.describe()
            #print(df_describe)
            #print(df_describe['energyact_pos']['mean'])
            new_stats = pd.DataFrame(data = {'mean': df_describe['energyact_pos']['mean'],
                                      'std': df_describe['energyact_pos']['std'],
                                      'min': df_describe['energyact_pos']['min'], 
                                      '25%': df_describe['energyact_pos']['25%'],
                                      '50%': df_describe['energyact_pos']['50%'],
                                      '75%': df_describe['energyact_pos']['75%'],
                                      'max': df_describe['energyact_pos']['max']
                                      }, index=[meter])
            df_stats = df_stats.append(new_stats)
        except:
            continue
    print(df_stats) 
    return df_stats
    
def cluster_labels(labels,df):
    label0 = []
    label1 = []
    label2 = []
    labellist = []
    
    #for i in labels:
        
    
    for i in range(len(df.index)):
        labels[i]
        
        if labels[i] == 0:
            label0.append(df.index[i])
        elif labels[i] == 1:
            label1.append(df.index[i])
        elif labels[i] == 2:
            label2.append(df.index[i])
        else:
            print('Error! Too many clusters.')
        
    return label0, label1, label2
        
    
def kmeans(k,df,df_data):
    ## creating K-means functionS
    kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, tol=0.0001, precompute_distances='auto', random_state=None, copy_x=True, n_jobs=None, algorithm='auto')
    
    kmeans = kmeans.fit(df)
    clusters = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    df['label'] = labels # adds a label column to the df of stats
    
    plot_labels = ['mean', 'std', 'min', '25%', '50%', '75%', 'max']
    
    for cluster in clusters: 
        #cluster = int(cluster)
        plt.plot(plot_labels, cluster, linewidth=0.4) #, label='Cluster %s' % (clusters.item(cluster)))
    #plt.plot(plot_labels, clusters[1], 'r',linewidth=0.4,label='Second Cluster')
    #plt.plot(plot_labels, clusters[2], 'g',linewidth=0.4,label='Third Cluster')
    plt.title('Cluster differentiation')
    plt.xlabel("Statistics factor")
    plt.ylabel("Value")
    plt.legend(loc="upper left")
    plt.show()    
    
    #### divide into cluster data ####
    df_cluster = pd.DataFrame()
    for cluster in range(k):
        #df_cluster.append(get_cluster_data(label.get_group(cluster),df_data))
        df_cluster = df_cluster.append(get_cluster_data(k,df,df_data)) # ineffective to send the whole matrix
        
    return df_cluster 

def get_cluster_data(k,labels,df): # puts the label into the df at the right meter
    df = df.groupby('meter_no')
    df_cluster = pd.DataFrame()
    labels = labels.groupby('label')
    for cluster in range(k):
        label_df = labels.get_group(cluster)
        for meter in label_df.index:
            df_meter = df.get_group(meter)
            df_meter['label'] = cluster
            df_cluster = df_cluster.append(df_meter)
    return df_cluster

def cluster_mean(df):
    
#    df = df.groupby('meter_no')
#    for meter in df:
#        meter_no = df.get_group(meter)
#    
#    df = df.groupby(df.index)
#    new_df = pd.DataFrame()
    
    mean_meter = pd.DataFrame()
    for date in df.index:
        energyact_pos = np.mean(df['energyact_pos'])
        energyact_neg = np.mean(df['energyact_neg'])
        energyreact_pos = np.mean(df['energyreact_pos'])
        energyreact_neg = np.mean(df['energyreact_neg'])
        mean_meter = {'date': date,'energyact_pos': energyact_pos, 'energyact_neg': energyact_neg,
                      'energyreact_pos': energyreact_pos, 'energyreact_neg': energyreact_neg}
        mean_meter.index = ['date']
        
        print(mean_meter)
    return mean_meter
#    for date in df:
#        for column in date:
#            energyact_pos = np.mean(df['energyact_pos'])
#            energyact_neg = np.mean(df['energyact_neg'])
#            energyreact_pos = np.mean(df['energyreact_pos'])
#            energyreact_neg = np.mean(df['energyreact_neg'])
#            
#            get_mean_from_all
#            new_df = {'energyact_pos': energyact_pos, 'energyact_neg': energyact_neg,
#                      'energyreact_pos': energyreact_pos, 'energyreact_neg': energyreact_neg}
#            
#    set_index = something
            
        
            
        
    
    


###########################################################################
def main():
    df_virksomhed = make_some_timeseries('../3011_Virksomhed_ny.csv')
    df_forbruger = make_some_timeseries('../3011_Forbruger_ny.csv')
    
    ## Print the datasets
    #print(df_virksomhed)
    #print('\n')
    #print(df_forbruger)
    #print('\n')
    
    ## Find simple stats from dataset ## 
    df_virk_stats = describe(df_virksomhed)
    df_forb_stats = describe(df_forbruger)
    
    k_virk = 2
    k_forb = 3
    
    print('K-means for Virksomhed:')
    virk_cluster = kmeans(k_virk,df_virk_stats,df_virksomhed)
    print('\n')
    print('K-means for Forbruger:')
    forb_cluster = kmeans(k_forb,df_forb_stats,df_forbruger)

    print('The virksomhed clusters are:')
    virk_cluster = virk_cluster.groupby('label')
    for label in range(k_virk): # print the clusters
        print("Cluster: " , label)
        virk_cluster0 = virk_cluster.get_group(label)
        cluster_mean(virk_cluster0)
        print(virk_cluster0.groupby('meter_no').head())
        print('\n')
        

    print('The forbruger clusters are:')
    forb_cluster = forb_cluster.groupby('label')
    for label in range(k_forb):
        print("Cluster: " , label)
        forb_cluster0 = forb_cluster.get_group(label)
        cluster_mean(forb_cluster0)
        # create new variables for each group
        
        print(forb_cluster0.groupby('meter_no').head())
        print('\n')
        
 
    
    
    
main()