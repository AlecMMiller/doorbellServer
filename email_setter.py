from uidTableModule import getTable, uidTable, uid, MAX_UID
from validate_email import validate_email

table = getTable()

# What UID are we setting the email for?
while True:
    try:
        raw = raw_input("Enter UID: ")
        uid = int(raw)
    except ValueError, NameError:
        print("UID must be integer")
        continue
    if(uid > MAX_UID or uid < 1):
        print("Valid UIDs must be between 1 and " + str(MAX_UID))
        continue
    if(table.validate(uid) is False):
        continue
    break

# Set the email
while True:    
    email = raw_input("Enter email: ")
    if(validate_email(email)):
       table.setEmail(uid, email) 
       break
    else:
       print(email + " is not a valid email address")
        
