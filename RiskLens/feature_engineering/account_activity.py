# Feature engineering for account activity metrics

class AccountActivityFeatures:
    def __init__(self, df):
        self.df = df

    def transaction_velocity(self):
        """Compute # of transactions per week/month."""
        pass

    def average_transaction_size(self):
        """Compute median vs. mean transaction size to spot outliers."""
        pass

    def balance_fluctuation(self):
        """Compute rolling volatility of daily balances."""
        pass 