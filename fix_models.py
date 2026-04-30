import re
with open('app/models/all_models.py', 'r') as f:
    content = f.read()

content = re.sub(r"__tablename__ = '([^p][^y][^s].*)'", r"__tablename__ = 'pyspace_\1'", content)

with open('app/models/all_models.py', 'w') as f:
    f.write(content)
