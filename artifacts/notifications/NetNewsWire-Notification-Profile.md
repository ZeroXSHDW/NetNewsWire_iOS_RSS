# NetNewsWire notification and profile matrix

Generated from `feed-manifest.json`; regenerate with `make generate` after manifest changes.

OPML imports carry the feed structure but do not reliably carry NetNewsWire notification settings. Apply the policy below manually after import.

## Profile summary

| Profile | Recommended | Feeds | On | Optional | Optional French | Off |
|---|---|---:|---:|---:|---:|---:|
| Master | No | 536 | 4 | 12 | 1 | 519 |
| iPhone Lite | No | 118 | 4 | 9 | 1 | 104 |
| iPhone Air | Yes | 125 | 4 | 9 | 1 | 111 |

## Policy meanings

| Policy | Meaning |
|---|---|
| On | Enable immediate notifications for urgent, high-signal alerts. |
| Optional | Keep off by default; enable when the topic is actively relevant. |
| Optional French | Same as Optional; translate/summarize in the daily digest when useful. |
| Off | Do not interrupt; include in the daily Apple Intelligence digest. |

## Per-feed matrix

| Section | Folder | Feed | Master | iPhone Lite | iPhone Air | Notification policy | Signal type |
|---|---|---|---|---|---|---|---|
| Finance | 01 — Core — Market & Trading | Nasdaq Trader — Trade Halts | Yes | Yes | Yes | **On** | alert |
| Finance | 01 — Core — Market & Trading | Nasdaq Trader — Equity Trader Alerts | Yes | Yes | Yes | Off; summarize | regulatory/event |
| Finance | 01 — Core — Market & Trading | Euronext — Market Status | Yes | Yes | Yes | Off; summarize | market-operations-alert |
| Finance | 01 — Core — Market & Trading | Euronext Athens — Market Notices | Yes | No | No | Off; summarize | exchange-notices |
| Finance | 01 — Core — Market & Trading | BBC — Business | Yes | No | No | Off; summarize | context |
| Finance | 01 — Core — Market & Trading | Bloomberg — Markets | Yes | No | Yes | Off; summarize | market |
| Finance | 01 — Core — Market & Trading | Financial Times — Markets | Yes | No | No | Off; summarize | market/research |
| Finance | 01 — Core — Market & Trading | MarketWatch — Top Stories | Yes | No | No | Off; summarize | market |
| Finance | 01 — Core — Market & Trading | RTÉ — Business | Yes | No | No | Off; summarize | context |
| Finance | 01 — Core — Market & Trading | The Wall Street Journal — Markets | Yes | No | No | Off; summarize | market |
| Finance | 02 — Core — Official & Macro | Central Bank of Ireland — News | Yes | Yes | Yes | Optional on | policy/regulatory |
| Finance | 02 — Core — Official & Macro | European Central Bank — Press | Yes | Yes | Yes | Optional on | policy/event |
| Finance | 02 — Core — Official & Macro | European Banking Authority — News | Yes | Yes | Yes | Off; summarize | regulatory/policy |
| Finance | 02 — Core — Official & Macro | European Systemic Risk Board — Press | Yes | Yes | Yes | Off; summarize | macroprudential/research |
| Finance | 02 — Core — Official & Macro | European Systemic Risk Board — Publications & Research | Yes | Yes | Yes | Off; summarize | macroprudential/research |
| Finance | 02 — Core — Official & Macro | European Systemic Risk Board — Policy Warnings & Advice | Yes | Yes | Yes | Off; summarize | macroprudential/policy |
| Finance | 02 — Core — Official & Macro | European Systemic Risk Board — National Macroprudential Notifications | Yes | No | No | Off; summarize | macroprudential/national-notifications |
| Finance | 02 — Core — Official & Macro | European Securities and Markets Authority — News | Yes | Yes | Yes | Off; summarize | regulatory/market |
| Finance | 02 — Core — Official & Macro | EIOPA — News | Yes | Yes | Yes | Off; summarize | insurance-pensions-regulation |
| Finance | 02 — Core — Official & Macro | AFM — Sector News (Dutch) | Yes | No | No | Off; summarize | securities-conduct/market-regulation |
| Finance | 02 — Core — Official & Macro | AMLA — News & Press | Yes | Yes | Yes | Off; summarize | aml/enforcement/regulatory |
| Finance | 02 — Core — Official & Macro | European Public Prosecutor’s Office — News | Yes | Yes | Yes | Off; summarize | financial-crime/enforcement |
| Finance | 02 — Core — Official & Macro | European Anti-Fraud Office (OLAF) — News | Yes | No | No | Off; summarize | anti-fraud/enforcement |
| Finance | 02 — Core — Official & Macro | Eurojust — Press Releases & News | Yes | No | No | Off; summarize | organised-crime/financial-crime |
| Finance | 02 — Core — Official & Macro | European Commission — Competition Policy News | Yes | Yes | Yes | Off; summarize | competition/antitrust/state-aid |
| Finance | 02 — Core — Official & Macro | European Commission — Taxation & Customs News | Yes | Yes | Yes | Off; summarize | tax-customs/policy |
| Finance | 02 — Core — Official & Macro | European Commission — Financial Services News (FISMA) | Yes | Yes | Yes | Off; summarize | financial-regulation/policy |
| Finance | 02 — Core — Official & Macro | European Commission — Energy News | Yes | No | No | Off; summarize | energy-policy/security |
| Finance | 02 — Core — Official & Macro | European Commission — Trade & Economic Security News | Yes | No | No | Off; summarize | trade/economic-security |
| Finance | 02 — Core — Official & Macro | European Commission — Mobility & Transport News | Yes | No | No | Off; summarize | transport/infrastructure-policy |
| Finance | 02 — Core — Official & Macro | AMF — News | Yes | No | No | Off; summarize | regulatory/news |
| Finance | 02 — Core — Official & Macro | Banca d’Italia — News (English) | Yes | Yes | Yes | Off; summarize | central-bank-news |
| Finance | 02 — Core — Official & Macro | DNB — General News | Yes | No | No | Off; summarize | central-bank-news |
| Finance | 02 — Core — Official & Macro | DNB — Supervision News | Yes | Yes | Yes | Off; summarize | banking-supervision/regulatory |
| Finance | 02 — Core — Official & Macro | DNB — Statistical News | Yes | Yes | Yes | Off; summarize | central-bank-data |
| Finance | 02 — Core — Official & Macro | Bank of England — News | Yes | Yes | Yes | Optional on | policy/event |
| Finance | 02 — Core — Official & Macro | HM Treasury — News & Communications | Yes | Yes | Yes | Off; summarize | policy/event |
| Finance | 02 — Core — Official & Macro | UK Department for Work and Pensions — Activity on GOV.UK | Yes | No | No | Off; summarize | pensions-labour/financial-resilience |
| Finance | 02 — Core — Official & Macro | Ofgem — Activity on GOV.UK | Yes | No | No | Off; summarize | energy-market-regulation/consumer-protection |
| Finance | 02 — Core — Official & Macro | Ofcom — Activity on GOV.UK | Yes | No | No | Off; summarize | communications-regulation/digital-resilience |
| Finance | 02 — Core — Official & Macro | Office for Budget Responsibility — News | Yes | Yes | Yes | Off; summarize | fiscal-policy/official-analysis |
| Finance | 02 — Core — Official & Macro | UK Export Finance — Activity on GOV.UK | Yes | No | No | Off; summarize | export-finance/trade-security |
| Finance | 02 — Core — Official & Macro | HM Revenue & Customs — Activity on GOV.UK | Yes | Yes | Yes | Off; summarize | tax-customs/official-news |
| Finance | 02 — Core — Official & Macro | Serious Fraud Office — Activity on GOV.UK | Yes | Yes | Yes | Off; summarize | financial-crime/official-news |
| Finance | 02 — Core — Official & Macro | Insolvency Service — Activity on GOV.UK | Yes | Yes | Yes | Off; summarize | insolvency/financial-crime |
| Finance | 02 — Core — Official & Macro | Federal Reserve — Monetary Policy | Yes | Yes | Yes | Optional on | policy/event |
| Finance | 02 — Core — Official & Macro | Federal Reserve — Other Announcements | Yes | Yes | Yes | Off; summarize | central-bank/official-announcement |
| Finance | 02 — Core — Official & Macro | SEC — Press Releases | Yes | Yes | Yes | Optional on | regulatory/event |
| Finance | 02 — Core — Official & Macro | CFTC — General Press Releases | Yes | Yes | Yes | Off; summarize | regulatory/event |
| Finance | 02 — Core — Official & Macro | CFTC — Enforcement | Yes | Yes | Yes | Optional on | enforcement/regulatory |
| Finance | 02 — Core — Official & Macro | CFTC — Speeches and Testimony | Yes | No | No | Off; summarize | derivatives-policy/speeches-testimony |
| Finance | 02 — Core — Official & Macro | Federal Trade Commission — Consumer Protection Press Releases | Yes | Yes | Yes | Off; summarize | consumer-protection/enforcement |
| Finance | 02 — Core — Official & Macro | Federal Trade Commission — Competition Press Releases | Yes | Yes | Yes | Off; summarize | competition/antitrust |
| Finance | 02 — Core — Official & Macro | CFPB — Newsroom | Yes | Yes | Yes | Off; summarize | consumer-finance/regulatory |
| Finance | 02 — Core — Official & Macro | Competition and Markets Authority — Activity on GOV.UK | Yes | Yes | Yes | Off; summarize | competition/consumer-policy |
| Finance | 02 — Core — Official & Macro | DOJ Antitrust Division — Press Releases | Yes | Yes | Yes | Off; summarize | antitrust/enforcement |
| Finance | 02 — Core — Official & Macro | DOJ National Security Division — News | Yes | No | No | Off; summarize | national-security/enforcement |
| Finance | 02 — Core — Official & Macro | ECB — Market Operations | Yes | Yes | Yes | Off; summarize | market-data/event |
| Finance | 02 — Core — Official & Macro | Federal Reserve — Speeches | Yes | Yes | Yes | Off; summarize | policy/research |
| Finance | 02 — Core — Official & Macro | Bank of Korea — Press Releases | Yes | No | No | Off; summarize | central-bank/policy |
| Finance | 02 — Core — Official & Macro | Bank of Korea — Monetary Policy Decisions | Yes | No | No | Off; summarize | central-bank/monetary-policy |
| Finance | 02 — Core — Official & Macro | Bangko Sentral ng Pilipinas — Media Releases | Yes | No | No | Off; summarize | central-bank/press |
| Finance | 02 — Core — Official & Macro | Bangko Sentral ng Pilipinas — Issuances | Yes | No | No | Off; summarize | central-bank/regulatory |
| Finance | 02 — Core — Official & Macro | Bangko Sentral ng Pilipinas — Public Advisories | Yes | No | No | Off; summarize | central-bank/advisory |
| Finance | 02 — Core — Official & Macro | ECB Banking Supervision — Press | Yes | Yes | Yes | Off; summarize | banking-supervision/regulatory |
| Finance | 02 — Core — Official & Macro | Financial Stability Board — News | Yes | Yes | Yes | Off; summarize | financial-stability/regulatory |
| Finance | 02 — Core — Official & Macro | Single Resolution Board — News | Yes | Yes | Yes | Off; summarize | bank-resolution/regulatory |
| Finance | 02 — Core — Official & Macro | European Investment Fund — News | Yes | Yes | Yes | Off; summarize | development-finance/SME |
| Finance | 02 — Core — Official & Macro | Federal Reserve — Banking & Consumer Regulatory Policy | Yes | Yes | Yes | Off; summarize | banking-regulation/policy |
| Finance | 02 — Core — Official & Macro | Federal Reserve — Enforcement Actions | Yes | Yes | Yes | Optional on | enforcement/banking-regulation |
| Finance | 02 — Core — Official & Macro | Federal Reserve — Banking Applications | Yes | Yes | Yes | Off; summarize | banking-regulation/decisions |
| Finance | 02 — Core — Official & Macro | OCC — Bulletins | Yes | Yes | Yes | Off; summarize | banking-supervision/regulatory |
| Finance | 02 — Core — Official & Macro | OCC — News Releases | Yes | No | No | Off; summarize | banking-supervision/news-releases |
| Finance | 02 — Core — Official & Macro | OCC — Speeches | Yes | No | No | Off; summarize | banking-supervision/speeches |
| Finance | 02 — Core — Official & Macro | OCC — Congressional Testimony | Yes | No | No | Off; summarize | banking-supervision/testimony |
| Finance | 02 — Core — Official & Macro | OCC — Publications | Yes | No | No | Off; summarize | banking-supervision/publications |
| Finance | 02 — Core — Official & Macro | NFA — Manual Updates | Yes | No | No | Off; summarize | derivatives-regulation/rulebook |
| Finance | 02 — Core — Official & Macro | NFA — News Releases | Yes | No | No | Off; summarize | derivatives-regulation/news-releases |
| Finance | 02 — Core — Official & Macro | NFA — Notices to Members | Yes | No | No | Off; summarize | derivatives-regulation/member-notices |
| Finance | 02 — Core — Official & Macro | NFA — Board Updates | Yes | No | No | Off; summarize | derivatives-regulation/governance |
| Finance | 02 — Core — Official & Macro | NFA — Comment Letters | Yes | No | No | Off; summarize | derivatives-regulation/consultation |
| Finance | 02 — Core — Official & Macro | NFA — CFTC Rule Submission Letters | Yes | No | No | Off; summarize | derivatives-regulation/rule-submission |
| Finance | 02 — Core — Official & Macro | NFA — Regulatory Actions | Yes | No | No | Off; summarize | derivatives-regulation/enforcement |
| Finance | 02 — Core — Official & Macro | FDIC — Press Releases | Yes | No | No | Off; summarize | deposit-insurance/banking-regulation |
| Finance | 02 — Core — Official & Macro | Bank of Canada — Press Releases | Yes | Yes | Yes | Off; summarize | central-bank/news |
| Finance | 02 — Core — Official & Macro | OSFI — News | Yes | No | No | Off; summarize | prudential-supervision/financial-stability |
| Finance | 02 — Core — Official & Macro | Bank of Canada — Market Notices | Yes | Yes | Yes | Off; summarize | market-infrastructure/official-notices |
| Finance | 02 — Core — Official & Macro | Bank of Canada — Regulatory News | Yes | No | No | Off; summarize | payments-regulation/enforcement |
| Finance | 02 — Core — Official & Macro | FINTRAC — News | Yes | Yes | Yes | Off; summarize | financial-crime/intelligence |
| Finance | 02 — Core — Official & Macro | HKMA — Circulars | Yes | No | No | Off; summarize | banking-supervision/regulatory |
| Finance | 02 — Core — Official & Macro | HKMA — Consultations | Yes | No | No | Off; summarize | banking-supervision/consultation |
| Finance | 02 — Core — Official & Macro | HKMA — Supervisory Policy Manual | Yes | No | No | Off; summarize | banking-supervision/policy-manual |
| Finance | 02 — Core — Official & Macro | Reserve Bank of India — Press Releases | Yes | Yes | Yes | Off; summarize | central-bank/market |
| Finance | 02 — Core — Official & Macro | Reserve Bank of India — Notifications | Yes | Yes | Yes | Off; summarize | banking-regulation/notifications |
| Finance | 02 — Core — Official & Macro | Japan Financial Services Agency — English News | Yes | Yes | Yes | Off; summarize | financial-regulation/news |
| Finance | 02 — Core — Official & Macro | SEBI — Press Releases, Circulars & Orders | Yes | No | No | Off; summarize | securities-regulation/enforcement |
| Finance | 02 — Core — Official & Macro | Australian Treasury — Treasurer’s Media Releases | Yes | Yes | Yes | Off; summarize | fiscal-policy/official-releases |
| Finance | 02 — Core — Official & Macro | Australian Treasury — Assistant Treasurer & Financial Services Releases | Yes | Yes | Yes | Off; summarize | financial-regulation/policy |
| Finance | 02 — Core — Official & Macro | APRA — News | Yes | No | No | Off; summarize | prudential-supervision/regulatory |
| Finance | 02 — Core — Official & Macro | Bank of Japan — What's New | Yes | No | No | Off; summarize | central-bank/policy |
| Finance | 02 — Core — Official & Macro | Swiss National Bank — Press Releases | Yes | No | No | Off; summarize | central-bank/policy |
| Finance | 02 — Core — Official & Macro | Swiss National Bank — Monetary Policy | Yes | No | Yes | Off; summarize | central-bank/monetary-policy |
| Finance | 02 — Core — Official & Macro | Norges Bank — Press Releases | Yes | Yes | Yes | Off; summarize | central-bank/policy |
| Finance | 02 — Core — Official & Macro | Banco de España — News & Events | Yes | No | No | Off; summarize | central-bank/policy |
| Finance | 02 — Core — Official & Macro | Banco de España — Regulatory Circulars | Yes | No | No | Off; summarize | banking-regulation |
| Finance | 02 — Core — Official & Macro | Riksbank — Press Releases | Yes | No | No | Off; summarize | central-bank/policy |
| Finance | 02 — Core — Official & Macro | Riksbank — News | Yes | No | No | Off; summarize | central-bank/news |
| Finance | 02 — Core — Official & Macro | Czech National Bank — Press Releases | Yes | No | No | Off; summarize | central-bank/policy |
| Finance | 02 — Core — Official & Macro | Danmarks Nationalbank — Press Releases | Yes | Yes | Yes | Off; summarize | central-bank/policy |
| Finance | 02 — Core — Official & Macro | Danmarks Nationalbank — Speeches | Yes | No | No | Off; summarize | central-bank/speech |
| Finance | 02 — Core — Official & Macro | Danmarks Nationalbank — Market Announcements | Yes | Yes | Yes | Off; summarize | central-bank/market-operations |
| Finance | 03 — Optional — Data, Ireland, EU & UK | ECB — USD Reference Rate | Yes | Yes | Yes | Off; summarize | daily-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | ECB — GBP Reference Rate | Yes | Yes | Yes | Off; summarize | daily-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | ECB — Statistical Releases | Yes | Yes | Yes | Off; summarize | data/event |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Central Bank of Ireland — Markets Update | Yes | No | Yes | Off; summarize | regulatory/event |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Eurostat — Economy & Finance Releases | Yes | No | Yes | Off; summarize | data/event |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Eurostat — Industry, Trade & Services Releases | Yes | Yes | Yes | Off; summarize | data/event |
| Finance | 03 — Optional — Data, Ireland, EU & UK | European Commission — Sanctions Guidance | Yes | No | No | Off; summarize | regulatory/event |
| Finance | 03 — Optional — Data, Ireland, EU & UK | UK ONS — Release Calendar | Yes | Yes | Yes | Off; summarize | calendar/data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Bank of Japan — Statistics | Yes | No | No | Off; summarize | central-bank/statistics |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Danmarks Nationalbank — Statistical News | Yes | No | No | Off; summarize | central-bank/statistics |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Bank of Korea — Statistics & Publications | Yes | No | No | Off; summarize | central-bank/statistics |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Bank of Korea — Payment & Settlement Systems | Yes | No | No | Off; summarize | central-bank/payments |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco Central do Brasil — Exchange Rate | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco Central do Brasil — Focus Market Readout | Yes | Yes | Yes | Off; summarize | central-bank/market-expectations |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco Central do Brasil — Open Market Statistics | Yes | No | No | Off; summarize | central-bank/statistics |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — Exchange Rate FIX | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — Exchange Rate for Payments | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — Euro Exchange Rate | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — Target Rate | Yes | No | No | Off; summarize | central-bank/monetary-policy-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — Interbank Funding | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — TIIE 28 Days | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — CETES 28 Days | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — Worker Remittances | Yes | No | No | Off; summarize | central-bank/statistics |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — International Reserves | Yes | No | No | Off; summarize | central-bank/statistics |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — Investment Units (UDIS) | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — Commercial Bank Term Deposit Cost (CCP) | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — Commercial Bank Funding Cost (CPP) | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — Dollar Term Deposit Cost (CCP-Dollars) | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Banco de México — UDIS Term Deposit Cost (CCP-UDIS) | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | National Bank of Poland — Table A Average Exchange Rates | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | National Bank of Poland — Table B Average Exchange Rates | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | National Bank of Poland — Table C Buying and Selling Rates | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 03 — Optional — Data, Ireland, EU & UK | US Bureau of Economic Analysis — News Releases | Yes | No | No | Off; summarize | official-statistics/macro |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Statistics Canada — Economic Accounts | Yes | No | No | Off; summarize | official-statistics/macro |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Statistics Canada — Labour | Yes | No | No | Off; summarize | official-statistics/labour |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Statistics Canada — Prices and Price Indexes | Yes | No | No | Off; summarize | official-statistics/inflation |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Statistics Canada — Housing | Yes | No | No | Off; summarize | official-statistics/housing |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Statistics Canada — Manufacturing | Yes | No | No | Off; summarize | official-statistics/industry |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Statistics Canada — Retail and Wholesale | Yes | No | No | Off; summarize | official-statistics/consumer-demand |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Statistics Canada — Business Performance and Ownership | Yes | No | No | Off; summarize | official-statistics/business |
| Finance | 03 — Optional — Data, Ireland, EU & UK | US Census Bureau — Economic Indicators | Yes | No | No | Off; summarize | official-statistics/macro |
| Finance | 04 — Optional — Global Data & Research | African Development Bank — News & Events | Yes | No | No | Off; summarize | development-finance/african-macro |
| Finance | 04 — Optional — Global Data & Research | WHO Africa — Featured News | Yes | No | No | Off; summarize | public-health/health-security-news |
| Finance | 04 — Optional — Global Data & Research | Asian Infrastructure Investment Bank — News | Yes | No | No | Off; summarize | development-finance/news |
| Finance | 04 — Optional — Global Data & Research | Asian Infrastructure Investment Bank — Blogs | Yes | No | No | Off; summarize | development-finance/analysis |
| Finance | 04 — Optional — Global Data & Research | Asian Development Bank — News Releases | Yes | No | No | Off; summarize | development-finance/news |
| Finance | 04 — Optional — Global Data & Research | Asian Development Bank — Publications | Yes | No | No | Off; summarize | development-finance/publication |
| Finance | 04 — Optional — Global Data & Research | Banco de la República — News & Research (Spanish) | Yes | No | No | Off; summarize | central-bank/news-research |
| Finance | 04 — Optional — Global Data & Research | Reserve Bank of Australia — Daily Exchange Rates | Yes | No | No | Off; summarize | central-bank/market-data |
| Finance | 04 — Optional — Global Data & Research | Reserve Bank of Australia — Media Releases | Yes | Yes | Yes | Off; summarize | central-bank/news |
| Finance | 04 — Optional — Global Data & Research | Reserve Bank of Australia — Speeches | Yes | Yes | Yes | Off; summarize | central-bank/speeches |
| Finance | 04 — Optional — Global Data & Research | Reserve Bank of Australia — Bulletin | Yes | Yes | Yes | Off; summarize | central-bank/analysis |
| Finance | 04 — Optional — Global Data & Research | Reserve Bank of Australia — Financial Stability Review | Yes | Yes | Yes | Off; summarize | financial-stability/report |
| Finance | 04 — Optional — Global Data & Research | Reserve Bank of Australia — Statements on Monetary Policy | Yes | Yes | Yes | Off; summarize | central-bank/monetary-policy |
| Finance | 04 — Optional — Global Data & Research | Reserve Bank of Australia — Research Discussion Papers | Yes | Yes | Yes | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | BIS — Statistical Releases | Yes | No | No | Off; summarize | data/research |
| Finance | 04 — Optional — Global Data & Research | BIS — Press Releases | Yes | No | No | Off; summarize | policy/research |
| Finance | 04 — Optional — Global Data & Research | Federal Trade Commission — HSR Early Termination Notices | Yes | No | No | Off; summarize | merger-review/official-notices |
| Finance | 04 — Optional — Global Data & Research | European Central Bank — Blog | Yes | No | No | Off; summarize | central-bank/analysis |
| Finance | 04 — Optional — Global Data & Research | European Central Bank — Publications | Yes | No | No | Off; summarize | central-bank/research-publication |
| Finance | 04 — Optional — Global Data & Research | European Central Bank — Working Papers | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | European Central Bank — Research Bulletin | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | Bank of England — Publications | Yes | No | No | Off; summarize | research |
| Finance | 04 — Optional — Global Data & Research | ECB Banking Supervision — Publications | Yes | Yes | Yes | Off; summarize | banking-supervision/research |
| Finance | 04 — Optional — Global Data & Research | ECB Banking Supervision — Speeches | Yes | No | No | Off; summarize | banking-supervision/speeches |
| Finance | 04 — Optional — Global Data & Research | Federal Reserve — Working Papers | Yes | No | No | Off; summarize | research |
| Finance | 04 — Optional — Global Data & Research | Federal Reserve — FEDS Notes | Yes | No | No | Off; summarize | research/data |
| Finance | 04 — Optional — Global Data & Research | Federal Reserve — International Finance Discussion Papers | Yes | No | No | Off; summarize | international-finance/research |
| Finance | 04 — Optional — Global Data & Research | Federal Reserve Bank of St. Louis — FRED Blog | Yes | No | No | Off; summarize | macro/data-analysis |
| Finance | 04 — Optional — Global Data & Research | Federal Reserve Bank of St. Louis — On the Economy | Yes | No | No | Off; summarize | macro/research |
| Finance | 04 — Optional — Global Data & Research | Federal Reserve Bank of St. Louis — Review | Yes | No | No | Off; summarize | central-bank-research |
| Finance | 04 — Optional — Global Data & Research | BIS — FSI Publications | Yes | No | No | Off; summarize | financial-stability/research |
| Finance | 04 — Optional — Global Data & Research | BIS — Central Bankers’ Speeches | Yes | No | No | Off; summarize | central-bank-policy/speeches |
| Finance | 04 — Optional — Global Data & Research | BIS — Management Speeches | Yes | No | No | Off; summarize | financial-policy/speeches |
| Finance | 04 — Optional — Global Data & Research | European Investment Bank — Press Releases | Yes | No | No | Off; summarize | development-finance/policy |
| Finance | 04 — Optional — Global Data & Research | European Investment Bank — News | Yes | Yes | Yes | Off; summarize | development-finance/context |
| Finance | 04 — Optional — Global Data & Research | European Investment Bank — Publications | Yes | No | No | Off; summarize | development-finance/research |
| Finance | 04 — Optional — Global Data & Research | European Investment Bank — Blog | Yes | No | No | Off; summarize | development-finance/analysis |
| Finance | 04 — Optional — Global Data & Research | Apple — Newsroom | Yes | Yes | Yes | Off; summarize | technology/platform-policy |
| Finance | 04 — Optional — Global Data & Research | Apple Developer — News | Yes | No | No | Off; summarize | technology/developer-platform |
| Finance | 04 — Optional — Global Data & Research | European Commission — Harmonised Standards | Yes | No | No | Off; summarize | product-standards/regulatory-compliance |
| Finance | 04 — Optional — Global Data & Research | EIOPA — Risk-Free Rate Term Structures | Yes | No | No | Off; summarize | insurance-data/supervisory |
| Finance | 04 — Optional — Global Data & Research | EIOPA — Symmetric Adjustment Equity Capital Charge | Yes | No | No | Off; summarize | insurance-data/supervisory |
| Finance | 04 — Optional — Global Data & Research | DNB — Publications | Yes | No | No | Off; summarize | central-bank-publication |
| Finance | 04 — Optional — Global Data & Research | Bank of Finland Bulletin — Articles | Yes | Yes | Yes | Off; summarize | central-bank-research |
| Finance | 04 — Optional — Global Data & Research | DNB — Research Publications | Yes | No | No | Off; summarize | central-bank-research |
| Finance | 04 — Optional — Global Data & Research | Bank of England — Bank Insights | Yes | No | No | Off; summarize | central-bank-analysis |
| Finance | 04 — Optional — Global Data & Research | Bank of England — Statistics | Yes | No | No | Off; summarize | central-bank-data |
| Finance | 04 — Optional — Global Data & Research | Bank of England — Speeches | Yes | No | No | Off; summarize | central-bank-policy/speeches |
| Finance | 04 — Optional — Global Data & Research | FINMA — News | Yes | No | No | Off; summarize | financial-regulation/news |
| Finance | 04 — Optional — Global Data & Research | Bank of Canada — Financial Stability Report | Yes | Yes | Yes | Off; summarize | financial-stability/central-bank-research |
| Finance | 04 — Optional — Global Data & Research | HKMA — Daily Monetary Statistics | Yes | No | No | Off; summarize | central-bank-data/monetary-statistics |
| Finance | 04 — Optional — Global Data & Research | HKMA — Speeches | Yes | No | No | Off; summarize | central-bank-policy/speeches |
| Finance | 04 — Optional — Global Data & Research | HKMA — Publications | Yes | No | No | Off; summarize | central-bank/publication |
| Finance | 04 — Optional — Global Data & Research | HKMA — Research | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | HKMA — inSight | Yes | No | Yes | Off; summarize | central-bank/policy-analysis |
| Finance | 04 — Optional — Global Data & Research | Reserve Bank of India — Speeches | Yes | No | No | Off; summarize | central-bank-policy/speeches |
| Finance | 04 — Optional — Global Data & Research | Reserve Bank of India — Publications & Surveys | Yes | No | No | Off; summarize | central-bank-data/research |
| Finance | 04 — Optional — Global Data & Research | WTO — Latest News | Yes | Yes | Yes | Off; summarize | global-trade/policy |
| Finance | 04 — Optional — Global Data & Research | UN News — Economic Development | Yes | Yes | Yes | Off; summarize | global-development/geopolitical |
| Finance | 04 — Optional — Global Data & Research | UN News — Human Rights | Yes | Yes | Yes | Off; summarize | human-rights/geopolitical |
| Finance | 04 — Optional — Global Data & Research | UN News — Peace and Security | Yes | Yes | Yes | Off; summarize | peace-security/geopolitical |
| Finance | 04 — Optional — Global Data & Research | UN News — Health | Yes | Yes | Yes | Off; summarize | health/biological-risk |
| Finance | 04 — Optional — Global Data & Research | UN News — Climate and Environment | Yes | No | No | Off; summarize | climate-environment/physical-risk |
| Finance | 04 — Optional — Global Data & Research | UN News — Law and Crime Prevention | Yes | No | No | Off; summarize | financial-crime/justice |
| Finance | 04 — Optional — Global Data & Research | UN News — UN Affairs | Yes | No | No | Off; summarize | multilateral-policy/ai-governance |
| Finance | 04 — Optional — Global Data & Research | UN News — Migrants and Refugees | Yes | No | No | Off; summarize | migration/humanitarian-risk |
| Finance | 04 — Optional — Global Data & Research | European Medicines Agency — News and Press Releases | Yes | Yes | Yes | Off; summarize | pharma-regulatory/health |
| Finance | 04 — Optional — Global Data & Research | Council of the EU — Press Releases | Yes | Yes | Yes | Off; summarize | eu-policy/geopolitical |
| Finance | 04 — Optional — Global Data & Research | European Parliament — Committee Press Releases | Yes | Yes | Yes | Off; summarize | eu-policy/legislative |
| Finance | 04 — Optional — Global Data & Research | UK Parliament — Public Bills | Yes | Yes | Yes | Off; summarize | uk-legislation/policy |
| Finance | 04 — Optional — Global Data & Research | UK Parliament — Private Bills | Yes | No | No | Off; summarize | uk-legislation/policy |
| Finance | 04 — Optional — Global Data & Research | European Parliament — Plenary Press Releases | Yes | No | No | Off; summarize | eu-legislation/plenary |
| Finance | 04 — Optional — Global Data & Research | Swiss National Bank — Speeches | Yes | No | No | Off; summarize | central-bank/speech |
| Finance | 04 — Optional — Global Data & Research | Swiss National Bank — Research & Working Papers | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | Norges Bank — Financial Stability | Yes | No | No | Off; summarize | financial-stability/research |
| Finance | 04 — Optional — Global Data & Research | Norges Bank — Working Papers | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | Banco de España — Studies & Publications | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | Banco de España — Statistics | Yes | No | No | Off; summarize | central-bank/statistics |
| Finance | 04 — Optional — Global Data & Research | Banco de España — Blog | Yes | No | No | Off; summarize | central-bank/analysis |
| Finance | 04 — Optional — Global Data & Research | Riksbank — Speeches | Yes | No | No | Off; summarize | central-bank/speech |
| Finance | 04 — Optional — Global Data & Research | Riksbank — Monetary Policy Minutes | Yes | No | No | Off; summarize | central-bank/monetary-policy |
| Finance | 04 — Optional — Global Data & Research | Czech National Bank — cnBlog | Yes | No | No | Off; summarize | central-bank/analysis |
| Finance | 04 — Optional — Global Data & Research | Danmarks Nationalbank — Analysis | Yes | No | No | Off; summarize | central-bank/analysis |
| Finance | 04 — Optional — Global Data & Research | Danmarks Nationalbank — Working Papers | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | Danmarks Nationalbank — Reports | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | Banco Central do Brasil — Direct Investment Report | Yes | No | No | Off; summarize | central-bank/external-sector |
| Finance | 04 — Optional — Global Data & Research | Banco Central do Brasil — Financial Stability Report | Yes | No | No | Off; summarize | financial-stability/report |
| Finance | 04 — Optional — Global Data & Research | Banco Central do Brasil — Inflation Report | Yes | No | No | Off; summarize | central-bank/monetary-policy |
| Finance | 04 — Optional — Global Data & Research | Banco Central do Brasil — Comef Minutes | Yes | No | No | Off; summarize | financial-stability/committee |
| Finance | 04 — Optional — Global Data & Research | Banco Central do Brasil — Copom Minutes | Yes | No | No | Off; summarize | central-bank/monetary-policy |
| Finance | 04 — Optional — Global Data & Research | Banco Central do Brasil — Research Reports | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | Bank of Korea — Monetary Policy Reports | Yes | No | No | Off; summarize | central-bank/monetary-policy |
| Finance | 04 — Optional — Global Data & Research | Bank of Korea — Monetary Policy Board Minutes | Yes | No | No | Off; summarize | central-bank/monetary-policy |
| Finance | 04 — Optional — Global Data & Research | Bank of Korea — Speeches | Yes | No | No | Off; summarize | central-bank/speeches |
| Finance | 04 — Optional — Global Data & Research | Bank of Korea — Regional Economic Report | Yes | No | No | Off; summarize | central-bank/regional-economics |
| Finance | 04 — Optional — Global Data & Research | Bank of Korea — Economic Analysis | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | Bank of Korea — Financial Stability Report | Yes | No | No | Off; summarize | financial-stability/report |
| Finance | 04 — Optional — Global Data & Research | Court of Justice of the European Union — Press Releases | Yes | Yes | Yes | Off; summarize | eu-law/judicial |
| Finance | 04 — Optional — Global Data & Research | European Environment Agency — Indicators | Yes | No | No | Off; summarize | environmental-risk/official-indicators |
| Finance | 04 — Optional — Global Data & Research | European Environment Agency — Press Releases | Yes | No | No | Off; summarize | environmental-risk/official-news |
| Finance | 04 — Optional — Global Data & Research | European Environment Agency — Publications | Yes | No | No | Off; summarize | environmental-risk/official-publications |
| Finance | 04 — Optional — Global Data & Research | European Environment Agency — Featured Articles | Yes | No | No | Off; summarize | environmental-risk/official-analysis |
| Finance | 04 — Optional — Global Data & Research | European Environment Agency — Maps & Charts | Yes | No | No | Off; summarize | environmental-risk/official-data |
| Finance | 04 — Optional — Global Data & Research | European Commission — Research & Innovation News | Yes | No | No | Off; summarize | research/innovation-policy |
| Finance | 04 — Optional — Global Data & Research | European Food Safety Authority — News | Yes | No | No | Off; summarize | food-safety/science |
| Finance | 04 — Optional — Global Data & Research | European Food Safety Authority — Publications | Yes | No | No | Off; summarize | food-safety/research |
| Finance | 04 — Optional — Global Data & Research | European Patent Office — News | Yes | No | No | Off; summarize | intellectual-property/innovation |
| Finance | 05 — Optional — UK Regulation & Warnings | Bank of England — Prudential Regulation Publications | Yes | No | No | Off; summarize | prudential-regulation |
| Finance | 05 — Optional — UK Regulation & Warnings | FCA — News | Yes | No | No | Off; summarize | regulatory/news |
| Finance | 05 — Optional — UK Regulation & Warnings | FCA — Scam Warnings | Yes | Yes | Yes | Off; summarize | regulatory/alert |
| Finance | 05 — Optional — UK Regulation & Warnings | OFSI — Financial Sanctions Blog | Yes | Yes | Yes | Off; summarize | sanctions/policy |
| Finance | 05 — Optional — UK Regulation & Warnings | OFSI — Activity on GOV.UK | Yes | No | No | Off; summarize | sanctions/compliance |
| Finance | 05 — Optional — UK Regulation & Warnings | Guernsey Financial Services Commission — Financial Crime News | Yes | No | No | Off; summarize | financial-crime/regulation |
| Finance | 05 — Optional — UK Regulation & Warnings | Guernsey Financial Services Commission — Sanctions | Yes | No | No | Off; summarize | sanctions/alert |
| Finance | 05 — Optional — UK Regulation & Warnings | National Crime Agency — News | Yes | No | No | Off; summarize | financial-crime/cyber-enforcement |
| Finance | 05 — Optional — UK Regulation & Warnings | National Crime Agency — Direct News | Yes | No | No | Off; summarize | serious-organised-crime/financial-intelligence |
| Finance | 05 — Optional — UK Regulation & Warnings | Public Sector Fraud Authority — Activity on GOV.UK | Yes | No | No | Off; summarize | financial-crime/fraud-prevention |
| Finance | 05 — Optional — UK Regulation & Warnings | UK Ministry of Justice — Activity on GOV.UK | Yes | No | No | Off; summarize | justice-policy/legal-risk |
| Finance | 05 — Optional — UK Regulation & Warnings | UK Attorney General's Office — Activity on GOV.UK | Yes | No | No | Off; summarize | criminal-law/prosecution |
| Finance | 05 — Optional — UK Regulation & Warnings | UK Crown Prosecution Service — Activity on GOV.UK | Yes | No | No | Off; summarize | criminal-prosecution/legal-enforcement |
| Finance | 05 — Optional — UK Regulation & Warnings | HM Courts & Tribunals Service — Activity on GOV.UK | Yes | No | No | Off; summarize | courts/tribunals/legal-risk |
| Finance | 05 — Optional — UK Regulation & Warnings | Courts and Tribunals Judiciary — Judgments | Yes | No | No | Off; summarize | judgments/legal-risk |
| Finance | 05 — Optional — UK Regulation & Warnings | UK Financial Reporting Council — Activity on GOV.UK | Yes | No | No | Off; summarize | audit/corporate-governance-regulation |
| Finance | 05 — Optional — UK Regulation & Warnings | Office of Trade Sanctions Implementation — Updates | Yes | No | No | Off; summarize | sanctions/trade-policy |
| Finance | 05 — Optional — UK Regulation & Warnings | Export Control Joint Unit — Updates | Yes | No | No | Off; summarize | export-controls/sanctions |
| Finance | 04 — Optional — Global Data & Research | UK National Audit Office — News | Yes | No | No | Off; summarize | public-finance/audit |
| Finance | 04 — Optional — Global Data & Research | US GAO — Budget & Spending Reports | Yes | No | No | Off; summarize | public-finance/audit |
| Finance | 04 — Optional — Global Data & Research | US GAO — Financial Markets & Institutions Reports | Yes | No | No | Off; summarize | financial-regulation/audit |
| Finance | 04 — Optional — Global Data & Research | US GAO — Tax Policy & Administration Reports | Yes | No | No | Off; summarize | tax-policy/audit |
| Finance | 04 — Optional — Global Data & Research | US Congressional Budget Office — Publications | Yes | No | No | Off; summarize | budget-analysis/research |
| Finance | 04 — Optional — Global Data & Research | NIESR — News & Analysis | Yes | No | No | Off; summarize | independent-macro/research |
| Finance | 04 — Optional — Global Data & Research | Resolution Foundation — Research & Commentary | Yes | No | No | Off; summarize | independent-macro/policy |
| Finance | 04 — Optional — Global Data & Research | CEPR — VoxEU Research & Policy Analysis | Yes | No | No | Off; summarize | independent-macro/research |
| Finance | 04 — Optional — Global Data & Research | CEPR — Discussion Papers | Yes | No | No | Off; summarize | independent-macro/research |
| Finance | 04 — Optional — Global Data & Research | Tax Foundation — Research & Commentary | Yes | No | No | Off; summarize | tax-policy/research |
| Finance | 04 — Optional — Global Data & Research | OECD Ecoscope — Economics Department Blog | Yes | No | No | Off; summarize | official-macro/research |
| Finance | 04 — Optional — Global Data & Research | Deutsche Bundesbank — Discussion Papers | Yes | No | No | Off; summarize | central-bank/research |
| Finance | 04 — Optional — Global Data & Research | Deutsche Bundesbank — Latest Announcements | Yes | No | No | Off; summarize | central-bank/market-operations |
| Finance | 04 — Optional — Global Data & Research | Deutsche Bundesbank — Speeches, Interviews & Contributions | Yes | Yes | Yes | Off; summarize | central-bank/policy |
| Finance | 04 — Optional — Global Data & Research | Deutsche Bundesbank — Topics | Yes | No | No | Off; summarize | central-bank/analysis |
| Finance | 04 — Optional — Global Data & Research | German Council of Economic Experts — RSS | Yes | No | No | Off; summarize | public-finance/research |
| Finance | 04 — Optional — Global Data & Research | DIW Berlin — News & Press Releases | Yes | No | No | Off; summarize | independent-macro/research |
| Finance | 04 — Optional — Global Data & Research | DIW Berlin — Publications | Yes | No | No | Off; summarize | independent-macro/research |
| Finance | 04 — Optional — Global Data & Research | DIW Berlin — SOEP News (English) | Yes | No | No | Off; summarize | social-economics/research |
| Finance | 04 — Optional — Global Data & Research | RWI Essen — Unstatistiken | Yes | No | No | Off; summarize | statistics/research |
| Finance | 04 — Optional — Global Data & Research | BMUKN — All News | Yes | No | No | Off; summarize | official-policy/research |
| Finance | 02 — Core — Official & Macro | Finanstilsynet — News (Norwegian) | Yes | No | No | Off; summarize | financial-regulation/news |
| Finance | 02 — Core — Official & Macro | Finanstilsynet — Circulars (Norwegian) | Yes | No | No | Off; summarize | financial-regulation/circular |
| Finance | 02 — Core — Official & Macro | Japan Financial Services Agency — All News (Japanese) | Yes | No | No | Off; summarize | financial-regulation/news |
| Finance | 02 — Core — Official & Macro | CSSF — All Publications (English) | Yes | No | No | Off; summarize | financial-regulation/publication |
| Finance | 02 — Core — Official & Macro | FMA Austria — All News (English) | Yes | No | No | Off; summarize | financial-regulation/news |
| Finance | 02 — Core — Official & Macro | FSMA Belgium — News & Warnings (English) | Yes | No | No | Off; summarize | financial-regulation/warning |
| Finance | 02 — Core — Official & Macro | BaFin — Supervisory Measures (German) | Yes | No | No | Off; summarize | financial-regulation/enforcement |
| Finance | 02 — Core — Official & Macro | BaFin — Circulars (German) | Yes | No | No | Off; summarize | financial-regulation/policy |
| Finance | 05 — Optional — UK Regulation & Warnings | The Pensions Regulator — Activity on GOV.UK | Yes | No | No | Off; summarize | pensions-regulation/financial-risk |
| Finance | 05 — Optional — UK Regulation & Warnings | Payment Systems Regulator — Activity on GOV.UK | Yes | No | No | Off; summarize | payments-regulation/financial-infrastructure |
| Finance | 05 — Optional — UK Regulation & Warnings | Pension Protection Fund — Activity on GOV.UK | Yes | No | No | Off; summarize | pension-protection/financial-resilience |
| Finance | 04 — Optional — Global Data & Research | European Labour Authority — News | Yes | No | No | Off; summarize | labour-mobility/enforcement |
| Finance | 04 — Optional — Global Data & Research | European Commission — Employment, Social Affairs & Inclusion News | Yes | No | No | Off; summarize | employment/social-policy |
| Finance | 04 — Optional — Global Data & Research | European Commission — Environment News | Yes | No | No | Off; summarize | environmental-risk/regulation |
| Finance | 04 — Optional — Global Data & Research | European Commission — Public Health News | Yes | No | No | Off; summarize | public-health/health-regulation |
| Finance | 04 — Optional — Global Data & Research | European Commission — Climate Action News | Yes | No | No | Off; summarize | climate-policy/carbon-market-risk |
| Finance | 02 — Core — Official & Macro | U.S. Department of Energy — Energy News | Yes | No | No | Off; summarize | energy-security/critical-infrastructure |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | NIST — General News & Critical Technology | Yes | No | No | Off; summarize | critical-technology/standards-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | European Commission — Digital Strategy News | Yes | No | No | Off; summarize | digital-policy/cyber-resilience |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | Ireland NCSC — Alerts & Advisories | Yes | Yes | Yes | **On** | alert |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | Ireland NCSC — Guidance Documents | Yes | Yes | Yes | Off; summarize | guidance/policy |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | Swiss NCSC — Press Releases (German) | Yes | No | No | Off; summarize | national-csirt/news |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CISA — All Advisories | Yes | Yes | Yes | **On** | advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CERT-EU — Security Advisories | Yes | Yes | Yes | **On** | advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CERT-FR — Security Alerts (French) | Yes | Yes | Yes | Optional on; French | alert/advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | NCSC UK — News | Yes | Yes | Yes | Optional on | alert/news |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | NCSC UK — All Updates | Yes | Yes | Yes | Optional on | alert/context |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CISA — News | Yes | Yes | Yes | Off; summarize | official-cyber/news |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | NCSC Netherlands — Security Advisories | Yes | No | No | Off; summarize | advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | NCSC Netherlands — News | Yes | No | No | Off; summarize | official-cyber/news |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CERT Polska — Security Advisories & News (Polish) | Yes | No | No | Off; summarize | national-csirt/advisory-news |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CERT.at — Warnings | Yes | No | No | Off; summarize | advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CERT Polska — Advisories | Yes | No | No | Off; summarize | advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CERT-SE — News | Yes | No | No | Off; summarize | advisory/news |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | New Zealand NCSC — News | Yes | No | No | Off; summarize | news/guidance |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | European Data Protection Board — News | Yes | Yes | Yes | Off; summarize | privacy/AI-governance |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | JPCERT/CC — All Updates | Yes | No | No | Off; summarize | national-csirt/advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | JVN — Vulnerability Notes | Yes | No | No | Off; summarize | vulnerability-coordination |
| Cyber Security | 02 — Core — News & Incident Reporting | BleepingComputer | Yes | Yes | Yes | Off; summarize | news |
| Cyber Security | 02 — Core — News & Incident Reporting | The Hacker News | Yes | No | No | Off; summarize | news/incident |
| Cyber Security | 02 — Core — News & Incident Reporting | CyberScoop | Yes | Yes | Yes | Off; summarize | news/policy |
| Cyber Security | 02 — Core — News & Incident Reporting | SecurityWeek | Yes | No | No | Off; summarize | news |
| Cyber Security | 02 — Core — News & Incident Reporting | The Record — Cybersecurity News | Yes | Yes | Yes | Off; summarize | news |
| Cyber Security | 02 — Core — News & Incident Reporting | The DFIR Report | Yes | No | No | Off; summarize | incident-response/research |
| Cyber Security | 02 — Core — News & Incident Reporting | Krebs on Security | Yes | No | No | Off; summarize | news/incident |
| Cyber Security | 03 — Core — Technical Research | CERT/CC — Vulnerability Notes | Yes | Yes | Yes | Off; summarize | advisory/research |
| Cyber Security | 03 — Core — Technical Research | NIST — Cybersecurity Insights | Yes | Yes | Yes | Off; summarize | research/guidance |
| Cyber Security | 03 — Core — Technical Research | Google Threat Intelligence — Mandiant | Yes | No | No | Off; summarize | research |
| Cyber Security | 03 — Core — Technical Research | FBI — Ahead of the Threat Cyber Podcast | Yes | No | No | Off; summarize | official-cyber/podcast |
| Cyber Security | 03 — Core — Technical Research | Google Project Zero — Research | Yes | No | No | Off; summarize | vulnerability-research |
| Cyber Security | 03 — Core — Technical Research | Google Security Blog | Yes | No | No | Off; summarize | official-vendor/research |
| Cyber Security | 03 — Core — Technical Research | Rapid7 — Research | Yes | No | No | Off; summarize | research/vulnerability |
| Cyber Security | 03 — Core — Technical Research | Elastic Security Labs | Yes | No | No | Off; summarize | research |
| Cyber Security | 03 — Core — Technical Research | Microsoft Security Blog | Yes | No | No | Off; summarize | research/advisory |
| Cyber Security | 03 — Core — Technical Research | Unit 42 — Threat Research | Yes | Yes | Yes | Off; summarize | research |
| Cyber Security | 03 — Core — Technical Research | GitHub Security Blog | Yes | Yes | Yes | Off; summarize | research/advisory |
| Cyber Security | 03 — Core — Technical Research | OWASP | Yes | No | No | Off; summarize | application-security/guidance |
| Cyber Security | 03 — Core — Technical Research | Zero Day Initiative — Blog | Yes | No | No | Off; summarize | vulnerability-research |
| Cyber Security | 03 — Core — Technical Research | Trail of Bits — Blog | Yes | No | No | Off; summarize | technical-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | KISA — Press Releases (Korean) | Yes | No | No | Off; summarize | national-cyber/news |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | KrCERT/CC — Security Alerts (Korean) | Yes | No | No | Off; summarize | national-csirt/advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | KrCERT/CC — Reports & Guides (Korean) | Yes | No | No | Off; summarize | national-csirt/research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | KrCERT/CC — Vulnerability Information (Korean) | Yes | No | No | Off; summarize | national-csirt/vulnerability |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | KrCERT/CC — Cyber Crisis Alert Level (Korean) | Yes | No | No | Off; summarize | national-csirt/alert-level |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | CISA — ICS Advisories | Yes | No | No | Optional on | advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | AWS Security Bulletins | Yes | No | No | Optional on | advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | CERT-EU — Threat Intelligence | Yes | No | Yes | Off; summarize | research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | CERT-FR — Security Advisories (French) | Yes | No | No | Off; summarize | advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Cisco PSIRT — Security Advisories | Yes | No | No | Optional on | advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Schneier on Security | Yes | No | No | Off; summarize | research/context |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Cisco Talos | Yes | No | No | Off; summarize | research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | CrowdStrike — Cybersecurity Research | Yes | No | No | Off; summarize | research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | OpenSSF — Supply Chain Security | Yes | No | No | Off; summarize | research/guidance |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Microsoft Security Response Center — Security Update Guide | Yes | No | No | Off; summarize | vendor-advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Ubuntu — Security Notices | Yes | No | No | Off; summarize | vendor-advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Red Hat — Security Advisories | Yes | No | No | Off; summarize | vendor-advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Docker — Security | Yes | No | No | Off; summarize | container-security/guidance |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Securelist | Yes | No | No | Off; summarize | threat-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | SentinelLabs | Yes | No | No | Off; summarize | threat-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Cloudflare — Security | Yes | No | No | Off; summarize | internet-security/guidance |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | HKCERT — Security Bulletin | Yes | No | No | Off; summarize | regional-csirt/advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | HKCERT — Security News | Yes | No | No | Off; summarize | regional-csirt/news |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | BSI — Press, Short Communications & Events | Yes | No | No | Off; summarize | cyber-policy/research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | BSI/CERT-Bund — IT Security Advisories | Yes | No | No | Off; summarize | national-csirt/advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | Centre for Cybersecurity Belgium — Advisories | Yes | Yes | Yes | Off; summarize | national-csirt/advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Centre for Cybersecurity Belgium — News | Yes | No | No | Off; summarize | cyber-policy/news |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | Romania DNSC — Cybersecurity News & Alerts | Yes | No | No | Off; summarize | national-csirt/news-advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CERT.LV — News & Cybersecurity Updates | Yes | No | No | Off; summarize | national-csirt/research |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | SI-CERT — Vulnerability & Cybersecurity News | Yes | No | No | Off; summarize | national-csirt/vulnerability |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | Norway NCSC — Vulnerability Alerts | Yes | No | No | Off; summarize | national-csirt/advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | INCIBE-CERT — Security Advisories (Spanish) | Yes | No | No | Off; summarize | national-csirt/advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | INCIBE — Enterprise Security Advisories (Spanish) | Yes | No | No | Off; summarize | national-csirt/enterprise-advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | INCIBE — Citizen Fraud & Impersonation Warnings (Spanish) | Yes | No | No | Off; summarize | consumer-fraud/warning |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | NÚKIB — News (Czech) | Yes | No | No | Off; summarize | national-csirt/news-advisory |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CERT.hr — News (Croatian) | Yes | No | No | Off; summarize | national-csirt/consumer-warning |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | Estonian RIA — Cybersecurity News (Estonian) | Yes | No | No | Off; summarize | national-csirt/news |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | ANSSI — Cyber Threat Overviews (English) | Yes | No | No | Off; summarize | threat-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | CSSF — Cybersecurity Publications (English) | Yes | No | No | Off; summarize | financial-cyber/regulatory-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | NCSC-FI — Vulnerabilities (Finnish) | Yes | No | No | Off; summarize | national-csirt/vulnerability |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | ACN / CSIRT Italia — Security Updates (Italian) | Yes | No | Yes | Off; summarize | national-csirt/vulnerability |
| Finance | 02 — Core — Official & Macro | Finansinspektionen — News (English) | Yes | No | No | Off; summarize | financial-regulation/news |
| Finance | 02 — Core — Official & Macro | European Ombudsman — News & Decisions (English) | Yes | No | No | Off; summarize | institutional-accountability/governance |
| Finance | 02 — Core — Official & Macro | EUR-Lex — Parliament & Council Legislation (English) | Yes | No | No | Off; summarize | eu-law/regulatory-policy |
| Finance | 02 — Core — Official & Macro | EUR-Lex — Official Journal C (English) | Yes | No | No | Off; summarize | eu-law/official-notices |
| Finance | 02 — Core — Official & Macro | European Commission — Migration & Home Affairs News | Yes | No | No | Off; summarize | internal-security/border-resilience |
| Finance | 02 — Core — Official & Macro | Frontex — News Releases | Yes | No | No | Off; summarize | border-security/organised-crime |
| Finance | 04 — Optional — Global Data & Research | EU Agency for the Space Programme — News | Yes | No | No | Off; summarize | space-infrastructure/security |
| Finance | 04 — Optional — Global Data & Research | EU Agency for the Space Programme — Press Releases | Yes | No | No | Off; summarize | space-markets/secure-connectivity |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | EASA — Cybersecurity News | Yes | No | No | Off; summarize | aviation-cybersecurity/transport-resilience |
| Finance | 04 — Optional — Global Data & Research | ECDC — News | Yes | No | No | Off; summarize | public-health-threat/news |
| Finance | 04 — Optional — Global Data & Research | ECDC — Communicable Disease Threat Reports | Yes | No | No | Off; summarize | public-health-threat/weekly-report |
| Finance | 02 — Core — Official & Macro | UK Home Office — Activity on GOV.UK | Yes | No | No | Off; summarize | internal-security/migration-policy |
| Finance | 02 — Core — Official & Macro | UK Ministry of Defence — Activity on GOV.UK | Yes | No | No | Off; summarize | defence/security-policy |
| Finance | 02 — Core — Official & Macro | UK Department for Transport — Activity on GOV.UK | Yes | No | No | Off; summarize | transport-infrastructure/policy |
| Finance | 02 — Core — Official & Macro | U.S. Department of Defense — News | Yes | No | No | Off; summarize | defence/security-policy |
| Finance | 02 — Core — Official & Macro | U.S. Department of Defense — Releases | Yes | No | No | Off; summarize | defence/strategic-industry |
| Finance | 04 — Optional — Global Data & Research | IAEA — News | Yes | No | No | Off; summarize | nuclear-safety/security-energy |
| Finance | 04 — Optional — Global Data & Research | IAEA — Publications | Yes | Yes | Yes | Off; summarize | nuclear-safety/security-research |
| Finance | 04 — Optional — Global Data & Research | European Union — Featured News | Yes | No | No | Off; summarize | eu-institutional-policy |
| Finance | 02 — Core — Official & Macro | U.S. Energy Information Administration — Today in Energy | Yes | No | No | Off; summarize | energy-markets/security-analysis |
| Finance | 02 — Core — Official & Macro | U.S. Energy Information Administration — Press Releases | Yes | No | No | Off; summarize | energy-policy/forecast |
| Finance | 04 — Optional — Global Data & Research | U.S. Energy Information Administration — What's New | Yes | No | No | Off; summarize | energy-data/release-calendar |
| Finance | 04 — Optional — Global Data & Research | CDC Travelers' Health — Travel Notices | Yes | No | No | Off; summarize | public-health-threat/travel-risk |
| Finance | 04 — Optional — Global Data & Research | CDC — Emerging Infectious Diseases Ahead-of-Print | Yes | No | No | Off; summarize | public-health-research/emerging-infections |
| Finance | 02 — Core — Official & Macro | U.S. Nuclear Regulatory Commission — News Releases | Yes | No | No | Off; summarize | nuclear-regulation/safety-policy |
| Finance | 04 — Optional — Global Data & Research | CDC — Morbidity and Mortality Weekly Report (MMWR) | Yes | No | No | Off; summarize | public-health-surveillance/research |
| Finance | 04 — Optional — Global Data & Research | U.S. Geological Survey — Significant Earthquakes | Yes | No | No | Off; summarize | natural-hazard/seismic-risk |
| Finance | 02 — Core — Official & Macro | FEMA — News Releases | Yes | No | No | Off; summarize | emergency-response/disaster-risk |
| Finance | 04 — Optional — Global Data & Research | U.S. FDA — Food Safety Recalls | Yes | No | No | Off; summarize | food-safety/recall-alert |
| Finance | 04 — Optional — Global Data & Research | U.S. FDA — MedWatch Safety Alerts | Yes | No | No | Off; summarize | medical-safety/alert |
| Finance | 04 — Optional — Global Data & Research | U.S. FDA — Press Releases | Yes | No | No | Off; summarize | health-regulation/public-policy |
| Finance | 04 — Optional — Global Data & Research | U.S. FDA — What’s New for Drugs | Yes | No | No | Off; summarize | drug-regulation/product-policy |
| Finance | 04 — Optional — Global Data & Research | U.S. FDA — What’s New for Vaccines, Blood & Biologics | Yes | No | No | Off; summarize | biologics-vaccines/regulation |
| Finance | 04 — Optional — Global Data & Research | U.S. FDA — Health Fraud Alerts | Yes | No | No | Off; summarize | health-fraud/consumer-risk |
| Finance | 04 — Optional — Global Data & Research | NASA — News Releases | Yes | No | No | Off; summarize | space-research/strategic-technology |
| Finance | 04 — Optional — Global Data & Research | NASA — Technology | Yes | No | No | Off; summarize | space-technology/research |
| Finance | 04 — Optional — Global Data & Research | NASA — Aeronautics | Yes | No | No | Off; summarize | aeronautics/aviation-infrastructure |
| Finance | 04 — Optional — Global Data & Research | NASA — Space Station | Yes | No | No | Off; summarize | spaceflight/orbital-research |
| Finance | 04 — Optional — Global Data & Research | NASA — Artemis | Yes | No | No | Off; summarize | lunar-exploration/strategic-space |
| Finance | 04 — Optional — Global Data & Research | ESA — Space News | Yes | No | No | Off; summarize | space-research/strategic-technology |
| Finance | 04 — Optional — Global Data & Research | ESA — Navigation | Yes | No | No | Off; summarize | GNSS/PNT-resilience |
| Finance | 04 — Optional — Global Data & Research | ESA — Observing the Earth | Yes | No | No | Off; summarize | Earth-observation/physical-risk |
| Finance | 04 — Optional — Global Data & Research | ESA — Launchers | Yes | No | No | Off; summarize | space-transport/industrial-resilience |
| Finance | 04 — Optional — Global Data & Research | ESA — Space Engineering & Technology | Yes | No | No | Off; summarize | space-technology/industrial-resilience |
| Finance | 04 — Optional — Global Data & Research | ESA — Telecommunications & Integrated Applications | Yes | No | No | Off; summarize | secure-connectivity/critical-infrastructure |
| Finance | 04 — Optional — Global Data & Research | EASA — News | Yes | No | No | Off; summarize | aviation-safety/strategic-infrastructure |
| Finance | 04 — Optional — Global Data & Research | EASA — Press Releases | Yes | No | No | Off; summarize | aviation-regulation/strategic-infrastructure |
| Finance | 04 — Optional — Global Data & Research | EASA — Notices of Proposed Amendment | Yes | No | No | Off; summarize | aviation-rulemaking/public-consultation |
| Finance | 04 — Optional — Global Data & Research | EASA — Opinions | Yes | No | No | Off; summarize | aviation-regulation/legal-policy |
| Finance | 04 — Optional — Global Data & Research | EASA — Regulations | Yes | No | No | Off; summarize | aviation-regulation/legal |
| Finance | 04 — Optional — Global Data & Research | EASA — Acceptable Means of Compliance & Guidance | Yes | No | No | Off; summarize | aviation-guidance/compliance |
| Finance | 04 — Optional — Global Data & Research | ESA — Space Science | Yes | No | No | Off; summarize | space-science/research |
| Finance | 04 — Optional — Global Data & Research | ESA — Operations | Yes | No | No | Off; summarize | space-operations/infrastructure-resilience |
| Finance | 04 — Optional — Global Data & Research | EASA — Agency Decisions | Yes | No | No | Off; summarize | aviation-regulation/agency-decision |
| Finance | 04 — Optional — Global Data & Research | EASA — Certification Specifications | Yes | No | No | Off; summarize | aviation-certification/technical-standard |
| Finance | 04 — Optional — Global Data & Research | EASA — Comment Response Documents | Yes | No | No | Off; summarize | aviation-rulemaking/consultation-response |
| Finance | 02 — Core — Official & Macro | U.S. Treasury — Press Releases | Yes | No | No | Off; summarize | fiscal-policy/financial-regulation |
| Finance | 02 — Core — Official & Macro | SEC — Speeches and Statements | Yes | No | No | Off; summarize | securities-regulation/policy |
| Finance | 02 — Core — Official & Macro | SEC — Testimony | Yes | No | No | Off; summarize | securities-regulation/testimony |
| Finance | 04 — Optional — Global Data & Research | House of Lords Library — Research | Yes | No | No | Off; summarize | uk-parliamentary-research/policy |
| Finance | 04 — Optional — Global Data & Research | House of Commons Library — Research | Yes | No | No | Off; summarize | uk-parliamentary-research/policy |
| Finance | 04 — Optional — Global Data & Research | UK Parliament POST — Research | Yes | No | No | Off; summarize | science-policy/cyber-resilience |
| Finance | 04 — Optional — Global Data & Research | European Economic and Social Committee — News | Yes | No | No | Off; summarize | eu-policy/institutional-research |
| Finance | 04 — Optional — Global Data & Research | UK Department for Energy Security and Net Zero — Activity on GOV.UK | Yes | No | No | Off; summarize | energy-security/strategic-infrastructure |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | UK Department for Science, Innovation and Technology — Activity on GOV.UK | Yes | Yes | Yes | Off; summarize | digital-policy/cyber-resilience |
| Finance | 04 — Optional — Global Data & Research | UK Foreign, Commonwealth & Development Office — Activity on GOV.UK | Yes | No | No | Off; summarize | foreign-policy/geopolitical-risk |
| Finance | 04 — Optional — Global Data & Research | UK Cabinet Office — Activity on GOV.UK | Yes | No | No | Off; summarize | government-resilience/cross-government-policy |
| Finance | 04 — Optional — Global Data & Research | UK Department of Health and Social Care — Activity on GOV.UK | Yes | No | No | Off; summarize | public-health/health-security-policy |
| Finance | 04 — Optional — Global Data & Research | United Nations — Meetings Coverage and Press Releases | Yes | No | No | Off; summarize | multilateral-security/geopolitical-risk |
| Finance | 04 — Optional — Global Data & Research | UK Department for Business and Trade — Activity on GOV.UK | Yes | No | No | Off; summarize | trade-policy/industrial-strategy |
| Finance | 04 — Optional — Global Data & Research | UK Department for Environment, Food & Rural Affairs — Activity on GOV.UK | Yes | No | No | Off; summarize | food-security/environmental-resilience |
| Finance | 04 — Optional — Global Data & Research | UK Government Office for Science — Activity on GOV.UK | Yes | No | No | Off; summarize | science-policy/emerging-risk |
| Finance | 04 — Optional — Global Data & Research | Pan American Health Organization — News | Yes | No | No | Off; summarize | public-health/health-security-news |
| Finance | 04 — Optional — Global Data & Research | Food and Agriculture Organization of the United Nations — Newsroom | Yes | No | No | Off; summarize | food-security/commodity-resilience |
| Finance | 04 — Optional — Global Data & Research | European Court of Human Rights — Press Releases (English) | Yes | No | No | Off; summarize | human-rights/legal-risk |
| Finance | 04 — Optional — Global Data & Research | European Court of Human Rights — Grand Chamber Judgments (English) | Yes | No | No | Off; summarize | human-rights/constitutional-law |
| Finance | 04 — Optional — Global Data & Research | European Court of Human Rights — Chamber Judgments and Decisions (English) | Yes | No | No | Off; summarize | human-rights/civil-liberties-law |
| Finance | 04 — Optional — Global Data & Research | European Union Agency for Fundamental Rights — News | Yes | No | No | Off; summarize | fundamental-rights/legal-risk |
| Finance | 04 — Optional — Global Data & Research | European Union Agency for Asylum — Press Releases | Yes | No | No | Off; summarize | asylum-migration/internal-security |
| Finance | 04 — Optional — Global Data & Research | ASEAN — News | Yes | No | No | Off; summarize | regional-integration/geopolitical-risk |
| Finance | 04 — Optional — Global Data & Research | ASEAN+3 Macroeconomic Research Office — News & Research | Yes | No | No | Off; summarize | macroeconomic-surveillance/financial-stability |
| Finance | 04 — Optional — Global Data & Research | ASEAN+3 Macroeconomic Research Office — Press Releases | Yes | No | No | Off; summarize | macroeconomic-surveillance/country-risk |
| Finance | 04 — Optional — Global Data & Research | European Commission — Agriculture & Rural Development News | Yes | No | No | Off; summarize | agri-food-trade/food-security |
| Finance | 04 — Optional — Global Data & Research | European Commission — Enlargement & Eastern Neighbourhood News | Yes | No | No | Off; summarize | geopolitical-risk/european-neighbourhood |
| Finance | 04 — Optional — Global Data & Research | European Maritime Safety Agency — Latest News | Yes | Yes | Yes | Off; summarize | maritime-safety/resilience |
| Finance | 04 — Optional — Global Data & Research | European Commission — Oceans & Fisheries News | Yes | Yes | Yes | Off; summarize | maritime-security/food-supply |
| Finance | 04 — Optional — Global Data & Research | Eurostat — Data and Data Structure Updates | Yes | No | No | Off; summarize | statistical-data-change |
| Finance | 04 — Optional — Global Data & Research | European Training Foundation — News | Yes | No | No | Off; summarize | skills/labour-migration/human-capital |
| Finance | 04 — Optional — Global Data & Research | European Union Agency for Railways — News | Yes | Yes | Yes | Off; summarize | rail-safety/transport-policy |
| Finance | 04 — Optional — Global Data & Research | Eurofound — News | Yes | Yes | Yes | Off; summarize | labour-market/social-policy |
| Finance | 04 — Optional — Global Data & Research | United Nations Office at Geneva — Meeting Summaries | Yes | No | No | Off; summarize | multilateral-policy/human-rights |
| Finance | 04 — Optional — Global Data & Research | Caribbean Development Bank — News Releases | Yes | No | No | Off; summarize | development-finance/regional-macro |
| Finance | 04 — Optional — Global Data & Research | Afreximbank Research — Journal of African Trade | Yes | No | No | Off; summarize | trade-policy/african-macro-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | European Cybersecurity Competence Centre and Network — News | Yes | No | No | Off; summarize | cyber-policy/resilience/funding |
| Finance | 02 — Core — Official & Macro | Banco Central do Brasil — News (Portuguese) | Yes | No | No | Off; summarize | central-bank/financial-system |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | RUSI — Latest Commentary | Yes | Yes | Yes | Off; summarize | security/geopolitical-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | SIPRI — Global Security & Arms Control | Yes | Yes | Yes | Off; summarize | security/arms-control-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Chatham House — Expert Comment | Yes | No | No | Off; summarize | security/geopolitical-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Chatham House — News Releases | Yes | No | No | Off; summarize | security/geopolitical-policy |
| Finance | 04 — Optional — Global Data & Research | U.S. Courts — Judiciary News | Yes | Yes | Yes | Off; summarize | legal/financial-risk |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | CIS — MS-ISAC Advisories | Yes | Yes | Yes | Off; summarize | vulnerability/advisory |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | EUISS — News & Publications | Yes | No | No | Off; summarize | security/geopolitical-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | ECFR — European Foreign & Security Policy | Yes | No | No | Off; summarize | security/geopolitical-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Bellingcat — Open-Source Investigations | Yes | No | No | Off; summarize | security/osint-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Global Initiative — Organized Crime & Illicit Economies | Yes | No | No | Off; summarize | security/organized-crime-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Jamestown — Eurasia & Terrorism Analysis | Yes | No | No | Off; summarize | security/geopolitical-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Atlantic Council — Global Security & Geopolitics | Yes | No | No | Off; summarize | security/geopolitical-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | FDD — National Security & Foreign Policy Analysis | Yes | No | No | Off; summarize | security/geopolitical-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Lawfare — Cybersecurity & Tech | Yes | No | No | Off; summarize | security/cyber-policy-research |
| Finance | 02 — Core — Official & Macro | National Defence — News | Yes | No | No | Off; summarize | defence/security-policy |
| Finance | 02 — Core — Official & Macro | Global Affairs Canada — News | Yes | Yes | Yes | Off; summarize | foreign-policy/trade-security |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | Communications Security Establishment — News | Yes | Yes | Yes | Off; summarize | cyber/national-security |
| Finance | 02 — Core — Official & Macro | Defence Investment Agency — News | Yes | Yes | Yes | Off; summarize | defence/industrial-policy |
| Finance | 02 — Core — Official & Macro | Canadian Security Intelligence Service — News | Yes | Yes | Yes | Off; summarize | national-security/intelligence |
| Finance | 04 — Optional — Global Data & Research | Council of the EU — Economic & Financial Affairs Meetings | Yes | No | No | Off; summarize | eu-policy/finance-calendar |
| Finance | 04 — Optional — Global Data & Research | Eurogroup — Meetings | Yes | No | No | Off; summarize | euro-area/finance-calendar |
| Finance | 04 — Optional — Global Data & Research | European Council — Meetings | Yes | Yes | Yes | Off; summarize | eu-policy/strategic-calendar |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Council of the EU — Justice & Home Affairs Meetings | Yes | No | No | Off; summarize | eu-security/justice-calendar |
| Finance | 04 — Optional — Global Data & Research | Council of the EU — Transport, Telecommunications & Energy Meetings | Yes | No | No | Off; summarize | eu-policy/energy-digital-calendar |
| Finance | 04 — Optional — Global Data & Research | UK Government — National Security News & Communications | Yes | No | No | Off; summarize | national-security/economic-security |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | UK Government — Cyber Security News & Communications | Yes | No | No | Off; summarize | cyber/policy |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | UK Government — Cyber Security Research & Statistics | Yes | No | No | Off; summarize | cyber/research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | UK Government — Cyber Security Policy Papers & Consultations | Yes | No | No | Off; summarize | cyber/regulation-policy |
| Finance | 04 — Optional — Global Data & Research | European Commission Representation in Ireland — News | Yes | No | No | Off; summarize | eu/ireland-policy |
| Finance | 03 — Optional — Data, Ireland, EU & UK | ComReg — News and Publications | Yes | No | No | Off; summarize | ireland/telecoms-regulation |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Houses of the Oireachtas — Press Releases | Yes | No | No | Off; summarize | ireland/parliamentary-policy |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Houses of the Oireachtas — Dáil Schedule | Yes | No | No | Off; summarize | ireland/parliamentary-calendar |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Houses of the Oireachtas — Seanad Schedule | Yes | No | No | Off; summarize | ireland/parliamentary-calendar |
| Finance | 03 — Optional — Data, Ireland, EU & UK | Houses of the Oireachtas — Committee Schedule | Yes | No | No | Off; summarize | ireland/parliamentary-oversight-calendar |
| Finance | 04 — Optional — Global Data & Research | European Union Agency for Fundamental Rights — Publications | Yes | No | No | Off; summarize | fundamental-rights/digital-governance-research |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | eu-LISA — News and Updates | Yes | No | No | Off; summarize | eu-large-scale-it-systems/cyber-resilience |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | eu-LISA — Publications | Yes | No | No | Off; summarize | eu-it-systems/digital-resilience-research |
| Cyber Security | 01 — Core — Ireland, EU & Official Alerts | Canadian Centre for Cyber Security — Alerts & Advisories | Yes | No | No | Off; summarize | cyber/official-advisories |
| Cyber Security | 04 — Optional — Specialist Alerts & Research | Canadian Centre for Cyber Security — Guidance, News & Events | Yes | No | No | Off; summarize | cyber/guidance-and-resilience |
| Finance | 04 — Optional — Global Data & Research | Japan Securities and Exchange Surveillance Commission — Press Releases | Yes | No | No | Off; summarize | securities-supervision/market-conduct |
| Finance | 04 — Optional — Global Data & Research | Federal Register — OFAC Sanctions Notices | Yes | No | No | Off; summarize | sanctions/official-notice |
| Finance | 04 — Optional — Global Data & Research | Federal Register — FinCEN AML & Financial-Crime Notices | Yes | No | No | Off; summarize | aml-financial-crime/official-notice |
| Finance | 04 — Optional — Global Data & Research | Federal Register — OCC Banking Rules & Notices | Yes | No | No | Off; summarize | banking-regulation/official-notice |

## Import checklist

1. Import exactly one profile: the **iPhone Air** OPML as the default, the Lite OPML for constrained connections, or the **Master** OPML for full coverage.
2. NetNewsWire adds imported feeds to the current subscription list; remove or separate an older copy before importing if you are replacing a previous bundle.
3. Apply **On** only to the four urgent official alert feeds unless your operating needs justify more interruptions.
4. Review **Optional** feeds after import; leave them off during normal use.
5. Leave **Off** feeds notification-disabled and process them in the daily digest.
6. Re-check this matrix after any manifest change; the generated OPML and source tables should be regenerated together.

See [NetNewsWire setup and notification plan](../../docs/NetNewsWire-Setup-and-Notification-Plan.md) for the operating rationale and [daily digest workflow](../../docs/NetNewsWire-Daily-Digest-Workflow.md) for batch review.
