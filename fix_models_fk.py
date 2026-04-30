import re
with open('app/models/all_models.py', 'r') as f:
    content = f.read()

content = re.sub(r"ForeignKey\('([^p][^y][^s][^\.]*\.[^\']+)'\)", r"ForeignKey('pyspace_\1')", content)

with open('app/models/all_models.py', 'w') as f:
    f.write(content)
