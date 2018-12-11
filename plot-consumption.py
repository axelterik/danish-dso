import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats


def edit_time_stamp(file,new_file):
    # function used to drop unnecessary columns from dataset and create new file
    data = pd.read_csv(file, sep=',', na_values=".",
        usecols=['meter_no','date','timestamp','energyact_pos','energyact_neg','energyreact_pos','energyreact_neg','generatingunitkind'])
    [['meter_no','date','timestamp','energyact_pos','energyact_neg','energyreact_pos','energyreact_neg','generatingunitkind']]
    data['datetime'] = data['date'] + ' ' + data['timestamp'] # can  only do some columns. Too big. Maybe add address
    #print(data.head())
    data = data.drop(['date','timestamp'],axis=1) # dropping the old date and time
    #print(data.head())
    data.to_csv(new_file, encoding='utf-8', index=False) # creating a new file

def make_some_timeseries(file):
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

def get_mean_hourly(meter,df,value): 
    # takes a matrix with one meter_no
    df_hour = df.groupby('hour')
    df_hour = df.groupby('hour')
    list = []
    for h in range(len(df_hour)):
        gethour = df_hour.get_group(h)
        list.append(gethour[value].mean())
    plt.plot(list,linewidth=0.2,label=meter)
    
def plot_user_hour(df,value): # plots all users on the same graph for mean hourly consumption
    file = open("../meter_id.txt","r")
    file = file.read().strip().split("\n")
    df_object = df.groupby('meter_no')
    for meter in file:
        meter = int(meter)
        try:
            df_meter = df_object.get_group(meter)
            get_mean_hourly(meter,df_meter,value)
        except:
            continue
    plt.title('Meter consumption per hour of the day')
    plt.xlabel("Hour of the day")
    plt.ylabel("kW")
    #plt.legend(loc="upper left")
    plt.show()

def get_mean_from_hour(df,value,label):
    df['weekday'] = df.index.weekday
    df['hour'] = df.index.hour
    df['date'] = df.index.date
    print(df.head())
    df_weekday = df.groupby('weekday')
    #print(df['hour'])
    for d in range(len(df_weekday)):
        list = [] 
        df_hour = df_weekday.get_group(d).groupby('hour')
        for h in range(len(df_hour)):
            gethour = df_hour.get_group(h)
            datehour = gethour.groupby('date')
            datelist = []
#            for date in df['date']:
#                try:
#                    date = str(date)
#                    #date = strftime("%Y-%m-%d")
#                    getdate = datehour.get_group(date)
#                    tot_hour = getdate[value].sum()
#                    datelist.append(tot_hour)    
#                except:
#                    continue
#            list.append(stats.mean(datelist))
            list.append(gethour[value].mean() )
        plt.plot(list,linewidth=0.2,label="day %s" % (d)) 
    plt.title('%s per hour of the day' % (label))
    plt.xlabel("Hour of the day")
    plt.ylabel("kW")
    plt.legend(loc="upper left")
    plt.show()
    
    list = []
    df_hour = df.groupby('hour')
    for h in range(len(df_hour)):
        gethour = df_hour.get_group(h)
        list.append(gethour[value].mean())
    plt.plot(list,linewidth=0.2,label=label)
    plt.title('Forbruger %s per hour of the day' % (label))
    plt.xlabel("Hour of the day")
    plt.ylabel("kW")
    plt.legend(loc="upper left")
    plt.show()
    

    #return(list)

def get_mean_from_day(df,value,label):
    df['day'] = df.index.day
    df['weekday'] = df.index.weekday
    df_day = df.groupby('day')
    df_weekday = df.groupby('weekday')
    listday = []
    listweekday = []
    for h in range(1,len(df_day)+1):
        gethour = df_day.get_group(h)
        listday.append(gethour[value].mean())
    
    for h in range(len(df_weekday)):
        gethour = df_weekday.get_group(h)
        listweekday.append(gethour[value].mean())
    plt.plot(listday,linewidth=0.2,label=label)
    plt.title('%s per day' % (label))
    plt.xlabel("Days")
    plt.ylabel("kW")
    plt.legend(loc="lower left")
    plt.show()
    plt.plot(listweekday,linewidth=0.2,label=label)
    plt.title('%s per day of the week' % (label))
    plt.xlabel("Days")
    plt.ylabel("kW")
    plt.legend(loc="lower left")
    plt.show()
    return(list)

def get_meter(meter,df):
    df = df.groupby('meter_no')
    df_meter = df.get_group(meter)
    return df_meter

def check_zero(df):
    print("Checking for zero values.")
    file = open("../meter_id.txt","r")
    file = file.read().strip().split("\n")
    df_object = df.groupby('meter_no')
    zerolist = []
    zeropower = []
    for meter in file:
        meter = int(meter)
        try:
            df_meter = df_object.get_group(meter)
            sum_actp = sum(df_meter['energyact_pos'])
            sum_actn = sum(df_meter['energyact_neg'])
            sum_reap = sum(df_meter['energyreact_pos'])
            sum_rean = sum(df_meter['energyreact_neg'])
            if sum_actp == 0:
                zeropower.append(meter)
            if sum_actp == sum_actn == sum_reap == sum_rean == 0:
                zerolist.append(meter)
            else:
                continue
        except: 
            continue
    print("These meters are missing values:")
    print(zerolist)
    print("These meters do not consume active power:")
    print(zeropower)
            
        

def statistics(df_object,key): ### not used anymore! 
    print("\n")
    print("Starting statistics.")
    file = open("../meter_id.txt","r")
    file = file.read().strip().split("\n")
    df_object = df_object.groupby('meter_no')
    df_stats = pd.DataFrame()
    for meter in file:
        meter = int(meter)
        try:
            df = df_object.get_group(meter)
            mini = min(df[key])
            maxi = max(df[key])
            mean = stats.mean(df[key])
            var = stats.variance(df[key],mean)
            stdev = stats.stdev(df[key])
            new_stats = pd.DataFrame(data = {'Mean': [mean],
                                      'Min': [mini], 'Max': [maxi],
                                      'Variance': [var], 'St.dev': [stdev]
                                      }, index=[meter])
            df_stats = df_stats.append(new_stats)
        except:
            continue
    return df_stats

def describe(df_object): #### use this for statistics
    print("\n")
    print("Starting statistics.")
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
    
    #return df_describe





# NOTES
### average of day and plot days, single day
### unit is kW and kVAR
### plot all the other energies as well

## make a statistics file, mean value for each customer, min, max, variance, chacarcherise every customers
## for both datasets
## Weka could be used for this, do it for you. Put a file and get back the values
# identify some unique IDs, check location as well, or similarites between different users

### make the code so that it can read different data
### address is important to keep
# ask about data if it takes too long

# identify meters that are consuming differently
##### plot these interesting users! 
    # and the mean without the outliers

# group_by(meterid) och se om det kan köras genom Weka

#### add adress and other columns to the data?

# make plots more visible 
    
##### make sure to sum up within the hours! 
    
## use keras for prediction 

### add proper file directory



###### main script here
import time
start = time.time()
print("Hello World!")


def prepare_data():
    #### Run first to edit the file with hours and dates in the same column
    #edit_time_stamp('3011_Virksomhed.csv','3011_Virksomhed_ny.csv')
    #edit_time_stamp('3011_Forbruger.csv','3011_Forbruger_ny.csv')
    
    #### Reading files into time series dataframes
    df_virksomhed = make_some_timeseries('../3011_Virksomhed_ny.csv')
    df_forbruger = make_some_timeseries('../3011_Forbruger_ny.csv')
#prepare_data()


describe(df_virksomhed)
describe(df_forbruger)


def test_plot():
    #### Plotting companies and ordinary customers
    print('Plotting companies and ordinary customers')
    plt.plot(df_virksomhed['energyact_pos'],linewidth=0.2,label='Energyact_pos Virksomhed')
    plt.plot(df_forbruger['energyact_pos'],linewidth=0.2,label='Energyact_pos Forbruger')
    #plt.plot(df_virksomhed['energyact_neg'],linewidth=0.2,label='Energyact_neg Virksomhed')
    #plt.plot(df_forbruger['energyact_neg'],linewidth=0.2,label='Energyact_neg Forbruger')
    plt.title('Active power for the full dataset')
    plt.xlabel("Time")
    plt.ylabel("kW")
    plt.legend(loc="upper left")
    plt.show()
#test_plot()


#plot_user_hour(df_virksomhed,'energyact_pos')
#plot_user_hour(df_forbruger,'energyact_pos')



def mean_plot():
    ########### Plot the means for hour and month
    print('Plot the means for hour and month')
    print("Plotting mean for Virksomhed negative energy for hour and day")
    get_mean_from_hour(df_virksomhed, 'energyact_neg', 'Mean Power')
    get_mean_from_day(df_virksomhed, 'energyact_neg', 'Mean Power')
    print("Plotting mean for Virksomhed positive energy for hour and day")
    get_mean_from_hour(df_virksomhed, 'energyact_pos', 'Mean Power')
    get_mean_from_day(df_virksomhed, 'energyact_pos', 'Mean Power')
    
    print("Plotting mean for Forbruger negative energy for hour and day")
    get_mean_from_hour(df_forbruger, 'energyact_neg', 'Mean Power')
    get_mean_from_day(df_forbruger, 'energyact_neg', 'Mean Power')
    print("Plotting mean for Forbruger positive energy for hour and day")
    get_mean_from_hour(df_forbruger, 'energyact_pos', 'Mean Power')
    get_mean_from_day(df_forbruger, 'energyact_pos', 'Mean Power')
#mean_plot()

#print(check_zero(df_virksomhed))
#print(check_zero(df_forbruger)) # one meter has no values

def create_stats_companies():
    ####### Create the stats for companies for each value
    stats_virksomhed_actpos = statistics(df_virksomhed,'energyact_pos')
    print("Positive active power stats for companies.")
    print(stats_virksomhed_actpos.to_string())
    stats_virksomhed_actneg = statistics(df_virksomhed,'energyact_neg')
    print("Negative active power stats for companies.")
    print(stats_virksomhed_actneg.to_string())
    stats_virksomhed_repos = statistics(df_virksomhed,'energyreact_pos')
    print("Positive reactive power stats for companies.")
    print(stats_virksomhed_repos.to_string())
    stats_virksomhed_reneg = statistics(df_virksomhed,'energyreact_neg')
    print("Negative reactive power stats for companies.")
    print(stats_virksomhed_reneg.to_string())

def create_stats_customers():
    ####### Create the stats for customers for each value
    print('Create the stats for customers for each value')
    stats_forbruger_actpos = statistics(df_forbruger,'energyact_pos')
    print("Positive active power stats for customers.")
    print(stats_forbruger_actpos.to_string())
    stats_forbruger_actneg = statistics(df_forbruger,'energyact_neg')
    print("Negative active power stats for customers.")
    print(stats_forbruger_actneg)
    stats_forbruger_repos = statistics(df_forbruger,'energyreact_pos')
    print("Positive reactive power stats for customers.")
    print(stats_forbruger_repos)
    stats_forbruger_reneg = statistics(df_forbruger,'energyreact_neg')
    print("Negative reactive power stats for customers.")
    print(stats_forbruger_reneg)


def make_big_df(df1,df2,df3,df4,filename):
    df = pd.DataFrame()
    df['Aposmean'] = df1['Mean']
    df['Aposmin'] = df1['Min']
    df['Aposmax'] = df1['Max']
    df['Aposvar'] = df1['Variance']
    df['Aposdev'] = df1['St.dev']
    df['Anegmean'] = df2['Mean']
    df['Anegmin'] = df2['Min']
    df['Anegmax'] = df2['Max']
    df['Anegvar'] = df2['Variance']
    df['Anegdev'] = df2['St.dev']
    df['Rposmean'] = df3['Mean']
    df['Rposmin'] = df3['Min']
    df['Rposmax'] = df3['Max']
    df['Rposvar'] = df3['Variance']
    df['Rposdev'] = df3['St.dev'] 
    df['Rnegmean'] = df4['Mean']
    df['Rnegmin'] = df4['Min']
    df['Rnegmax'] = df4['Max']
    df['Rnegvar'] = df4['Variance']
    df['Rnegdev'] = df4['St.dev']
       #,'Aposmax','Aposmin','Aposvar','Aposdev'] = df1['Mean','Min','Max','Variance','St.dev']
    print(df.head())
    df = df.round(3)
    print(df.head())
    df.to_csv(filename, encoding='utf-8', index=True)





#meter5650 = get_meter(19565650,df_forbruger)
#print("Printing power from meter 19565650")
#print(meter5650['energyact_pos'])


########### Sort values on maximum
#print('Sort values on maximum')
#stats_forbruger_actpos.sort_values('Max', axis=0, ascending=True,inplace=True)
#print("Sorted values on maximum power consumption for customers")
##print(statistics_forbruger.to_string())
#stats_virksomhed_actpos.sort_values('Max', axis=0, ascending=True,inplace=True)
#print("Sorted values on maximum power consumption for companies")
#print(stats_virksomhed_actpos.to_string())
#
######## Creating different columns for different types of local generation
#print('Creating different columns for different types of local generation')
#df_virksomhed_gentype = df_virksomhed['generatingunitkind']
#df_virksomhed_gentype = df_virksomhed.groupby('generatingunitkind')
#df_virksomhed_sol = df_virksomhed_gentype.get_group('Solceller')
#df_virksomhed_none = df_virksomhed_gentype.get_group('Inget')

##### checking difference in negative energy
#print('Checking difference in negative energy:')
#get_mean_from_hour(df_virksomhed_sol, 'energyact_neg', 'Mean Power')
#get_mean_from_hour(df_virksomhed_none, 'energyact_neg', 'Mean Power')

### check the same for reactive power, see if solar producers have more or less reactive

#df_meterid = df_virksomhed.groupby('meter_no')
#print("These are the meter ID's: ")
#print(df_meterid.head(1))


#make_big_df(stats_virksomhed_actpos,stats_virksomhed_actneg,stats_virksomhed_repos,stats_virksomhed_reneg,'../virksomhed_stats_data.csv')
#make_big_df(stats_forbruger_actpos,stats_forbruger_actneg,stats_forbruger_repos,stats_forbruger_reneg,'../forbruger_stats_data.csv')


#df_meterid.get_group(19547874).to_csv('../meter_id.csv', encoding='utf-8', index=True)

########### Use if forbruger has solar panels or to check the types of generation
#df_forbruger_gentype = df_forbruger['generatingunitkind']
#df_forbruger_gentype = df_forbruger.groupby('generatingunitkind')
#df_forbruger_sol = df_forbruger_gentype.get_group('Solceller')
#df_forbruger_none = df_forbruger_gentype.get_group('Inget')


#### Checking what different typs of generation there are in the datasets
#print('Virksomhet grupper')
#print(df_virksomhed_gentype.head())
#print('\n')
#print('Forbruger grupper')
#print(df_forbruger_gentype.head())

#### Plotting company customer with and without solar power.
#plt.plot(df_virksomhed_sol['energyact_pos'],linewidth=0.2, color = 'r',label='With solar')
#plt.plot(df_virksomhed_none['energyact_pos'],linewidth=0.2,color = 'b',label='No solar')
#plt.title('Companies')
#plt.xlabel("Time")
#plt.ylabel("kW")
#plt.legend(loc="upper left")
#plt.show()
#### Plotting ordinary customers and companies with solar
#plt.plot(df_forbruger_none['energyact_pos'],linewidth=0.2,color = 'm',label='Customer')
#plt.plot(df_virksomhed_sol['energyact_pos'],linewidth=0.2,color = 'b',label='Company with solar')
#plt.title('Companies and Customers')
#plt.xlabel("Time")
#plt.ylabel("kW")
#plt.legend(loc="upper left")
#plt.show()




end = time.time()
print('Time elaps was: ' , end - start , ' seconds.')
