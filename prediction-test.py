# Prediction tests # 
import pandas as pd
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
    for i in range(len(df.index)):
        if labels[i] == 0:
            label0.append(df.index[i])
        elif labels[i] == 1:
            label1.append(df.index[i])
        elif labels[i] == 2:
            label2.append(df.index[i])
        else:
            print('Error! Too many clusters.')
        
    return label0, label1, label2
        
    
def kmeans(df,df_data):
    ## creating K-means functionS
    kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=300, tol=0.0001, precompute_distances='auto', random_state=None, copy_x=True, n_jobs=None, algorithm='auto')
    
    kmeans = kmeans.fit(df)
    clusters = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    label0, label1, label2 = cluster_labels(labels,df) 
    
#    # Print the cluster centers and labels
#    print('Cluster Centers')
#    print(kmeans.cluster_centers_)
#    print('\n')
#    print('Labels')
#    print(kmeans.labels_)
#    print('\n')
#    # Print meters in each cluster
#    print('The labeled clusters are: ')
#    print(label0)
#    print(label1)
#    print(label2)
    
    plot_labels = ['mean', 'std', 'min', '25%', '50%', '75%', 'max']
    
    plt.plot(plot_labels, clusters[0], 'b',linewidth=0.4,label='First Cluster')
    plt.plot(plot_labels, clusters[1], 'r',linewidth=0.4,label='Second Cluster')
    plt.plot(plot_labels, clusters[2], 'g',linewidth=0.4,label='Third Cluster')
    plt.title('Cluster differentiation')
    plt.xlabel("Statistics factor")
    plt.ylabel("Value")
    plt.legend(loc="upper left")
    plt.show()    
    
    #### divide into cluster data ####
    cluster0 = get_cluster_data(label0,df_data)
    cluster1 = get_cluster_data(label1,df_data)
    cluster2 = get_cluster_data(label2,df_data)
    
    return cluster0, cluster1, cluster2

def get_cluster_data(labels,df):
    df = df.groupby('meter_no')
    df_cluster = pd.DataFrame()
    for meter in labels:
        df_meter = df.get_group(meter)
        df_cluster = df_cluster.append(df_meter)
    return df_cluster




###########################################################################
def main():
    #df_virksomhed = make_some_timeseries('../3011_Virksomhed_ny.csv')
    #df_forbruger = make_some_timeseries('../3011_Forbruger_ny.csv')
    
    ## Print the datasets
    #print(df_virksomhed)
    #print('\n')
    #print(df_forbruger)
    #print('\n')
    
    ## Find simple stats from dataset ## 
    df_virk_stats = describe(df_virksomhed)
    df_forb_stats = describe(df_forbruger)
    
    
    print('K-means for Virksomhed:')
    virk_cluster0, virk_cluster1, virk_cluster2 = kmeans(df_virk_stats,df_virksomhed)
    
    print('\n')
    print('K-means for Forbruger:')
    forb_cluster0, forb_cluster1, forb_cluster2 = kmeans(df_forb_stats,df_forbruger)

    print('\n')
    print('The virksomhed clusters are:') # printing the beginning of each meter
    print(virk_cluster0.groupby('meter_no').head())
    print('\n')
    print(virk_cluster1.groupby('meter_no').head())
    print('\n')
    print(virk_cluster2.groupby('meter_no').head())
    print('\n')
    
    
    
main()