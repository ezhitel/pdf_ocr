import pdf_tables_parse.pdf_to_images
import pdf_tables_parse.extract_tables
import pdf_tables_parse.extract_cells
import pytesseract
import os

def start(path: str, type: str) -> dict:
    files = pdf_to_images.get_images(path, type)
    headers, tables = extract_tables.main(sorted(files))
    cells = []
    for file in tables:
        for table in file:
            cells.append(extract_cells.main(table))
    ocr_data = {'headers': {},
                'data': {}}

    if type == 'mir':
        lang = 'rus'
    else:
        lang = 'eng'

    for count, _table in enumerate(cells):
        ocr_data['data'][count] = {}
        for cell in _table:
            row, column = os.path.split(cell)[-1].split(".")[0].split("-")
            if row in ocr_data['data'][count]:
                ocr_data['data'][count][row][column] = pytesseract.image_to_string(image=cell, config='--oem 1', lang=lang).strip()
            else:
                ocr_data['data'][count][row] = {}
                ocr_data['data'][count][row][column] = pytesseract.image_to_string(image=cell, config='--oem 1', lang=lang).strip()
    for count, header in enumerate(headers):
        ocr_data['headers'][count] = pytesseract.image_to_string(image=header, config='--oem 1 --psm 12', lang=lang).split('\n')
    return ocr_data

