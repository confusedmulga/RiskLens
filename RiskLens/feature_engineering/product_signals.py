# Feature engineering for product and relationship signals

class ProductSignalsFeatures:
    def __init__(self, df):
        self.df = df

    def product_tenure(self):
        """Compute age of the loan/account."""
        pass

    def product_diversity(self):
        """Compute # of different products held."""
        pass

    def recent_credit_inquiries(self):
        """Compute # of credit inquiries in last 6-12 months."""
        pass 