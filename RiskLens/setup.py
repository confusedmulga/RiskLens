from setuptools import setup, find_packages

setup(
    name='RiskLens',
    version='0.1.0',
    description='Open‑Source Credit‑Risk Analytics with Real‑World, Privacy‑Friendly Signals',
    author='RiskLens Contributors',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'xgboost',
        'lightgbm',
        'shap',
        'streamlit',
        'matplotlib',
        'seaborn',
        'jupyter',
    ],
    include_package_data=True,
    python_requires='>=3.7',
) 