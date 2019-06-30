import requests
from bs4 import BeautifulSoup
import csv

def add(name,data):

	with open(name, mode='a') as csv_file:
		fieldnames = ['ASIN','Reviews','Price','Title']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writerow(data)

url=input('Enter url to extract data:-')
url=url.strip()
u=url.split('=')[1].split('&')[0].replace('+' ,'_')+'.csv'
details={}
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
r=requests.get(url=url,headers=headers)
html=r.content
soup=BeautifulSoup(html,'lxml')
products=soup.find_all('div',{'class':'s-result-item'})
print('Scraping url :-'+url)
if products:
	
	
	for product in products:
		try:
			price=product.find('span',{'class':'a-offscreen'})
			details['Reviews']=0
			reviews=product.find('span',{'class':'a-size-base'})
			asin=product.find('a',{'class':'a-link-normal a-text-normal'})
			title=asin
			carousel=product.find_all('li',{'class':'a-carousel-card'})
			top=product.find_all('div',{'class':'s-result-item'})
		except Exception as e:
			print(e)
		try:
			if asin.get('href').split('/')[-2] != 'picassoRedirect.html' and not carousel:
			
				details['Title']=title.text.encode("utf-8")
				details['ASIN']=asin.get('href').split('/')[-2]
				if price :
					details['Price']=price.text.split('$')[1]
				else:
					try:
						details['Price']=product.find('div',{'class':'a-section a-spacing-none a-spacing-top-mini'}).text.strip().split('$')[-1].strip().split('(')[0].strip()
					except:
						details['Price']='Free'
						continue
				if reviews :
					try:
						details['Reviews']=int(reviews.text.replace(',',''))
					except:
						try:
							ff=product.find_all('a',{'class':'a-link-normal'})
							details['Reviews']=int(ff[2].text.replace(',',''))
						except:
							pass
					
				else:
					details['Reviews']=0
				add(u,details)
				print('ADDED--> ASIN:- '+details['ASIN']+' Reviews:- '+str(details['Reviews'])+'\t Price :-$'+details['Price'])
			elif carousel and not top:
				print('Found Carousel....Scraping from Carousel..')
				for i in carousel:
					try:
						cprice=i.find_all('span',{'class':'a-offscreen'})
						creviews=i.find('span',{'class':'a-size-base'})
						casin=i.find('a',{'class':'a-link-normal a-text-normal'})
					except:
						continue
					try:
						if casin:
							if casin.get('href').split('/')[-2] != 'picassoRedirect.html':

				
								details['Title']=casin.text.encode("utf-8")
								details['ASIN']=casin.get('href').split('/')[-2]
								if price :
									try:
										details['Price']=cprice[0].text.split('$')[1]
									except:
										try:
											details['Price']=cprice[1].text.split('$')[1]
										except:
											continue

								else:
									try:
										details['Price']=i.find('div',{'class':'a-section a-spacing-none a-spacing-top-mini'}).text.strip().split('$')[-1].strip().split('(')[0].strip()
									except:
										details['Price']='Free'
										continue
								if creviews :
									try:
										details['Reviews']=int(creviews.text.replace(',',''))
									except:
										details['Reviews']=0
								else:
									details['Reviews']=0
								add(u,details)
								print('ADDED--> ASIN:- '+details['ASIN']+' Reviews:- '+str(details['Reviews'])+'\t Price :-$'+details['Price'])
					except Exception as e:
						print(e)
		
						
		except Exception as e:
			print(e)

else:
	print('Possible Errors:-\nCheck Internet Connection\nCheck if url has products')


