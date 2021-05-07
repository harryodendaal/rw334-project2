import pandas as pd
import numpy as np
import re


#import emails
filename = 'emails.csv'
df = pd.DataFrame()
def auto_truncate(val):
    return val[:]
   


for tp in pd.read_csv(filename, chunksize = 25000, converters={'message': auto_truncate}):
    tp = tp.loc[~tp['file'].str.contains("sent_mail|all_documents/|discussion_threads/")].dropna()
    df = df.append(tp)
df = df.reset_index(drop=True)


#get fields
data = []
keys = ['Date', 'X-From', 'X-To', 'Subject', 'X-cc', 'X-bcc', 'Message-ID','dupmessage']
row = dict.fromkeys(keys)
for x in range(len(df)):
    message = df['message'].iloc[x]
    result = re.sub(', \n', ', ', message)
    result = re.sub('\n ', ' ', result)
    i = result.find('X-FileName')
    k = result.find('\n',i)
    body = result[k+2:]
    result = result[:i-1]
    result = re.split('\n', result)
    value = [s[s.find(': ')+2:] for s in result]
    key = [s[:s.find(': ')] for s in result]
    temp = dict(zip(key, value))
    row.update(temp)
    dup = row['X-From']
    if row['X-To']: dup = dup + row['X-To']
    elif row['Subject']: dup = dup + row['Subject']
    dup = dup+body
    row['dupmessage'] = dup
    row['Message-ID'] = row['Message-ID'][1:-1]
    values = list(row.values())[:8]
    values.insert(0, body)
    data.append(values)
df = df.drop('message',1)
df = pd.concat([df, pd.DataFrame.from_records(data)], axis=1)

df.columns = ['file','body','Date', 'X-From', 'X-To', 'Subject', 'X-cc', 'X-bcc', 'Message-ID', 'dupmessage']
df = df.drop_duplicates(subset='dupmessage', keep="last") #delete duplicate emails (Same from, to, subject, body)
df = df.drop('dupmessage', 1)

def file_to_email():
    valid = set()
    valid.add('no.address@enron.com')
    for file in df['file']:
        i = file.find('/')
        #if statements are for spelling inconsistentcies in the csv
        if file[:i] == 'crandell-s':
            valid.add('crandall-s@enron.com')
        elif file[:i] == 'merriss-s':
            valid.add('merris-s@enron.com')
        elif file[:i] == 'phanis-s':
            valid.add('panus-s@enron.com')
        elif file[:i] == 'rodrique-r':
            valid.add('rodrigue-r@enron.com')
        else:
            valid.add(file[:i]+'@enron.com')
    return list(valid)

# Surname, Name
def lastcommafirst(name):
    i = name.find(',')
    j = name.find(' ', i+2)
    if j == -1: j = len(name)
    sname = name[:i].capitalize()
    l = sname.find(' ')
    if l >= 0: sname=sname[:l]
    fname = name[i+2:j].capitalize()
    sname = re.sub('[\W_]', '', sname)
    if len(fname) > 0 and len(sname) > 0:
        return [fname, sname]
    else:
        return []

# Name (middle )Surname
def firstmidlast(name):
    i = name.find(' ')
    j = name.rfind(' ')
    fname = name[:i].capitalize()
    sname = name[j+1:].capitalize()
    sname = re.sub('[\W_]', '', sname)
    if len(fname) > 0 and len(sname) > 0:
        return [fname, sname]
    else:
        return []


def string_to_name(name):
    k = name.find('<')
    if name == 'Patrice L Mims':
        return ['Patrice', 'Mims-Thurston']
    # Has <>
    if k >= 0:
        name = name[:k-1]
        #"Name Surname"
        if name[0] == '\"':
            i = name.find('\"',1)
            name = name[1:i]
            # No space (invalid)
            if name.find(' ') == -1:
                return []
            # Has space
            else:
                return firstmidlast(name)                

        #No quotation marks
        else:
            # string-with-no-space (is never valid)
            if name.find(' ') == -1:
                return []
            # Surname, Name
            else:
                if name[:18] == 'Williams III, Bill':
                    return ['Bill', 'Williams', 'williams-w3@enron.com']
                return lastcommafirst(name)
            
    # No <>            
    else:
       #Surname, Name
        if ',' in name:
            return lastcommafirst(name)
        #Name Surname@
        elif '@' in name:
            i = name.find('@')
            name = name[:i]
            return firstmidlast(name)
        #Name( middle) Surname
        else:
            if name == 'Carol St Clair':
                return ['Carol', 'StClair']
            if name == 'Liz M Taylor':
                return ['Liz', 'Taylor', 'whalley-l@enron.com']
            return firstmidlast(name)

def sep_name(all_name):
    listofnames = set()
    undis = 'undisclosed-recepients@enron.com'
    name_reg = r"^((?:([\da-z]+)@enron.com)|(?:[\']?\"[a-z]+ [a-z]+\" <(.*?)>[\']?)|(?:[\']?([a-z]+)@enron.com[\']?)|(?:([a-z]+[,]? [a-z. ]+) <.*?>)|([a-z]+ [a-z ]+)|\(undisclosed-recipients\))*(.*?)[,\n]??$"
    while True:
        names = re.search(name_reg, all_name, re.IGNORECASE)
        if names.group(7) == all_name:
            i = all_name.find(',')
            if i == -1:
                listofnames.add('undisclosed-recepients@enron.com')
                break
            all_name = all_name[i+1].strip()
            
        append = undis
        if names.group(3) is not None:
            curr_name = names.group(3)
            i = curr_name.find('@')
            email = (curr_name[1:i]+'-'+curr_name[0]+'@enron.com').lower()
            if email in valid_email:
                append = email
        elif names.group(2) is not None:
            curr_name = names.group(2).lower()
            email = (curr_name[1:]+'-'+curr_name[0]+'@enron.com').lower()
            if email in valid_email:
                append = email
        elif names.group(4) is not None:
            curr_name = names.group(4).lower()
            email = (curr_name[1:]+'-'+curr_name[0]+'@enron.com').lower()
            if email in valid_email:
                append = email
        elif names.group(5) is not None:
            curr_name = names.group(5).lower()
            #print(curr_name)
            i = curr_name.find(',')
            if i == -1:
                i = curr_name.find(' ')
                j = curr_name.rfind(' ')
                email = (curr_name[j+1:]+'-'+curr_name[0]+'@enron.com').lower()
            else:
                j = curr_name.find(' ', i+2)
                if j == -1: j = len(curr_name)
                email = (curr_name[:i]+'-'+curr_name[i+2]+'@enron.com').lower()
            if email in valid_email:
                append = email
        elif names.group(6) is not None:
            curr_name = names.group(6)
            i = curr_name.rfind(' ')
            email = (curr_name[i+1:]+'-'+curr_name[0]+'@enron.com').lower()
            if email in valid_email:
                append = email
        listofnames.add(append)
        if names.group(7) == '' or names.group(7) is None:
            break
        else:
            all_name = all_name[all_name.find(names.group(7))+1:].strip()
    #print(listofnames)
    return list(listofnames)

email_reg = r"^[a-z]+\-[\da-z-]+@enron.com$"
valid_email = file_to_email()
employ = []
mess = []
rec =[]
undisclosed = 'undisclosed-recepients@enron.com'
no_ad = [None, None, 'no.address@enron.com']
employ.append(no_ad)

for x in range(len(df)):
    row = df.iloc[x].tolist()
    from_name = string_to_name(row[3])
    if len(from_name) >= 2:
        from_mail = (from_name[1]+'-'+from_name[0][0]+'@enron.com').lower()
        if len(from_name) == 3:
            from_mail = from_name[2]
        if re.match(email_reg, from_mail) and from_mail in valid_email:
            from_name.append(from_mail)
            employ.append(from_name[:3])
        else:
            from_mail = 'no.address@enron.com'
    else:
        from_mail = 'no.address@enron.com'
    row[3] = from_mail
    
    xto = str(row[4])
    if xto == '':
        row[4] = [undisclosed]
        to_names = [undisclosed]
    else:
        xto = xto.replace('\n', '')
        to_names  = sep_name(xto)
    row[4] = to_names
    
    xcc = str(row[6])
    if xcc == '':
        row[6] = None
        cc_names = None
    else:
        xcc = xcc.replace('\n', '')
        cc_names  = sep_name(xcc)
    row[6] = cc_names
    
    xbcc = str(row[7])
    if xbcc == '':
        row[7] = None
        bcc_names = None
    else:
        xbcc = xbcc.replace('\n', '')
        bcc_names  = sep_name(xbcc)
    row[7] = bcc_names
    to_check = len(row[4]) == 1 and row[4][0] == undisclosed
    cc_check = row[6] is None
    if not cc_check: cc_check = len(row[6]) == 1 and row[6][0] == undisclosed
    bcc_check = row[7] is None
    if not bcc_check: bcc_check = len(row[7]) == 1 and row[7][0] == undisclosed
    file = row[0]
    i = file.find('/')
    file = file[:i]+'@enron.com'
    if from_mail != file and to_check and cc_check and bcc_check:
        row[4] = [file]
    # message table info
    messagetab = [row[3], row[2], row[8], row[5], row[1], row[0]]
    for emailname in row[4]:
        recipient = [x, 'TO', emailname]
        rec.append(recipient)
    if row[6] is not None:
        for emailname in row[6]:
            recipient = [x, 'CC', emailname]
            rec.append(recipient)
    if row[7] is not None:
        for emailname in row[7]:
            recipient = [x, 'BCC', emailname]
            rec.append(recipient)
    
    mess.append(messagetab)
    df.iloc[x] = np.array(row, dtype=object)

#EmployeeList
employdf = pd.DataFrame(employ)
employdf = employdf.drop_duplicates(2, keep = 'first') #removes dup emails
employdf = employdf.sort_values(2)
employdf = employdf.reset_index(drop=True)
employdf.to_csv('EmployeeList.csv')

#Message
msgdf = pd.DataFrame(mess)
msgdf = msgdf.reset_index(drop=True)
msgdf.to_csv('Message.csv')

#RecipientInfo
recdf = pd.DataFrame(rec)
recdf = recdf.reset_index(drop=True)
recdf.to_csv('RecipientInfo.csv', index=False)

#CSV with all from, to, cc and bcc
emails = df.copy()
email = df.drop(['file','body','Date','Subject','Message-ID'], axis =1)
email.to_csv('FromToCcBcc.csv', index=False)