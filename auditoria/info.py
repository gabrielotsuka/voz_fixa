import calendar
import datetime as dt


def go_through_file(file):
	dictr = {}
	dictr['address'] = ''
	flags = {
		'numero' : True,
		'data'   : True,
		'tipo'   : True,
		'poste'  : True,
		'endere' : True,
		'prazo'  : True
	}	
	flagtipo = True
	flaga = False
	flags['endere'] = True

	for line in file:

		idxnum = line.find('NOTIFICAÇÃO N')
		if idxnum  != -1 and flags['numero']:
			dictr['notif']  = line
			flags['numero'] = False
		idxdate = line.find(',')

		if idxdate != -1 and flags['data']:
			dictr['date'] = line
			flags['data'] = False

		if flags['tipo']:
			idxtypea = line.find('REVELIA')
			idxtypeb = line.find('TÉCNICAS')
			if idxtypea != -1:
				dictr['type'] = True
				flags['tipo'] = False
			elif idxtypeb != -1:
				dictr['type'] = False
				flags['tipo'] = False

		idxpost = line.find('POSTES')
		if idxpost != -1 and flags['poste']:
			dictr['post']  = line
			flags['poste'] = False

		if flags['endere']:
			idxane  = line.find('ANEXO')
			idxp    = line.find('POSTES')
			if (idxane != -1):
				flaga = True
				continue
			elif (flaga and (idxp != -1)):
				flags['endere'] = False
			elif flaga and flags['endere']:
				dictr['address'] += line[:-1] + ' '

		idxprom = line.find('dias corridos')
		if idxprom != -1 and flags['prazo']:
			dictr['prompt'] = line
			flags['prazo']  = False

	return dictr


#Function that returns the number of the notification
def get_number(string):
	ans = string[15 : -6]
	ans = ans.replace(".", "")
	return ans


# Function that returns the date that was sent the notification
def get_date(string):
	months = {
		"Janeiro":   '1',
		"Fevereiro": '2',
		"Março":     '3',
		"Abril": 	 '4',
		"Maio":		 '5',
		"Junho":	 '6',
		"Julho":	 '7',
		"Agosto":	 '8',
		"Setembro":	 '9',
		"Outubro":	 '10',
		"Novembro":  '11',
		"Dezembro":  '12'
	}
	idxv    = string.find(',')
	date    = string[idxv+2:-2].split(" de ")
	date[1] = months[date[1]]
	date = '/'.join(date)
	date1 = dt.datetime.strptime(date, '%d/%m/%Y').date()
	return date1


#Get the type of the notification, the description and the proposed action to solve it
def get_type(flag_type):
	if flag_type:
		return ["À Revelia", 
				"Instalação sem Aprovação de Projeto Técnico", 
				"Apresentação de Projeto Técnico"]
	else:
		return ["Operacional", 
				"Irregularidade Técnica", 
				"Adequação"]


# Returns the quantity of posts included in the problem
def get_pst(string):
	lst = string.split(" ")
	for i in lst:
		if i.isdigit():
			return int(i)
	return


# # Return the full addres in a list, [Street, City, State]
# def get_address(string):	
# 	r = string.split(' – ')
# 	r[2] = r[2][:-2]
# 	return r

def get_address(string):
	return string

# Return the max date to solve the problem
def get_prompt(prompt, date):
	r = prompt.split(" ")
	for i in r:
		if i.isdigit():
			days = int(i)
			break
	return date + dt.timedelta(days=days)