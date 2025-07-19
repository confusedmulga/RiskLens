# Feature engineering for external, non-sensitive data

class ExternalSignalsFeatures:
    def __init__(self, df):
        self.df = df

    def macro_indicators(self):
        """Map local unemployment rate, inflation to customer’s region."""
        pass

    def industry_stress_signals(self):
        """Sector-level default rates for business borrowers."""
        pass 