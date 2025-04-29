import os
import shutil
import tempfile
import zipfile
from flask import Flask, request, send_file, render_template
import pandas as pd
from lxml import etree

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        temp_dir = tempfile.mkdtemp()
        upload_dir = os.path.join(temp_dir, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        try:
            if 'csv' not in request.files or 'pdfs' not in request.files:
                return 'Arquivo CSV e PDF são obrigatórios.', 400

            csv_file = request.files['csv']
            pdf_files = request.files.getlist('pdfs')

            # Salvar PDFs dentro da pasta uploads/
            for pdf in pdf_files:
                pdf_path = os.path.join(upload_dir, pdf.filename)
                pdf.save(os.path.abspath(pdf_path))  # Forçar gravação correta

            # Ler CSV
            try:
                df = pd.read_csv(csv_file, encoding='utf-8')
            except UnicodeDecodeError:
                csv_file.seek(0)
                df = pd.read_csv(csv_file, encoding='latin1')

            if df.empty or len(df.columns) == 0:
                return 'O arquivo CSV enviado está vazio ou inválido.', 400

            # Criar pasta para cada item
            for i, (_, row) in enumerate(df.iterrows()):
                item_dir = os.path.join(temp_dir, f'item_{i}')
                os.makedirs(item_dir, exist_ok=True)

                # Criar dublin_core.xml
                dc_root = etree.Element('dublin_core', schema='dc')

                for col in df.columns:
                    if pd.isna(row[col]) or col.lower() == 'filename':
                        continue

                    parts = col.split('.')
                    element = parts[1] if len(parts) > 1 else ''
                    qualifier = parts[2] if len(parts) > 2 else None

                    attribs = {'element': element}
                    if qualifier:
                        attribs['qualifier'] = qualifier

                    '''
                    elem = etree.SubElement(dc_root, 'dcvalue', **attribs)
                    elem.text = str(row[col])
                    '''
                    valores = str(row[col]).split('||')
                    for valor in valores:
                        valor = valor.strip()
                        if valor:
                            elem = etree.SubElement(dc_root, 'dcvalue', **attribs)
                            elem.text = valor

                dublin_core_path = os.path.join(item_dir, 'dublin_core.xml')
                tree = etree.ElementTree(dc_root)
                tree.write(dublin_core_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')

                # Copiar o PDF correto para a pasta do item
                contents_path = os.path.join(item_dir, 'contents')
                with open(contents_path, 'w') as f:
                    pdf_filename = row.get('filename')
                    if pdf_filename:
                        pdf_filename = pdf_filename.strip()
                        src_pdf_path = os.path.join(upload_dir, pdf_filename)
                        if os.path.exists(src_pdf_path):
                            dest_pdf_path = os.path.join(item_dir, pdf_filename)
                            shutil.copy2(src_pdf_path, dest_pdf_path)  # Usar copy2 (mantém metadata)
                            f.write(f'{pdf_filename}\n')
                        else:
                            print(f"WARNING: PDF '{pdf_filename}' não encontrado nos uploads!")

            # Criar arquivo ZIP final
            output_zip = os.path.join(temp_dir, 'archive.zip')
            with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    if upload_dir in root:  # Ignorar a pasta uploads
                        continue
                    for file in files:
                        if file == 'archive.zip':
                            continue
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)

            return send_file(output_zip, as_attachment=True)

        except Exception as e:
            app.logger.error(f"Erro durante o processamento: {e}")
            return f"Ocorreu um erro: {e}", 500

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)