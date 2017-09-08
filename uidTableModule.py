import cPickle as pickle
from mailer import sendMail
MAX_UID = 15

uidPickle = "/share/Doorbell/table.p"

# Individual UID
class uid:

    def reset(self):
        self.isValid = False
        self.email = ""
        
    def __init__(self, ident):
        self.ident = ident
        self.reset()

    def setValid(self):
        self.isValid = True

    def release(self):
        self.reset()

    def setEmail(self, email):
        self.email = email

    def checkIsValid(self):
        return self.isValid

    def sendEmail(self, payload):
        if(self.email != ""):
            sendMail(self.email, payload)
        else:
            print("No email address for UID " + str(self.ident))

# Table of all UIDs
class uidTable:

    def __init__(self):
        self.instanceList = [ uid(i) for i in range (1, MAX_UID) ]

    def updatePickle(self):
        pickle.dump ( self, open( uidPickle , "wb" ) )
    
    def requestUid(self):
        for instance in self.instanceList:
            if (instance.checkIsValid() == False):
                instance.setValid()
                self.updatePickle()
                return instance.ident
        return 0

    def validate(self, uid):
        for instance in self.instanceList:
            if (instance.ident == uid):
                print "UID", uid, "valid:", instance.isValid
                if (instance.isValid == True):
                    return True
                else:
                    return False

    def release(self, uid):
        for instance in self.instanceList:
            if (instance.ident == uid):
                print "Releasing", uid
                instance.release()
                self.updatePickle()

    def setEmail(self, uid, email):
        for instance in self.instanceList:
            if (instance.ident == uid):
                print("Setting email for UID " + str(uid) + " to " + email)
                instance.setEmail(email)
                self.updatePickle()

    def sendEmail(self, uid, payload):
        for instance in self.instanceList:
            if (instance.ident == uid):
                instance.sendEmail(payload)

def getTable():                
    try:
        table = pickle.load(open(uidPickle, "rb"))
    except (OSError, IOError) as e:
        table = uidTable()
        pickle.dump ( table, open(uidPickle, "wb" ) )
    return table
