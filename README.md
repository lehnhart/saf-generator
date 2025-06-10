# DSpace SAF Generator

Este é um aplicativo Flask que gera arquivos no formato Simple Archive Format (SAF), que possibilita realizar a importação em lote no [Aplicativo DSpace](https://dspace.org/).

Acesse o aplicativo: [Aplicativo SAF Generator Web](https://saf.waydigital.com.br)

Veja mais na [Documentação DSpace](https://wiki.lyrasis.org/display/DSDOC8x/Importing+and+Exporting+Items+via+Simple+Archive+Format)

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Flask
- Pandas
- LXML

## Instalação

1. Clone este repositório
2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Inicie o servidor Flask:
   ```bash
   python app.py
   ```
2. Acesse http://localhost:5000 no seu navegador
3. Faça upload do arquivo CSV e dos arquivos PDFs correspondentes
4. Clique em "Gerar SAF" para criar o arquivo archive.zip

## Formato do CSV

O arquivo CSV deve ser salvo no formato UTF-8, utilizando a vírgula (,) como separador. Não utilizar ponto-e-vírgula (;).

Exemplo de colunas do arquivo CSV:

- dc.title: Título do documento.
- dc.creator: Autor(es) do documento.
- dc.date.issued: Data de publicação.
- dc.description.abstract: Resumo do documento.
- filename: Nome exato do arquivo PDF que será carredo.

Exemplo:
```csv
dc.title,dc.creator,dc.date.issued,dc.description.abstract,filename
Título do Documento,Nome do Autor,20-03-2025,"Resumo do documento",Nome-Exato-do-Arquivo.pdf
```

## Importação no DSpace

1. Acesse a interface administrativa do DSpace
2. Vá para "Administração" > "Importação em Lote"
3. Faça upload do arquivo archive.zip gerado
4. Siga as instruções na tela para completar a importação 