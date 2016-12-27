from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.FSM import FSM
from direct.distributed.PyDatagram import *
from toontown.toon.ToonDNA import ToonDNA
from toontown.makeatoon.NameGenerator import NameGenerator
from toontown.toonbase import TTLocalizer
from otp.distributed import OtpDoGlobals
from toontown.uberdog.BanManagerUD import BanManagerUD
from toontown.uberdog.AccountFirewallUD import AccountFirewallUD
from sys import platform
from toontown.toontowngui import TTDialog
from toontown.toontowngui import FeatureComingSoonDialog
from toontown.uberdog.LoginQueue import LoginQueue
import dumbdbm
import anydbm
import time
import hmac
import hashlib
import json

def judgeName(name):
    FeatureComingSoonDialog.FeatureComingSoonDialog()
    #Do name checking here
    #For now, just block every name they try typing in
    return False

REPORT_REASONS = [
    'MODERATION_FOUL_LANGUAGE', 'MODERATION_PERSONAL_INFO',
    'MODERATION_RUDE_BEHAVIOR', 'MODERATION_BAD_NAME', 'MODERATION_HACKING',
]

# --- ACCOUNT DATABASES ---
class LocalAccountDB:

    def __init__(self, csm):
        self.csm = csm

        # This uses dbm, so we open the DB file:
        filename = simbase.config.GetString('accountdb-local-file',
                                            'astron/databases/accounts.db')
        if platform == 'darwin':
            self.dbm = dumbdbm.open(filename, 'c')
        else:
            self.dbm = anydbm.open(filename, 'c')

    def lookup(self, cookie, callback):
        #if cookie.startswith('.'):
            # Beginning a cookie with . symbolizes "invalid"
        #    callback({'success': False,
        #              'reason': 'Invalid cookie specified!'})
        #    return

        #if cookie.__len__() != 64:
        #    callback({'success': False,
        #              'reason': 'False Cookie Specified. Gosh Darn Hacker!'})
        #    return
            
        #allowedCookies = ["39eaf8ca684f95bbbd841691305b2be150dd34509d9f6c1d1343b986c987646c","6a8725093e29506cb1ae8e21b45ad6bc365041f733ec7dad62be2e087eb18894","506039c9182578e57ae050ab2cba7757eabeac12bc6e67c79ff21a371b301cd6","8dea1140bc5b6b236cfc658d583618630bb635df864d3d6b2d7d5364893b89de","8b2d58084626f9221e49b334f783cc251f761c5e53b0d3248a1fa9a8188ba70b","eec636493d53fec138bc701dfd61cb3a874e64caf36fa56dbc5c3d30d02e7148","3f23b7a9a2806125d894c18dc702f23dcc4c3abb869f4dedff53caac13ee893a","bbb092b50878601e8e11ad9b4d4ce02e38552dc43db03f262f5d3e1735babab7","40baf9e4780824c61aaef25c168f40b05a20acaa8ca36edf1d2c5d207532f75a","b15b0f34aa2bd87f265b69b8d2a787102112a63e1ca46edfe224835d43d8c638","08a00edb3699187c7c1e6a528397f0451318c94372cf4eeedd731090a96f31fc","4fd20119f90159c867d1523a345b1e7bd4c8534f1564461dc3fbc211f5b5d33c","fea51b3ce2d96a84e36c90681ab2dcbf2b262923754a0ec304abc099c045cae4","e7430f6b3bb996d0718df07765c42909ee7be137cb12f836a54ed388525b69a7","39eaf8ca684f95bbbd841691305b2be150dd34509d9f6c1d1343b986c987646c"]
        
        #if cookie not in allowedCookies:
            # Cookies should be exactly 64 Characters long!
            #callback({'success': False,
             #         'reason': 'Toontown: Project Altis is currently in Whitelist mode! Please try again later!'})
            #return
            
        # IF I WANT TO BE BITCHEY, I CAN WRITE A LOOKUP HERE TO MAKE SURE THAT THE PLAYCOOKIE IS ACTUALLY IN OUR ACCOUNTS DB, BUT THAT'S NOT NEEDED FOR ALPHA

        # SECONDARILY, HERE'S WHERE WE CAN SPIN OFF TO DUBRARI'S "TOON GUARD" SYSTEM TO ENSURE THAT THE RIGHT IP IS LOGGING INTO THE ACCOUNT, AGAIN, NOT NEEDED FOR ALPHA
        
        # See if the cookie is in the DBM:

        if cookie in self.dbm:
            # Return it w/ account ID!
            import urllib2
            # As account is already in DBM, we need to CHECK it's level
            url = "http://gs1.projectaltis.com/Dubrari/powerCheck.php?token="+str(cookie)
            output = urllib2.urlopen(url).read()
            callback({'success': True,
                      'accountId': int(self.dbm[cookie]),
                      'databaseId': cookie,
                      'adminAccess': int(output)})
        else:
            # Nope, let's return w/o account ID:
            import urllib2
            # As account is being created with access 150, we need to tell level DB that it's level for checking later
            url = "http://gs1.projectaltis.com/Dubrari/powerCreate.php?token="+str(cookie)+"&level=150"
            output = urllib2.urlopen(url).read()
            callback({'success': True,
                      'accountId': 0,
                      'databaseId': cookie,
                      'adminAccess': 150})

    def storeAccountID(self, databaseId, accountId, callback):
        self.dbm[databaseId] = str(accountId)
        if getattr(self.dbm, 'sync', None):
            self.dbm.sync()
        callback()

class RemoteAccountDB:
    def __init__(self, csm):
        self.csm = csm

        self.http = HTTPClient()
        self.http.setVerifySsl(0) # Whatever OS certs my laptop trusts with panda doesn't include ours. whatever

    def lookup(self, cookie, callback):
        response = self.__executeHttpRequest("verify/%s" % cookie, cookie)
        if not response:
            callback({'success': False,
                      'reason': 'Account server failed to respond properly.'})
        elif (not response.get('status') or not response.get('valid')): # status will be false if there's an hmac error, for example
            callback({'success': False,
                      'reason': response.get('banner', 'Failed for unknown reason')})
        else:
            gsUserId = response.get('gs_user_id', -1)
            if (gsUserId == -1):
                gsUserId = 0
            callback({'success': True,
                      'databaseId': response['user_id'],
                      'accountId': gsUserId,
                      'adminAccess': response['adminAccess']})
    def storeAccountID(self, databaseId, accountId, callback):
        response = self.__executeHttpRequest("associate_user/%s/with/%s" % (databaseId, accountId), str(databaseId) + str(accountId))
        if not response:
            self.csm.notify.warning("Unable to set accountId with account server. No response!")
            callback(False)
        elif (not response.get('success')):
            self.csm.notify.warning("Unable to set accountId with account server! Message: %s" % response.get('banner', '[NON-PRESENT]'))
            callback(False)
        else:
            callback(True)


# Constants used by the naming FSM:
WISHNAME_LOCKED = 0
WISHNAME_OPEN = 1
WISHNAME_PENDING = 2
WISHNAME_APPROVED = 3
WISHNAME_REJECTED = 4

# --- FSMs ---
class OperationFSM(FSM):
    TARGET_CONNECTION = False

    def __init__(self, csm, target):
        self.csm = csm
        self.target = target
        FSM.__init__(self, self.__class__.__name__)

    def enterKill(self, reason=''):
        if self.TARGET_CONNECTION:
            self.csm.killConnection(self.target, reason)
        else:
            self.csm.killAccount(self.target, reason)
        self.demand('Off')

    def enterOff(self):
        if self.TARGET_CONNECTION:
            del self.csm.connection2fsm[self.target]
        else:
            del self.csm.account2fsm[self.target]

class LoginAccountFSM(OperationFSM):
    TARGET_CONNECTION = True
    notify = directNotify.newCategory('LoginAccountFSM')

    def enterStart(self, cookie):
        self.cookie = cookie

        self.demand('QueryAccountDB')

    def enterQueryAccountDB(self):
        self.csm.accountDB.lookup(self.cookie, self.__handleLookup)

    def __handleLookup(self, result):
        if not result.get('success'):
            self.csm.air.writeServerEvent('cookie-rejected', clientId=self.target, cookie=self.cookie)
            self.demand('Kill', result.get('reason', 'The accounts database rejected your cookie.'))
            return

        self.databaseId = result.get('databaseId', 0)
        accountId = result.get('accountId', 0)
        self.adminAccess = result.get('adminAccess', 0)

        self.notify.debug('Account %s has logged in with access level %s' % (str(self.cookie), 
            str(self.adminAccess)))

        # Do they have the minimum access needed to play?
        if self.adminAccess < 100:
            self.csm.air.writeServerEvent('insufficient-access', self.target, self.cookie)
            self.demand('Kill', result.get('reason', 'You have insufficient access to login.'))
            return

        if accountId:
            self.accountId = accountId
            self.demand('RetrieveAccount')
        else:
            self.demand('CreateAccount')

    def enterRetrieveAccount(self):
        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.accountId,
                                             self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields
        self.demand('SetAccount')

    def enterCreateAccount(self):
        self.account = {'ACCOUNT_AV_SET': [0]*6,
                        'ESTATE_ID': 0,
                        'ACCOUNT_AV_SET_DEL': [],
                        'CREATED': time.ctime(),
                        'LAST_LOGIN': time.ctime(),
                        'ACCOUNT_ID': str(self.databaseId),
                        'ADMIN_ACCESS': self.adminAccess}

        self.csm.air.dbInterface.createObject(
            self.csm.air.dbId,
            self.csm.air.dclassesByName['AccountUD'],
            self.account,
            self.__handleCreate)

    def __handleCreate(self, accountId):
        if self.state != 'CreateAccount':
            self.notify.warning('Received create account response outside of CreateAccount state.')
            return

        if not accountId:
            self.notify.warning('Database failed to construct an account object!')
            self.demand('Kill', 'Your account object could not be created in the game database.')
            return

        self.csm.air.writeServerEvent('accountCreated', accountId)

        self.accountId = accountId
        self.demand('StoreAccountID')

    def enterStoreAccountID(self):
        self.csm.accountDB.storeAccountID(self.databaseId, self.accountId, self.__handleStored)

    def __handleStored(self, success=True):
        if not success:
            self.demand('Kill', 'The account server could not save your account DB ID!')
            return

        self.demand('SetAccount')

    def enterSetAccount(self):
        # First, if there's anybody on the account, kill 'em for redundant login:
        dg = PyDatagram()
        dg.addServerHeader(self.csm.GetAccountConnectionChannel(self.accountId),
                           self.csm.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(100)
        dg.addString('This account has been logged in elsewhere.')
        self.csm.air.send(dg)

        # Next, add this connection to the account channel.
        dg = PyDatagram()
        dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
        dg.addChannel(self.csm.GetAccountConnectionChannel(self.accountId))
        self.csm.air.send(dg)

        # Subscribe to any "staff" channels that the account has access to.
        access = self.account.get('ADMIN_ACCESS', 0)
        if access >= 200:
            # Subscribe to the moderator channel.
            dg = PyDatagram()
            dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
            dg.addChannel(OtpDoGlobals.OTP_MOD_CHANNEL)
            self.csm.air.send(dg)
        if access >= 400:
            # Subscribe to the administrator channel.
            dg = PyDatagram()
            dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
            dg.addChannel(OtpDoGlobals.OTP_ADMIN_CHANNEL)
            self.csm.air.send(dg)
        if access >= 500:
            # Subscribe to the system administrator channel.
            dg = PyDatagram()
            dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
            dg.addChannel(OtpDoGlobals.OTP_SYSADMIN_CHANNEL)
            self.csm.air.send(dg)

        # Now set their sender channel to represent their account affiliation:
        dg = PyDatagram()
        dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_SET_CLIENT_ID)
        dg.addChannel(self.accountId << 32) # accountId in high 32 bits, 0 in low (no avatar)
        self.csm.air.send(dg)

        # Un-sandbox them!
        dg = PyDatagram()
        dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_SET_STATE)
        dg.addUint16(2) # ESTABLISHED state. BIG FAT SECURITY RISK!!!
        self.csm.air.send(dg)

        # Update the last login timestamp:
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.accountId,
            self.csm.air.dclassesByName['AccountUD'],
            {'LAST_LOGIN': time.ctime(),
             'ACCOUNT_ID': str(self.databaseId),
             'ADMIN_ACCESS': self.adminAccess})

        # Add a POST_REMOVE to the connection channel to execute the NetMessenger
        # message when the account connection goes RIP on the Client Agent.
        dgcleanup = self.csm.air.netMessenger.prepare('accountDisconnected', [self.accountId])
        dg = PyDatagram()
        dg.addServerHeader(self.target, self.csm.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addString(dgcleanup.getMessage())
        self.csm.air.send(dg)

        # We're done.
        self.csm.air.writeServerEvent('account-login', clientId=self.target, accId=self.accountId, webAccId=self.databaseId, cookie=self.cookie)
        self.csm.sendUpdateToChannel(self.target, 'acceptLogin', [])
        self.demand('Off')

class CreateAvatarFSM(OperationFSM):
    notify = directNotify.newCategory('CreateAvatarFSM')

    def enterStart(self, dna, index, uber):
        # Basic sanity-checking:
        if index >= 6:
            self.demand('Kill', 'Invalid index specified!')
            return

        if not ToonDNA().isValidNetString(dna):
            self.demand('Kill', 'Invalid DNA specified!')
            return

        self.index = index
        self.dna = dna
        self.uber = uber

        # Okay, we're good to go, let's query their account.
        self.demand('RetrieveAccount')

    def enterRetrieveAccount(self):
        # self.target is the accountId, so:
        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.target,
                                             self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields

        self.avList = self.account['ACCOUNT_AV_SET']
        # Sanitize; just in case avList is too long/short:
        self.avList = self.avList[:6]
        self.avList += [0] * (6-len(self.avList))

        # Make sure the index is open:
        if self.avList[self.index]:
            self.demand('Kill', 'This avatar slot is already taken by another avatar!')
            return

        # Okay, there's space, let's create the avatar!
        self.demand('CreateAvatar')

    def enterCreateAvatar(self):
        dna = ToonDNA()
        dna.makeFromNetString(self.dna)
        colorstring = TTLocalizer.NumToColor[dna.headColor]
        animaltype = TTLocalizer.AnimalToSpecies[dna.getAnimal()]
        name = colorstring + ' ' + animaltype

        toonFields = {
            'setName': (name,),
            'WishNameState': WISHNAME_OPEN,
            'WishName': '',
            'setDNAString': (self.dna,),
            'setDISLid': (self.target,),
            'setUber': (self.uber,),
        }

        self.csm.air.dbInterface.createObject(
            self.csm.air.dbId,
            self.csm.air.dclassesByName['DistributedToonUD'],
            toonFields,
            self.__handleCreate)

    def __handleCreate(self, avId):
        if not avId:
            self.demand('Kill', 'Database failed to create the new avatar object!')
            return

        self.avId = avId

        self.demand('StoreAvatar')

    def enterStoreAvatar(self):
        # Associate the avatar with the account...
        self.avList[self.index] = self.avId

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.target, # i.e. the account ID
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': self.avList},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET']},
            self.__handleStoreAvatar)

    def __handleStoreAvatar(self, fields):
        if fields:
            # TODO: delete self.avId
            self.demand('Kill', 'Database failed to associate the new avatar to your account!')
            return

        # Otherwise, we're done!
        self.csm.air.writeServerEvent('avatar-created', avId=self.avId, accId=self.target, dna=self.dna.encode('hex'), slot=self.index)
        self.csm.sendUpdateToAccountId(self.target, 'createAvatarResp', [self.avId])
        self.demand('Off')

class AvatarOperationFSM(OperationFSM):
    # This needs to be overridden.
    POST_ACCOUNT_STATE = 'Off'

    def enterRetrieveAccount(self):
        # Query the account:
        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.target,
                                             self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields
        self.avList = self.account['ACCOUNT_AV_SET']
        # Sanitize; just in case avList is too long/short:
        self.avList = self.avList[:6]
        self.avList += [0] * (6-len(self.avList))

        self.demand(self.POST_ACCOUNT_STATE)

class GetAvatarsFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('GetAvatarsFSM')
    POST_ACCOUNT_STATE = 'QueryAvatars'

    def enterStart(self):
        self.demand('RetrieveAccount')

    def enterQueryAvatars(self):
        self.pendingAvatars = set()
        self.avatarFields = {}
        for avId in self.avList:
            if avId:
                self.pendingAvatars.add(avId)

                def response(dclass, fields, avId=avId):
                    if self.state != 'QueryAvatars': return
                    if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
                        self.demand('Kill', "One of the account's avatars is invalid!")
                        return
                    # Since we weren't previously setting the DISLid of an avatar upon creating
                    # a toon, we will check to see if they already have a DISLid value or not.
                    # If they don't, we will set it here.
                    if not fields.has_key('setDISLid'):
                        self.csm.air.dbInterface.updateObject(
                            self.csm.air.dbId,
                            avId,
                            self.csm.air.dclassesByName['DistributedToonUD'],
                            {'setDISLid' : [self.target]}
                        )
                    self.avatarFields[avId] = fields
                    self.pendingAvatars.remove(avId)
                    if not self.pendingAvatars:
                        self.demand('SendAvatars')

                self.csm.air.dbInterface.queryObject(self.csm.air.dbId, avId,
                                                     response)

        if not self.pendingAvatars:
            self.demand('SendAvatars')

    def enterSendAvatars(self):
        potentialAvs = []

        for avId, fields in self.avatarFields.items():
            index = self.avList.index(avId)
            wns = fields.get('WishNameState', WISHNAME_LOCKED)
            name = fields['setName'][0]
            if wns == WISHNAME_OPEN:
                nameState = 1
            elif wns == WISHNAME_PENDING:
                nameState = 2
            elif wns == WISHNAME_APPROVED:
                nameState = 3
                name = fields['WishName']
            elif wns == WISHNAME_REJECTED:
                nameState = 4
            elif wns == WISHNAME_LOCKED:
                nameState = 0
            else:
                self.csm.notify.warning('Avatar %d is in unknown name state %s.' % (avId, wns))
                nameState = 0

            potentialAvs.append([avId, name, fields['setDNAString'][0],
                                 index, nameState, max(0, fields['setHp'][0]),
                                 fields['setMaxHp'][0], fields['setLastHood'][0]])

        self.csm.sendUpdateToAccountId(self.target, 'setAvatars', [potentialAvs])
        self.demand('Off')

# This inherits from GetAvatarsFSM, because the delete operation ends in a
# setAvatars message being sent to the client.
class DeleteAvatarFSM(GetAvatarsFSM):
    notify = directNotify.newCategory('DeleteAvatarFSM')
    POST_ACCOUNT_STATE = 'ProcessDelete'

    def enterStart(self, avId):
        self.avId = avId
        GetAvatarsFSM.enterStart(self)

    def enterProcessDelete(self):
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to delete an avatar not in the account!')
            return

        index = self.avList.index(self.avId)
        self.avList[index] = 0

        avsDeleted = list(self.account.get('ACCOUNT_AV_SET_DEL', []))
        avsDeleted.append([self.avId, int(time.time())])

        estateId = self.account.get('ESTATE_ID', 0)

        if estateId != 0:
            # This assumes that the house already exists, but it shouldn't
            # be a problem if it doesn't.
            self.csm.air.dbInterface.updateObject(
                self.csm.air.dbId,
                estateId,
                self.csm.air.dclassesByName['DistributedEstateAI'],
                { 'setSlot%dToonId' % index : [0], 'setSlot%dItems' % index : [[]] }
            )

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.target, # i.e. the account ID
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': self.avList,
             'ACCOUNT_AV_SET_DEL': avsDeleted},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET'],
             'ACCOUNT_AV_SET_DEL': self.account['ACCOUNT_AV_SET_DEL']},
            self.__handleDelete)

    def __handleDelete(self, fields):
        if fields:
            self.demand('Kill', 'Database failed to mark the avatar deleted!')
            return
        self.csm.air.friendsManager.clearList(self.avId)
        self.csm.air.writeServerEvent('avatar-deleted', avId=self.avId, accId=self.target)
        self.demand('QueryAvatars')

class SetNameTypedFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('SetNameTypedFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, name):
        self.avId = avId
        self.name = name

        if self.avId:
            self.demand('RetrieveAccount')
            return

        # Hmm, self.avId was 0. Okay, let's just cut to the judging:
        self.demand('JudgeName')

    def enterRetrieveAvatar(self):
        if self.avId and self.avId not in self.avList:
            self.demand('Kill', 'Tried to name an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        if fields['WishNameState'] != WISHNAME_OPEN:
            self.demand('Kill', 'Avatar is not in a namable state!')
            return

        self.demand('JudgeName')

    def enterJudgeName(self):
        status = judgeName(self.name)

        if self.avId and status:
            self.csm.air.dbInterface.updateObject(
                self.csm.air.dbId,
                self.avId,
                self.csm.air.dclassesByName['DistributedToonUD'],
                {'WishNameState': WISHNAME_APPROVED,
                 'WishName': self.name,
                 'WishNameTimestamp': int(time.time())})

        if self.avId:
            self.csm.air.writeServerEvent('avatar-wishname', self.avId, self.name)

        self.csm.sendUpdateToAccountId(self.target, 'setNameTypedResp', [self.avId, status])
        self.demand('Off')

class SetNamePatternFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('SetNamePatternFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, pattern):
        self.avId = avId
        self.pattern = pattern

        self.demand('RetrieveAccount')

    def enterRetrieveAvatar(self):
        if self.avId and self.avId not in self.avList:
            self.demand('Kill', 'Tried to name an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        if fields['WishNameState'] != WISHNAME_OPEN:
            self.demand('Kill', 'Avatar is not in a namable state!')
            return

        self.demand('SetName')

    def enterSetName(self):
        # Render pattern into a string:
        parts = []
        for p,f in self.pattern:
            if p==213: p=212 # Don't allow the name Slappy if they try to add it back in NameMasterEnglish (it will generate a blank name)
            part = self.csm.nameGenerator.nameDictionary.get(p, ('',''))[1]
            if f: part = part[:1].upper() + part[1:]
            else: part = part.lower()
            parts.append(part)

        parts[2] += parts.pop(3) # Merge 2&3 (the last name) as there should be no space.
        while '' in parts: parts.remove('')
        name = ' '.join(parts)

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedToonUD'],
            {'WishNameState': WISHNAME_LOCKED,
             'WishName': '',
             'setName': (name,)})

        self.csm.air.writeServerEvent('avatar-named', avId=self.avId, name=name)
        self.csm.sendUpdateToAccountId(self.target, 'setNamePatternResp', [self.avId, 1])
        self.demand('Off')

class AcknowledgeNameFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('AcknowledgeNameFSM')
    POST_ACCOUNT_STATE = 'GetTargetAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterGetTargetAvatar(self):
        # Make sure the target avatar is part of the account:
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to acknowledge name on an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        # Process the WishNameState change.
        wns = fields['WishNameState']
        wn = fields['WishName']
        name = fields['setName'][0]

        if wns == WISHNAME_APPROVED:
            wns = WISHNAME_LOCKED
            name = wn
            wn = ''
        elif wns == WISHNAME_REJECTED:
            wns = WISHNAME_OPEN
            wn = ''
        else:
            self.demand('Kill', "Tried to acknowledge name on an avatar in %s state!" % wns)
            return

        # Push the change back through:
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedToonUD'],
            {'WishNameState': wns,
             'WishName': wn,
             'setName': (name,)},
            {'WishNameState': fields['WishNameState'],
             'WishName': fields['WishName'],
             'setName': fields['setName']})

        self.csm.sendUpdateToAccountId(self.target, 'acknowledgeAvatarNameResp', [])
        self.demand('Off')

class LoadAvatarFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('LoadAvatarFSM')
    POST_ACCOUNT_STATE = 'GetTargetAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterGetTargetAvatar(self):
        # Make sure the target avatar is part of the account:
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to play an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedToonUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        self.avatar = fields
        self.demand('SetAvatar')

    def enterSetAvatar(self):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # First, give them a POSTREMOVE to unload the avatar, just in case they
        # disconnect while we're working.
        dgcleanup = PyDatagram()
        dgcleanup.addServerHeader(self.avId, channel, STATESERVER_OBJECT_DELETE_RAM)
        dgcleanup.addUint32(self.avId)
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addString(dgcleanup.getMessage())
        self.csm.air.send(dg)

        # Get the avatar's "true" access. (without "server" bit)
        adminAccess = self.account.get('ADMIN_ACCESS', 0)
        adminAccess = adminAccess - adminAccess % 100

        # Activate the avatar on the DBSS:
        self.csm.air.sendActivate(self.avId, 0, 0,
                                  self.csm.air.dclassesByName['DistributedToonUD'],
                                  {'setAdminAccess': [self.account.get('ADMIN_ACCESS', 0)]})

        # Next, add them to the avatar channel:
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_OPEN_CHANNEL)
        dg.addChannel(self.csm.GetPuppetConnectionChannel(self.avId))
        self.csm.air.send(dg)

        # Now set their sender channel to represent their account affiliation:
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_SET_CLIENT_ID)
        dg.addChannel(self.target<<32 | self.avId) # accountId in high 32 bits, avatar in low
        self.csm.air.send(dg)

        # Finally, grant ownership and shut down.
        dg = PyDatagram()
        dg.addServerHeader(self.avId, self.csm.air.ourChannel, STATESERVER_OBJECT_SET_OWNER)
        dg.addChannel(self.csm.GetAccountConnectionChannel(self.target)) # Set ownership channel to the connection's account channel.
        self.csm.air.send(dg)

        # Tell everything that an avatar is coming online!
        fields = self.avatar
        fields.update({'setAdminAccess': [self.account.get('ADMIN_ACCESS', 0)]})
        self.csm.air.friendsManager.toonOnline(self.avId, fields)

        # Tell the GlobalPartyManager as well
        self.csm.air.globalPartyMgr.avatarJoined(self.avId)

        # Post-remove for an avatar that disconnects unexpectedly.
        dgcleanup = self.csm.air.netMessenger.prepare('avatarOffline', [self.avId])
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addString(dgcleanup.getMessage())
        self.csm.air.send(dg)

        self.csm.air.writeServerEvent('avatar-chosen', avId=self.avId, accId=self.target)
        self.demand('Off')

class UnloadAvatarFSM(OperationFSM):
    notify = directNotify.newCategory('UnloadAvatarFSM')

    def enterStart(self, avId):
        self.avId = avId

        # We don't even need to query the account, we know the avatar is being played!
        self.demand('UnloadAvatar')

    def enterUnloadAvatar(self):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # Tell FriendsManager somebody is logging off:
        self.csm.air.friendsManager.toonOffline(self.avId)

        # Get lost, POST_REMOVES!:
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_CLEAR_POST_REMOVES)
        self.csm.air.send(dg)

        # Remove avatar channel:
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_CLOSE_CHANNEL)
        dg.addChannel(self.csm.GetPuppetConnectionChannel(self.avId))
        self.csm.air.send(dg)

        # Reset sender channel:
        dg = PyDatagram()
        dg.addServerHeader(channel, self.csm.air.ourChannel, CLIENTAGENT_SET_CLIENT_ID)
        dg.addChannel(self.target<<32) # accountId in high 32 bits, no avatar in low
        self.csm.air.send(dg)

        # Unload avatar object:
        dg = PyDatagram()
        dg.addServerHeader(self.avId, channel, STATESERVER_OBJECT_DELETE_RAM)
        dg.addUint32(self.avId)
        self.csm.air.send(dg)

        # Done!
        self.csm.air.writeServerEvent('avatar-unload', avId=self.avId)
        self.demand('Off')

# --- ACTUAL CSMUD ---
class ClientServicesManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('ClientServicesManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.queue = LoginQueue(self)

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        # These keep track of the connection/account IDs currently undergoing an
        # operation on the CSM. This is to prevent (hacked) clients from firing up more
        # than one operation at a time, which could potentially lead to exploitation
        # of race conditions.
        self.connection2fsm = {}
        self.account2fsm = {}
        self.sessionKey = '1Cgb/DcqxgqXO5b62nHw+RQFVdOwl+i20AK1z5oTv8Z='

        # start the queue
        self.queue.start()

        # For processing name patterns.
        self.nameGenerator = NameGenerator()
        
        # Setup ban manager
        self.banManager = BanManagerUD(self.air)
        self.banManager.setup()

        # Setup Account Firewall
        self.AccountFirewallUD = AccountFirewallUD(self.air)
        self.AccountFirewallUD.setup()

        # Instantiate our account DB interface using config:
        dbtype = config.GetString('accountdb-type', 'local')
        if dbtype == 'local':
            self.accountDB = LocalAccountDB(self)
        elif dbtype == 'remote':
            self.accountDB = RemoteAccountDB(self)
        else:
            self.notify.error('Invalid account DB type configured: %s' % dbtype)

        # This attribute determines if we want to disable logins.
        self.loginsEnabled = True

    def killConnection(self, connId, reason):
        dg = PyDatagram()
        dg.addServerHeader(connId, self.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(122)
        dg.addString(reason)
        self.air.send(dg)

    def killConnectionFSM(self, connId):
        fsm = self.connection2fsm.get(connId)
        if not fsm:
            self.notify.warning('Tried to kill connection %d for duplicate FSM, but none exists!' % connId)
            return
        
        self.killConnection(connId, 'An operation is already underway: ' + fsm.name)

    def killAccount(self, accountId, reason):
        self.killConnection(self.GetAccountConnectionChannel(accountId), reason)

    def killAccountFSM(self, accountId):
        fsm = self.account2fsm.get(accountId)
        if not fsm:
            self.notify.warning('Tried to kill account %d for duplicate FSM, but none exists!' % accountId)
            return
        
        self.killAccount(accountId, 'An operation is already underway: ' + fsm.name)

    def runAccountFSM(self, fsmtype, *args):
        sender = self.air.getAccountIdFromSender()

        if not sender:
            self.killAccount(sender, 'Client is not logged in.')

        if sender in self.account2fsm:
            # hot fix, remove the sender from the fsm and request the fsm state OFF
            self.account2fsm[sender].demand('Off')

        self.account2fsm[sender] = fsmtype(self, sender)
        self.account2fsm[sender].request('Start', *args)

    def setLoginEnabled(self, enable):
        if not enable:
            self.notify.warning('The CSMUD has been told to reject logins! All future logins will now be rejected.')
        
        self.loginsEnabled = enable

    def login(self, cookie, sessionKey):
        self.queue.queueObject(self.queue.getNewId(), (cookie, sessionKey))

    def performLogin(self, cookie, sessionKey):
        sender = self.air.getMsgSender()

        if not self.AccountFirewallUD.checkPlayerLogin(cookie):
            self.killConnection(sender, 'Your account has been disallowed login to Project Altis. Please try again later.')
            return

        self.notify.debug('Received login cookie %r from %d' % (cookie, self.air.getMsgSender()))      

        if not self.loginsEnabled:
            # Logins are currently disabled... RIP!
            dg = PyDatagram()
            dg.addServerHeader(sender, self.air.ourChannel, CLIENTAGENT_EJECT)
            dg.addUint16(200)
            dg.addString('Logins are currently disabled. Please try again later.')
            self.air.send(dg)

        if sender >> 32:
            # Oops, they have an account ID on their connection already!
            self.killConnection(sender, 'Client is already logged in.')
            return

        if sender in self.connection2fsm:
            # hot fix, remove the sender from the fsm and request the fsm state OFF
            self.connection2fsm[sender].demand('Off')
        
        if sessionKey != self.sessionKey:
            self.killConnection(sender, 'Failed to login, recieved a bad login cookie!')
            
            # notify the admin that someone tried to login with a custom client.
            self.notify.warning('%s: Tried to login with a custom client!' % (sender))
            return
        
        if self.banManager.getToonBanned(cookie):
            self.killConnection(sender, self.banManager.getToonBanReason(cookie))
            return

        self.connection2fsm[sender] = LoginAccountFSM(self, sender)
        self.connection2fsm[sender].request('Start', cookie)

    def requestAvatars(self):
        self.notify.debug('Received avatar list request from %d' % (self.air.getMsgSender()))
        self.runAccountFSM(GetAvatarsFSM)

    def createAvatar(self, dna, index, uber):
        self.runAccountFSM(CreateAvatarFSM, dna, index, uber)

    def deleteAvatar(self, avId):
        self.runAccountFSM(DeleteAvatarFSM, avId)

    def setNameTyped(self, avId, name):
        self.runAccountFSM(SetNameTypedFSM, avId, name)

    def setNamePattern(self, avId, p1, f1, p2, f2, p3, f3, p4, f4):
        self.runAccountFSM(SetNamePatternFSM, avId, [(p1, f1), (p2, f2),
                                                     (p3, f3), (p4, f4)])

    def acknowledgeAvatarName(self, avId):
        self.runAccountFSM(AcknowledgeNameFSM, avId)

    def chooseAvatar(self, avId):
        currentAvId = self.air.getAvatarIdFromSender()
        accountId = self.air.getAccountIdFromSender()
        if currentAvId and avId:
            self.killAccount(accountId, 'A Toon is already chosen!')
            return
        elif not currentAvId and not avId:
            # This isn't really an error, the client is probably just making sure
            # none of its Toons are active.
            return

        if avId:
            self.runAccountFSM(LoadAvatarFSM, avId)
        else:
            self.runAccountFSM(UnloadAvatarFSM, currentAvId)

    def reportPlayer(self, avId, category):
        reporterId = self.air.getAvatarIdFromSender()
        if len(REPORT_REASONS) <= category:
            self.air.writeServerEvent("suspicious", avId=reporterId, issue="Invalid report reason index (%d) sent by avatar." % category)
            return
        
        self.air.writeServerEvent("player-reported", reporterId=reporterId, avId=avId, category=REPORT_REASONS[category])

    def requestBanPlayer(self, avId, reason):
        self.air.dbInterface.queryObject(self.air.dbId, avId, callback=self.__handleLookupPlayer, 
            avId=avId, reason=reason)

    def __handleLookupPlayer(self, dclass, fields, avId, reason):
        accountId = fields.get('setDISLid')

        # lookup account to get login cookie
        self.air.dbInterface.queryObject(self.air.dbId, accountId, callback=self.__handleLookupAccount, 
            accountId=accountId, reason=reason)

    def __handleLookupAccount(self, dclass, fields, accountId, reason):
        cookie = fields.get('ACCOUNT_ID')

        # check if the player is already banned.
        if self.banManager.getToonBanned(cookie):
            return

        self.banManager.banToon(cookie, reason)

        # new, disconnect the toon
        self.killAccount(accountId, reason)