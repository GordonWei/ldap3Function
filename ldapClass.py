from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_DELETE

#Author : GordonWei
#Date : 04/22/20
#Blog : https://www.kmp.tw/
#Comment : Python3 Control Ldap 

class ldapFunc():

	def __init__(self, ip, loginUser, loginPass):
		self.ip = ip
		self.loginUser = loginUser
		self.loginPass = loginPass
		self.host = Server(self.ip, get_info=ALL)
		self.conn = Connection(self.host, self.loginUser, self.loginPass, check_names=True, lazy=False, raise_exceptions=True)
		self.conn.open()
		self.conn.bind()

    @property
    def conn(self):
        if not self.conn:
            print('connect init')
            self.conn = Connection(self.host, self.loginUser, self.loginPass, check_names=True, lazy=False, raise_exceptions=True)
        return self.conn

    def listUser(self, groupName):
        self.conn.search('cn='+groupName+',ou=OU,dc=Domain,dc=com,dc=tw', '(objectClass=group)', 'SUBTREE', attributes = ['member'])
        result = self.conn.entries
        print('The ' + groupName + ' Member Lists:')
        for en in result:
            for member in en.member.values:
                member = member.split(',')
                print(member[0].replace('CN=',''))
        self.conn.unbind()

    def addUserToGroup(self, userName, groupName):
        response = ''
        self.conn.search(search_base = 'ou=OU,dc=Domain,dc=com,dc=tw', search_filter = '(&(objectclass=person)(cn=' + userName + '*))', search_scope='SUBTREE', attributes = ['*'])
        result = self.conn.entries
        getDn = result[0].distinguishedName
        getDn = str(getDn)
        group = 'cn='+ groupName +',ou=OU,dc=Domain,dc=com,dc=tw'
        self.conn.modify(dn=group, changes={'member': [(MODIFY_ADD, [getDn])]})
        addResult = self.conn.entries
        if addResult == [ ]:
        	print('Already Add ' + userName + ' To ' + groupName)
            response = ('Already Add ' + userName + ' To ' + groupName)
        else:
            print('SomeThing Error')
            response = 'Erro Please Check It!'

        return response
        self.conn.unbind()

    def delUserFromGroup(self, userName, groupName):
    	response = ''
        self.conn.search(search_base = 'ou=OU,dc=Domain,dc=com,dc=tw', search_filter = '(&(objectclass=person)(cn=' + userName + '*))', search_scope='SUBTREE', attributes = ['*'])
        result = self.conn.entries
        getDn = result[0].distinguishedName
        getDn = str(getDn)
        group = 'cn='+ groupName +',ou=OU,dc=Domain,dc=com,dc=tw'
        self.conn.modify(dn=group, changes={'member': [(MODIFY_DELETE, [getDn])]})
        delResult = self.conn.entries
        if delResult == [ ]:
            print('Already Del ' + userName + ' From ' + groupName + ' !')
            response = ('Already Del ' + userName + ' From ' + groupName + ' !')
        else:
            print('Got Error')
            response = 'Del Error'

        return response
        self.conn.unbind()    
