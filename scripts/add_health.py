with open('backend/app/main.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '@app.get("/api/health")'
replacement = '@app.get("/api/health")\n@app.get("/health")\n@app.get("/")'

if '@app.get("/health")' not in code:
    code = code.replace(target, replacement, 1)
    with open('backend/app/main.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Health alias added successfully")
else:
    print("Health alias already present")
