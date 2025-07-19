# Feature engineering for payment behavior (DPD, payment consistency, etc.)

class PaymentBehaviorFeatures:
    def __init__(self, df):
        self.df = df

    def compute_dpd_buckets(self):
        """Compute 30-, 60-, 90-day DPD buckets."""
        pass

    def payment_consistency(self):
        """Compute std. dev. of payment dates vs. due dates."""
        pass 