# Feature engineering for credit utilization metrics

class UtilizationFeatures:
    def __init__(self, df):
        self.df = df

    def credit_utilization_ratio(self):
        """Compute revolving balance ÷ credit limit."""
        pass

    def revolving_vs_installment_mix(self):
        """Compute % of credit in revolvers vs. term loans."""
        pass 