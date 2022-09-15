from datetime import datetime
import pandas as pd
import logging
import requests
import bs4

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
	logger.info('COMPANY: ' + company)
	logger.info('Stock Price: ' + re_val.strip().replace(',','.'))
	logger.info('Amount: ' + str(company_dict[company]))
	logger.info('in TRY: ' + str(try_val))


print()
print()
print('TOTAL TRY: ' + str(total_try))

logger.info('TOTAL BALANCE: ' + str(total_try))
