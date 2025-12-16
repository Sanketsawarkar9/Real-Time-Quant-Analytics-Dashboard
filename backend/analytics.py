import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

def price_stats(series):
    return {
        "mean": float(series.mean()),
        "std": float(series.std())
    }

def hedge_ratio(y, x):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    return model.params[1]

def spread(y, x, beta):
    return y - beta * x

def zscore(series, window=30):
    return (series - series.rolling(window).mean()) / series.rolling(window).std()

def rolling_corr(y, x, window=30):
    return y.rolling(window).corr(x)

def adf_test(series):
    stat, p, *_ = adfuller(series.dropna())
    return {"adf_stat": stat, "p_value": p}
