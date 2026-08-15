# Market hours and holiday reference

Checked: 15 August 2026 (Europe/Dublin)

This is a timing aid for interpreting RSS headlines. It is not a live market-data service, order router or trading calendar API. Always confirm the instrument-specific exchange calendar before acting.

## Normal opening and closing windows

| Market | Normal local session | Europe/Dublin interpretation | Important caveat |
|---|---|---|---|
| London Stock Exchange Main Market / SETS | Continuous trading generally 08:00–16:30 Europe/London | The same clock as Dublin: 08:00–16:30 | The opening auction call is generally 07:50–08:00; the closing auction call starts at 16:30 and is normally at least five minutes, with random extensions and a post-close crossing session. Services and instruments can differ. |
| Euronext Dublin cash equities | Typical headline window about 08:00–16:30 Europe/Dublin | 08:00–16:30 Dublin time on a normal full session | Exact auction, closing and post-trade times vary by market and instrument. Use Euronext’s current trading-hours and holiday calendar; half-day equity closes can be around 12:28–12:30 Dublin time, while ETFs can close around 13:00 Dublin time. |
| NYSE / Nasdaq regular equities | 09:30–16:00 America/New_York | Usually 14:30–21:00 Dublin time | The 13:30–20:00 Dublin window occurs during the short periods when US and Irish daylight-saving changes do not line up. NYSE opening and closing auctions occur at 09:30 and 16:00 ET. |

## US extended sessions

- Nasdaq publishes pre-market trading as 04:00–09:30 ET and after-hours trading as 16:00–20:00 ET. Broker availability and eligible instruments can differ, and extended hours can have lower liquidity and higher volatility.
- These are not the same as the regular-session open or close. Do not label a pre-market headline as a regular-market move.

## 2026 Dublin conversion for the US regular session

When Ireland and New York are on the same seasonal schedule, NYSE/Nasdaq 09:30–16:00 ET is normally 14:30–21:00 in Dublin.

For 2026, the temporary mismatch windows are expected to be:

- Monday 9 March through Friday 27 March: 13:30–20:00 Dublin time.
- Monday 26 October through Friday 30 October: 13:30–20:00 Dublin time.

The dates change each year. Recalculate from the exchange and local time-zone calendars rather than hard-coding these dates into an alert rule.

## Holidays, early closes and auctions

- US equity markets can be closed or close early for US holidays. For 2026, Nasdaq and NYSE list early closes at 13:00 ET on the day after Thanksgiving and on Christmas Eve; the official calendars control if an exception or additional session is announced.
- London and Euronext calendars have their own UK, Irish and European holidays, substitute days and half-days. A market can be open in one country while another is closed.
- An “open” headline, opening auction, continuous trading session, closing auction and post-close reporting window are different states. Summaries must name the state when the source provides it.
- Market holidays, half-days, auction extensions, trading suspensions and halts override normal clock times.

## Official references

- [Nasdaq trading schedule and holiday hours](https://www.nasdaq.com/market-activity/stock-market-holiday-schedule)
- [NYSE holidays and trading hours](https://www.nyse.com/trade/hours-calendars)
- [London Stock Exchange business days](https://www.londonstockexchange.com/trade/trading-access/business-days)
- [London Stock Exchange retail guide with SETS auction phases](https://docs.londonstockexchange.com/sites/default/files/documents/lse-retail.pdf)
- [Euronext trading hours and holidays](https://www.euronext.com/en/trading/trading-hours-holidays)

## RSS boundary

The RSS bundle can surface trade-halt notices, news and official releases. It does not provide live quotes, order books, broker execution, portfolio positions or trade IDs. Use a broker or dedicated exchange-data application for live trading information, and do not turn a headline into a buy/sell instruction.
