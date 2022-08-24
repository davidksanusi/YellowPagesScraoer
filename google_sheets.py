import gspread


gc = gspread.service_account(filename="/Users/David/PycharmProjects/yp-scraper/creds.json")
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1m3S0MgCRZxXp1aG-em2Fzovnf1hABfJ4BGrY3p95p0s/edit#gid=105903045').get_worksheet(8)
sh2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1m3S0MgCRZxXp1aG-em2Fzovnf1hABfJ4BGrY3p95p0s/edit#gid=105903045').get_worksheet(9)

print(sh)