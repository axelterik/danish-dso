import pandas as pd


def arima_function(df,column,p,d,q):
    from statsmodels.tsa.arima_model import ARIMA
    from pandas.plotting import autocorrelation_plot
    from matplotlib import pyplot
    
    series = df[column]
    #autocorrelation_plot(series) #### very unstable, should be closer examined
    #pyplot.show()
    # pd.read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
    # fit model
    model = ARIMA(series, order=(p,d,q))
    model_fit = model.fit(disp=0)
    print(model_fit.summary())
    # plot residual errors
    residuals = pd.DataFrame(model_fit.resid)
    residuals.plot()
    pyplot.show()
    residuals.plot(kind='kde')
    pyplot.show()
    print(residuals.describe())

file = 'cluster 1.csv'
df = pd.read_csv(file, sep=',', na_values=".") # make sure to add datetime

print(df.head())
df = df.drop(df.index[1000:],axis=0)


arima_function(df,'energyact_pos',24,1,0)