import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
class Quote:

	def __init__(self,author,birthday,text,birth_loc):
		self.author = author
		self.birthday = birthday
		self.text = text
		self.birth_loc = birth_loc


	def __repr__(self):
		return f"{self.author} who has born {self.birthday} in {self.birth_loc} say: \n {self.text}"


def scrape(base_url,result,url=""):

	'''
	get a url and list of results and get data from scraping and construct Quote class and append it to result and return result
	if there is next page scrape call the function recursively
	sleep 2 second before each requests
	'''

	# sleep(1)
	respond = requests.get(base_url+url).text
	soup = BeautifulSoup(respond,"html.parser")
	next_page = soup.select('.next')
	quotes = soup.select(".quote")
	for q in quotes:
		text = q.findChild('span', {'class':'text'}).get_text()
		author = q.findChild('small', {'class':'author'}).get_text()
		href = q.findChild('small', {'class':'author'}).findNextSibling()['href']
		sleep(1)
		res = requests.get(base_url+href).text
		soup = BeautifulSoup(res,'html.parser')
		try:
			#some of the pages was filtered by iranian government so i wanted to prevent any kind of error
			birthday = soup.select('.author-born-date')[0]
			location = birthday.findNextSibling().get_text()
			birthday = birthday.get_text()
		except:
			birthday = "unkown"
			location = 'unkown'
		quote = Quote(author,birthday,text,location)
		result.append(quote)
	if len(next_page) != 0:
		next_page = next_page[0].findChild('a')['href']
		result = scrape(base_url,result,next_page)
	return result

def game(result):
	'''
	get a list of quotes and choose 1 from it and loop 4 time and each time gives a hint
	after that ask do u wanna play again and return true false according to that
	'''
	count = 0
	q = choice(result)
	print(f'Who said this: {q.text}')
	while count < 4:
		answer = input("Enter ur guess: ")
		if answer.lower() == q.author.lower():
			print('Thats Correct')
			break
		else:
			if count == 0:
				print(f'the author was born in {q.birthday} in {q.birth_loc}')
			elif count == 1:
				print(f'the author first name start with {q.author[0]}')
			elif count == 2:
				lastname = q.author.split(" ")[-1]
				print(f"the author last name start with {lastname[0]}")
			elif count == 3:
				print(f'The correct answer was {q.author}')
		count += 1
	print(q)
	answer = ''
	while answer.lower() not in ('yes','y','no','n'):
		answer = input('do u want to play again?')
	if answer == 'yes' or answer == 'y':
		return True
	elif answer == 'no' or answer == 'n':
		return False



if __name__=="__main__":
	URL = 'http://quotes.toscrape.com'
	print(f"It gonna take some time to scrape all the pages from {URL} please be patient")
	result = []
	result = scrape(URL,result)
	want_to_play = True
	while want_to_play:
		want_to_play = game(result)
