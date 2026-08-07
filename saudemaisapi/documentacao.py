import json

from saudemaisapi.app import app

# 1. Pega os dados do OpenAPI gerados pelo FastAPI
openapi_data = json.dumps(app.openapi(), ensure_ascii=False)

# 2. Monta o HTML estático completo do ReDoc
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>{app.title} - Documentação</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>
      body {{
        margin: 0;
        padding: 0;
      }}
    </style>
</head>
<body>
    <div id="redoc-container"></div>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
    <script>
        const spec = {openapi_data};
        Redoc.init(
            spec,
            {{
                expandResponses: '200,201',
                hideDownloadButton: false,
                theme: {{
                    colors: {{
                        primary: {{
                            main: '#0066cc'
                        }}
                    }}
                }}
            }},
            document.getElementById('redoc-container')
        );
    </script>
</body>
</html>
"""

# 3. Salva o arquivo estático
with open("documentacao.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Documentação estilo ReDoc gerada com sucesso em 'documentacao.html'!")
