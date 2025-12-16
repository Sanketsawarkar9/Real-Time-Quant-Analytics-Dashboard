def zscore_alert(z, threshold):
    if z.dropna().empty:
        return None
    if abs(z.iloc[-1]) > threshold:
        return f"Z-score crossed ±{threshold}"
    return None
