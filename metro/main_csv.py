
import csv
import json
import sys
sys.path.append("/home/gardusi/github/sql_library")
from sql_json import mySQL


def build_result(file):
	global db_i
	csv_reader = csv.reader(file, delimiter=';')
	line_count = 0
	result = []
	months = []
	for row in csv_reader:
		data = {}
		if line_count == 0:
			months = row[9:]
			for month in months:
				db_i[month] = 'INT'
		else:
			data = {
				"Estado": row[0],
				"Cidade": row[1],
				"Anel": row[2],
				"Speed": float(row[3]),
				"Informacao": row[4].encode('utf-8'),
				"Traffic_100%": percent_to_int(row[5]),
				"Traffic_95%": percent_to_int(row[6]),
				"Traffic_Gbps": float(row[7].replace(',','.')),
				"TX": percent_to_int(row[8])
			}
			for idx, m in enumerate(months):
				data[m] = percent_to_int(row[idx+9])
			result.append(data)
		line_count += 1
	return result


def db_inserction(filepath, db_name, tb_name, docs):
	global db_i
	credentials = read_json(filepath)
	db = mySQL(credentials, db_name)
	print(db_i)
	db.create_table(tb_name, db_i)
	db.insert_into(tb_name, db_i, docs)


def main():
	global db_i
	db_i = read_json("/home/otsuka/doing/metro/files/table_info.json")
	files = read_json("/home/otsuka/doing/metro/files/config.json")
	items = open_file(files["csv_filepath"], build_result)
	db_inserction(
		files["database_credentials"],
		files["database_name"],
		files["table_name"],
		items
	)


def open_file(file_path, fun_kappa):
	with open(file_path, "r", encoding='ISO-8859-1') as file:
		return fun_kappa(file)


def percent_to_int(string):
	return int(string[:-1])


def read_json(filepath):
	with open(filepath, 'rb') as file:
		return json.load(file, encoding = 'utf-8')


if __name__ == '__main__':
	main()
