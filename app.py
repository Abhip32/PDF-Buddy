import re, smtplib
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pdf_tools import merge, split, remove, rotate, watermark, encrypt,merge_images_to_pdf
from docx2pdf import convert
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['MAX_CONTENT_LENGTH'] = 40 * 1024 * 1024

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/merge_pdf', methods=['GET', 'POST'])
def merge_pdf():
    error = None
    if request.method == 'POST':
        files = request.files.getlist("files")
        if len(files) > 1:
            merge(files)
            return send_file('output.pdf', as_attachment=True)
        else:
            error = 'Please upload more than one file for merging'
    return render_template('pdf/merge_pdf.html', error = error)

@app.route('/split_pdf', methods=['GET', 'POST'])
def split_pdf():
    error = None
    if request.method == 'POST':
        pdf = request.files['file']
        ranges = request.form.get('range')

        regexObj = re.compile(r'\d+-\d+|\d+')
        matches = regexObj.findall(ranges)

        range_list = []
        page_list = []
        
        for match in matches:
            if '-' in match:
                left, right = match.split('-')
                if int(left) < int(right):
                    range_list.append([int(left), int(right)])
            else:
                page_list.append(int(match))

        if range_list == [] and page_list == []:
            error = 'Invalid range specification'
        else:
            if split(pdf, range_list, page_list):
                return send_file('new.zip', as_attachment=True, mimetype='zip')
            else:
                error = 'Invalid pages specified'
    return render_template('pdf/split_pdf.html', error = error)

@app.route('/remove_pages', methods=['GET', 'POST'])
def remove_pages():
    error = None
    if request.method == 'POST':
        pdf = request.files['file']
        ranges = request.form.get('range')

        regexObj = re.compile(r'\d+-\d+|\d+')
        matches = regexObj.findall(ranges)
        
        #expand the page ranges 
        only_pages = []
        for match in matches:
            if '-' in match:
                left, right = match.split('-')
                if int(left) < int(right):
                    for num in range(int(left), int(right)+1):
                        only_pages.append(num)
            else:
                only_pages.append(int(match))

        if only_pages == []:
            error = 'Invalid range specification'
        else:
            #sort the list
            matches = sorted(set(only_pages))
            if remove(pdf, matches):
                return send_file('output.pdf', as_attachment=True)
            else:
                error = 'Invalid pages specified'
    return render_template('pdf/remove_pages.html', error = error)

@app.route('/rotate_pdf', methods=['GET', 'POST'])
def rotate_pdf():
    if request.method == 'POST':
        pdf = request.files['file']
        degree = int(request.form.get('degreeOfRotation'))
        rotate(pdf, degree)
        return send_file('output.pdf', as_attachment=True)
    return render_template('pdf/rotate_pdf.html')

@app.route('/watermark_pdf', methods=['GET', 'POST'])
def watermark_pdf():
    if request.method == 'POST':
        pdf = request.files['file']
        watermark_file = request.files['watermark_file']
        pages = request.form.get('typeOfWatermark')
        watermark(pdf, watermark_file, pages)
        return send_file('output.pdf', as_attachment=True)
    return render_template('pdf/watermark_pdf.html')

@app.route('/encrypt_pdf', methods=['GET', 'POST'])
def encrypt_pdf():
    if request.method == 'POST':
        pdf = request.files['file']
        password = request.form.get('password')
        encrypt(pdf, password)
        return send_file('output.pdf', as_attachment=True)
    return render_template('pdf/encrypt_pdf.html')

@app.route('/merge_images', methods=['GET', 'POST'])
def image_pdf():
    if request.method == 'POST':
        files = request.files.getlist("filesImages")
        if len(files) > 1:
            merge_images_to_pdf(files)
            return send_file('output.pdf', as_attachment=True)
        else:
            error = 'Please upload more than one file for merging'
    return render_template('pdf/merge_images.html')





if __name__ == '__main__':
    app.run(debug=True)