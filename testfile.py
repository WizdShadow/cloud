import bcrypt
from datetime import datetime
parol = "vivapro12"
let = bcrypt.hashpw(parol.encode('utf-8'), bcrypt.gensalt())
print(let[29])
print(let)