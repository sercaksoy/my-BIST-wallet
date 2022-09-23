import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import logging
import requests
import bs4
import sys

def timeline_df(fi):
	dates = []
	companies = []
	stock_prices = []
	for line in fi:
		parts = line[:-1].split(' ')
		if parts[2][0] == 'C':
			request_date = parts[0] + ' ' + parts[1][:5]
			dates.append(request_date)
			companies.append(parts[3])
			stock_prices.append(parts[6])
		elif parts[2] == 'TOTAL':
			request_date = parts[0] + ' ' + parts[1][:5]
			dates.append(request_date)
			companies.append('TOTAL BALANCE')
			stock_prices.append(parts[4])

	df = pd.DataFrame(list(zip(dates,companies,stock_prices)),columns=['Date','Company','StockPrice'])		
	df.StockPrice = df.StockPrice.astype(float)
	return df


def plot_figures(df):
	axes_size = len(df.Company.unique())
	fig, axes = plt.subplots(nrows=axes_size, ncols=1, figsize=(10,10))
	i = 0
	for comp in df.Company.unique():
		df_temp = df[df.Company == comp]
		axes[i].plot(df_temp.Date, df_temp.StockPrice)
		axes[i].set_ylabel(comp)
		axes[i].tick_params(axis='x', labelrotation=30, labelsize=6)
		i += 1
	plt.tight_layout()
	plt.show()

logging.basicConfig(filename="hisse.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


df = pd.read_excel('bist_wallet.xlsx', header = None)
company_dict = dict(zip(df[0],df[1]))  # df[0] is the names of companies
									   # df[1] is how much amount I own
total_try = 0

for company in company_dict.keys():
	r = requests.get('https://www.google.com/search?q='+company+'+hisse')
	data = bs4.BeautifulSoup(r.text,'html.parser')

	start_ind = data.text.find('Hisse Senedi Fiyatı') + len('Hisse Senedi Fiyatı')
	end_ind = start_ind + 5  # xx,yy
	re_val = data.text[start_ind:end_ind]

	print(company.upper() + '  ' + re_val)
	try_val = company_dict[company] * float(re_val.strip().replace(',','.'))
	total_try += try_val
	print('Stock: ' + str(company_dict[company]) + '\tTRY VAL: ' + str(try_val))
	print()

	# Logging 
	logger.info(datetime.now())
	logger.info('COMPANY: ' + company + ' Stock Price: ' + re_val.strip().replace(',','.'))
	logger.info('Amount: ' + str(company_dict[company]))
	logger.info('in TRY: ' + str(try_val))


print()
print()
print('TOTAL TRY: ' + str(total_try))

logger.info('TOTAL BALANCE: ' + str(total_try))


if len(sys.argv) == 2:
	if sys.argv[1] == 'show':
		with open('hisse.log') as fi:
			fi = fi.readlines()

		plot_figures(timeline_df(fi))
