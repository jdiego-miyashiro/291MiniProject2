
"""this functions get's the raw input from the user and splits it into a list that
contains the individual constrains on the output in a proper format 

ie. if the input is body:    stock  confidential  shares  date < 2001/04/12
the function will return [body:stock,confidential,shares,date<2001/04/12] """

from bsddb3 import db

def main():
    #brief by default
    output_mode = "brief"
    while True:
        command = input("press enter to start(q to quit, change output mode here): ")
        comm = command.lower()

        if comm == "output=full":
            output_mode = "full"
            print("outputting in full")
        elif comm == "output=brief":
            output_mode = "brief"
            print("outputting in brief")
        elif comm == "q":
            break
        
        query_input=get_input()
        query_system(query_input,output_mode)
    
    
    return



def get_input():
    
    keywords=[':', '>','<','>=','<=','&']
    query_input=input('Please enter a query using the provided grammar  ')
    query_input = query_input.lower()
    query_input=query_input.split()
    
    for i in range(0,len(query_input)-1):
        for keyword in keywords:
            if query_input[i][-1] not in keywords and query_input[i+1][0] not in keywords:
                query_input[i]=query_input[i] +'&'
                
    query_input=''.join(query_input)
    query_input=query_input.split('&')
    
    
    return query_input
    
    
""" this function makes the actual queries"""    
    
def query_system(query_input,output_mode):
    
    all_query_results = []

    queries_results=[]
    
    for query in query_input:
        query=query.split(':')
        
        if query[0] in ['to','cc','bcc','from','to']:
            query_result=email_adress_queries(query)
            query_result=set(query_result)

            queries_results.append(query_result)
            
        
        # if len == 1, then these are the inputs that arent split
        if len(query) == 1:
            # query for date
            if query[0][:4] == "date":
                # determine the operators, then query with the operators
                if query[0][4:6] in "<=, >=":
                    oper = query[0][4:6]
                    all_query_results.append(query_dates(query[0][6:],oper))
                else:
                    oper = query[0][4:5]
                    all_query_results.append(query_dates(query[0][5:],oper))
            # if query was in form [word]%
            elif len(query[0]) > 1 and query[0][-1] == "%":
                all_query_results.append(wild_card_query(query[0][:-1]))
            # if query was in form [word] %
            elif query_input.index(query[0]) < len(query_input) - 1:
                if query_input[query_input.index(query[0]) + 1] == "%":
                    all_query_results.append(wild_card_query(query[0])) 
            # if query is not these search options, query body and subject
            elif query[0] not in ['to','cc','bcc','from','to','%']:
                all_query_results.append(query_subjects(query[0]))
                all_query_results.append(query_bodies(query[0]))
        elif query[0] == "body":
            all_query_results.append(query_bodies(query[1]))
        elif query[0] == "subj":
            all_query_results.append(query_subjects(query[1]))
        elif query[0] == "date":
            all_query_results.append(query_dates(query[1],"=="))
        

    # add more row ids to all_query_results, ie, ids from the beginning of the function
    # assumes queries_results is a list of list, where each embedded list is the output of a query
    if len(queries_results) > 0:
        for query in queries_results:
            all_query_results.append(query)     

    # if there are no results
    if len(all_query_results) == 0:
        print("(no results)")
        return
    
    results =[]
    # find the intersection of the queries
    results = intersect(all_query_results)

    # get the info to print
    output_info = fetch_output_info(results, output_mode)
    
    # print everything
    print_output_info(output_info, output_mode)

 
    ####
    #   Below this is old code i wont get rid of until we know the new stuff works
    ####


    #rows_id=queries_results[0]
    #for query_result in queries_results:
    #    temp = query_result.intersection(rows_id)
    #    rows_id=temp
        
        
        
    #print result depending on the output mode
    
    
    #rows_id=list(rows_id)
    #rows_id=encode(rows_id)    #econded rows_ids
    
    
    #replace this part with your printing methode
    """if output_mode=='full':
        retrieve_emails(rows_id)
    else:
        print("Emails ids")
        rows_id=list(rows_id)
        rows_id.sort()
        for element in rows_id:
            
            print(element)
        """
    
        
        #if output mode equal brief
            #return set of the intersection
        
        # if output mode equal full
            
      
        #query again for the full record 
        
def encode(rows_id):
    for i in range(0,len(rows_id)):
        rows_id[i]=rows_id[i].encode("utf-8")
    return rows_id

            
        
def email_adress_queries(query):

   
    DB_File = "em.idx"
    database=db.DB()
    database.open(DB_File,None,db.DB_BTREE)
    curs=database.cursor()
    result=[]
    txt='%s-%s' %(query[0], query[1])
   
    
    value=curs.set(txt.encode("utf-8"))
    if value != None:
        result.append(str(value[1]))
        
        dup=curs.next_dup()
        
        while dup!= None:
            result.append(str(dup[1]))
            dup=curs.next_dup()
    else:
        result.append(None)
    curs.close()
    database.close()
    
    return result
    
""" this following function prints the whole text if the ouput mode is full """ 

def retrieve_emails(rows_id):
    
    DB_File ="re.idx"
    database=db.DB()
    database.open(DB_File,None,db.DB_HASH)
    curs=database.cursor()
    emails=[]
    for element in rows_id:
        emails.append(curs.set(element.encode("utf-8")))
   
    
    for email in emails:
        print(email[1])
    curs.close()
    database.close()


def wild_card_query(word):
    # queries for words with the inputted word as the prefix
    
    db_file = "te.idx"
    database = db.DB()
    database.open(db_file, None, db.DB_BTREE, db.DB_CREATE)
    cur = database.cursor()
    result = []
    currLine = cur.first()

    while currLine:
        currWord = currLine[0].decode("utf-8")
        if word in currWord:
            result.append(currLine[1])
        currLine = cur.next()

    cur.close()
    database.close()
    
    return result


def fetch_output_info(rowID_list, output_mode):
    # usage: given a list of row ids, it returns a tuple of lists consisitng of row id, subject, and (if output_mode = full) body
    # ie it returns ([id_1,subject_1,body_1],[id_2,subject_2,body_2],...,[id_n, subject_n,body_n]) for some integer n
    # Given a list of row ids, this function returns the row ids and the subjects' and body's(if mode is full) associated with the row ids.
    #####
    # NOTE : each number in rowID_list must be encoded in utf-8 format
    #####

    # ensures uniqueness (dont need duplicates)
    rowID_list = set(rowID_list)
    rowID_list = list(rowID_list)

    db_file = "re.idx"
    database = db.DB()
    database.open(db_file, None, db.DB_HASH, db.DB_CREATE)
    cur = database.cursor()
    resultArray = []

    currLine = cur.first()

    while currLine:
        # if the current line is relevant
        if currLine[0] in rowID_list:
            # currIndex holds all the desired info from this line
            currIndex = []
            # grab the row number and associated text
            rowNum = currLine[0].decode("utf-8")
            rowText = currLine[1].decode("utf-8")

            # currIndex gets the row num
            currIndex.append(rowNum)

            # splice the subject
            subStart = rowText.find("<subj>") + 6
            subEnd = rowText.find("</subj>")

            if subStart == subEnd:
                subjectText = "(no subject)"
            else:
                subjectText = rowText[subStart:subEnd]

            # currIndex gets the subject
            currIndex.append(subjectText)

            if output_mode == "full":
                # splice the body
                bodyStart = rowText.find("<body>") + 6
                bodyEnd = rowText.find("</body>")
                
                if bodyStart == bodyEnd:
                    bodyText = "(no body)"
                else:
                    bodyText = rowText[bodyStart:bodyEnd]
                # currIndex gets the body
                currIndex.append(bodyText)

            # relevent info from this line is appended to the entire array of results
            resultArray.append(currIndex)

        currLine = cur.next()

    cur.close()
    database.close()

    return tuple(resultArray)

def print_output_info(output_info, output_mode):
    # output_info should be in the form ([rowID,subject, body], [rowID,subject, body], ...) where body is not necessary 
    # prints relevent info based on output mode
    if output_mode == "brief":
        for tup in output_info:
            print("row id: " + tup[0] + "\t" + "subject: " + tup[1])
    elif output_mode == "full":
        for tup in output_info:
            print("row id: " + tup[0] + "\t" + "subject: " + tup[1] + "\n" + "body: " + tup[2] +"\n")
        

def intersect(IDList):
    # convert everything to a set
    for entry in range(len(IDList)):
        IDList[entry] = set(IDList[entry])

    # start off the new set containing all row ids to print
    IDSet = IDList[0]

    # find common row ids
    for entry in IDList:
        IDSet = IDSet.intersection(entry)

    # returned the list of desired row ids
    return list(IDSet)
        

def query_dates(day, oper):
    db_file = "da.idx"
    database = db.DB()
    database.open(db_file, None, db.DB_BTREE, db.DB_CREATE)
    rowID_list = []
    cur = database.cursor()
    day = day.split("/")
    # ensure that every date has no unneeded zeros
    if day[1][0] == "0":
        day[1] = day[1][-1]
    if day[2][0] == "0":
        day[2] = day[2][-1]
        

    currLine = cur.first()

    while currLine:
        lineDate = currLine[0].decode("utf-8")
        lineDate = lineDate.split("/")

        # ensure that every date has no unneeded zeros
        if lineDate[1][0] == "0":
            lineDate[1] = lineDate[1][-1]
        if lineDate[2][0] == "0":
            lineDate[2] = lineDate[2][-1]  

        # compare the dates, append if the date is what we want
        # compare year
        if eval(lineDate[0] + oper + day[0]) and oper != "==":
            rowID_list.append(currLine[1])
        elif lineDate[0] == day[0]:
            # compare month
            if eval(lineDate[1] + oper + day[1]) and oper != "==":
                rowID_list.append(currLine[1])
            elif lineDate[1] == day[1]:
                # compare day
                if eval(lineDate[2] + oper + day[2]):
                    rowID_list.append(currLine[1])

        currLine = cur.next()
    
    cur.close()
    database.close()

    return rowID_list


        




def query_subjects(word):
    db_file = "re.idx"
    database = db.DB()
    database.open(db_file, None, db.DB_HASH, db.DB_CREATE)
    rowID_list = []
    cur = database.cursor()

    currLine = cur.first()

    while currLine:
        rowText = currLine[1].decode("utf-8")
        # find beginning and end of subject
        subStart = rowText.find("<subj>") + 6
        subEnd = rowText.find("</subj>")

        # determine if word is in subject, addi if it is
        if word in rowText[subStart:subEnd]:
            rowNum = currLine[0]
            rowID_list.append(rowNum)
        
        currLine = cur.next()

    cur.close()
    database.close()

    return rowID_list

def query_bodies(word):
    db_file = "re.idx"
    database = db.DB()
    database.open(db_file, None, db.DB_HASH, db.DB_CREATE)
    rowID_list = []
    cur = database.cursor()

    currLine = cur.first()

    while currLine:
        rowText = currLine[1].decode("utf-8")
        # find beginning and end of subject
        bodyStart = rowText.find("<body>") + 6
        bodyEnd = rowText.find("</body>")

        # determine if word is in subject, addi if it is
        if word in rowText[bodyStart:bodyEnd]:
            rowNum = currLine[0]
            rowID_list.append(rowNum)

        currLine = cur.next()

    cur.close()
    database.close()

    return rowID_list




main()    
    