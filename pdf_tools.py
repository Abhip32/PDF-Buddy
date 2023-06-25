import os, zipfile, PyPDF2

def merge(files):
    pdfWriter = PyPDF2.PdfFileWriter()
    for pdf in files:
        pdfReader = PyPDF2.PdfFileReader(pdf)
        for page in range(pdfReader.numPages):
            pdfWriter.addPage(pdfReader.getPage(page))
    pdfOutput = open('output.pdf', 'wb')
    pdfWriter.write(pdfOutput)
    pdfOutput.close()

def split(pdf, rangeList, pageList):
    
    try:
        os.remove('new.zip')
    except FileNotFoundError:
        pass

    pdfReader = PyPDF2.PdfFileReader(pdf)
    downloadZip = zipfile.ZipFile('new.zip', 'a')
    added = False
    for lst in rangeList:
        pdfWriter = PyPDF2.PdfFileWriter()
        if lst[0] <= pdfReader.numPages and lst[1] <= pdfReader.numPages:
            added = True
            for pageNo in range(lst[0]-1, lst[1]):
                pdfWriter.addPage(pdfReader.getPage(pageNo))
            pdfOutput = open('temp/output' + str(lst[0]) + str(lst[1]) + '.pdf', 'wb')
            pdfWriter.write(pdfOutput)
            pdfOutput.close()
            downloadZip.write(pdfOutput.name, compress_type=zipfile.ZIP_DEFLATED)
    
    for page in pageList:
        pdfWriter = PyPDF2.PdfFileWriter()
        if page <= pdfReader.numPages:
            added = True
            pdfWriter.addPage(pdfReader.getPage(page-1))
        pdfOutput = open('temp/output' + str(page) + '.pdf', 'wb')
        pdfWriter.write(pdfOutput)
        pdfOutput.close()
        downloadZip.write(pdfOutput.name, compress_type=zipfile.ZIP_DEFLATED)

    downloadZip.close()
    for pdf in os.listdir('temp'):
        os.remove('temp/' + pdf)

    return added

def remove(pdf, matches):
    pdfReader = PyPDF2.PdfFileReader(pdf)
    pdfWriter = PyPDF2.PdfFileWriter()
    i=0
    removed = False
    for pageNo in range(pdfReader.numPages):
        if i < len(matches) and matches[i] == pageNo + 1:
            i += 1
            removed = True
            continue
        pdfWriter.addPage(pdfReader.getPage(pageNo))
    pdfOutput = open('output.pdf', 'wb')
    pdfWriter.write(pdfOutput)
    pdfOutput.close()
    return removed

def rotate(pdf, degree):
    pdfReader = PyPDF2.PdfFileReader(pdf)
    pdfWriter = PyPDF2.PdfFileWriter()
    for pageNo in range(pdfReader.numPages):
        page = pdfReader.getPage(pageNo)
        page.rotateClockwise(degree)
        pdfWriter.addPage(page)
    pdfOutput = open('output.pdf', 'wb')
    pdfWriter.write(pdfOutput)
    pdfOutput.close()

def watermark(pdf, watermark_file, typ):
    pdfReader = PyPDF2.PdfFileReader(pdf)
    watermarkReader = PyPDF2.PdfFileReader(watermark_file)
    pdfWriter = PyPDF2.PdfFileWriter()
    pageObj = watermarkReader.getPage(0)
    if typ == 'first':
        page = pdfReader.getPage(0)
        page.mergePage(pageObj)
        pdfWriter.addPage(page)
        for pageNo in range(1, pdfReader.getNumPages()):
            pdfWriter.addPage(pdfReader.getPage(pageNo))
    elif typ == 'all':
        for pageNo in range(pdfReader.getNumPages()):
            page = pdfReader.getPage(pageNo)
            page.mergePage(pageObj)
            pdfWriter.addPage(page)
    pdfOutput = open('output.pdf', 'wb')
    pdfWriter.write(pdfOutput)
    pdfOutput.close()

def encrypt(pdf, password):
    pdfReader = PyPDF2.PdfFileReader(pdf)
    pdfWriter = PyPDF2.PdfFileWriter()
    for pageNo in range(pdfReader.getNumPages()):
        pdfWriter.addPage(pdfReader.getPage(pageNo))
    pdfWriter.encrypt(password)
    pdfOutput = open('output.pdf', 'wb')
    pdfWriter.write(pdfOutput)
    pdfOutput.close()