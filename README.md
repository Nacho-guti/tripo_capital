# Portfolio Optimisation
For a university project, I have been tasked to design an investment plan for an elderly couple.
To accomplish this, I will be carrying out all the data manipulation and optimisation strategies, here, in python.

Disclaimer: I am not a great coder or have never before used git or github, so my terminologies may not be the best.

## Project Structure

 portfolio-optimization/
├── data/
│   ├── raw/                    # Raw Bloomberg data
│   │   ├── equities/
│   │   ├── bonds/
│   │   ├── alternatives/
│   │   ├── cash/
│   │   └── benchmarks/
│   └── processed/              # Cleaned and processed data
├── src/
│   ├── data_collection.py      # Bloomberg data pipeline
│   ├── portfolio_optimizer.py  # Core optimization engine
│   ├── risk_analysis.py        # Risk metrics and VaR
│   ├── benchmark_analysis.py   # Performance attribution
│   ├── backtesting.py         # Historical performance testing
│   └── visualization.py       # Charts and reporting
├── notebooks/
│   ├── data_exploration.ipynb  # Exploratory data analysis
│   └── optimization_analysis.ipynb
├── results/
│   ├── optimal_portfolios/     # Optimization outputs
│   ├── charts/                # Visualizations
│   └── reports/               # Excel reports
├── config/
│   ├── portfolio_constraints.yaml
│   └── benchmarks.yaml
└── README.md

