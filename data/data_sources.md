# Data Sources

## 1. USD/TZS Exchange Rate
- Source: fawazahmed0 Currency API
- URL: https://latest.currency-api.pages.dev/v1/currencies/usd.json
- Fallback: https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json
- Cost: Free, no API key
- Frequency: Daily
- Historical: Yes (by date in URL)

## 2. US Interest Rate (Federal Funds Rate)
- Source: FRED
- Series ID: FEDFUNDS
- Cost: Free, API key required (get at fred.stlouisfed.org)
- Frequency: Monthly

## 3. Oil Prices (WTI Crude)
- Source: FRED
- Series ID: DCOILWTICO
- Cost: Free, API key required
- Frequency: Daily

## 4. Gold Prices
- Source: FRED
- Series ID: GOLDAMGBD228NLBM
- Cost: Free, API key required
- Frequency: Daily

## 5. World Bank Indicators (Tanzania)
- Base URL: https://api.worldbank.org/v2/country/TZ/indicator/
- Cost: Free, no API key
- Frequency: Annual

Indicators:
- Inflation: FP.CPI.TOTL.ZG
- Foreign Reserves: FI.RES.TOTL.CD
- Trade Balance: BN.CAB.XOKA.CD
- Remittances: BX.TRF.PWKR.CD.DT
- Tourism receipts: ST.INT.RCPT.CD