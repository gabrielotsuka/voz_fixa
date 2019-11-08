import subprocess
import info
from openpyxl import load_workbook

def main():
	subprocess.run(args = ["pdftotext", "teste3.pdf"])
	with open("teste3.txt", "r") as file:
		lines = info.go_through_file(file)
		num   = info.get_number(lines['notif'])
		data  = info.get_date(lines['date'])
		conc  = 'CPFL Paulista'
		tipo  = info.get_type(lines['type'])
		pst   = info.get_pst(lines['post'])
		ende  = lines['address']
		prazo = info.get_prompt(lines['prompt'], data)
		resp  = 'Laércio'
		ans   = (
			num,     data,    conc,    tipo[0],
			tipo[1], pst,     ende,    tipo[2], 
			prazo,   data,    resp 
		)
		wb = load_workbook(filename = 'teste.xlsx')
		ws = wb.get_sheet_names()[0]
		ws = wb.get_sheet_by_name(ws)
		ws.append(ans)
		wb.save('teste.xlsx')


main()