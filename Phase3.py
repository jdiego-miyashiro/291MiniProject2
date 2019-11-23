
"""this functions get's the raw input from the user and splits it into a list that
contains the individual constrains on the output in a proper format 

ie. if the input is body:    stock  confidential  shares  date < 2001/04/12
the function will return [body:stock,confidential,shares,date<2001/04/12] """

from bsddb3 import db

def main():
    query_input=get_input()
    query_system(query_input,'full')
    pass



def get_input():
    
    keywords=[':', '>','<','>=','<=','&']
    query_input=raw_input('Please enter a query using the provided grammar  ')
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
    
    queries_results=[]
    
    for query in query_input:
        query=query.split(':')
        
        if query[0] in ['to','cc','bcc','from','to']:
            query_result=email_adress_queries(query)
            query_result=set(query_result)

            queries_results.append(query_result)
            
           # if type of query == key_word for query type
                #perform the query for the given operator
        
                #query_result.append(list of rows ids output from the query
                # maybe this can be written as a separate function that directly outputs the list of row ids that needs to be appended
                
           
           
           
           # if type of query == key_word for another query type
                #perform the query for the given operator
                
                #same as above
        
        
        
            #and so on with all the types
            
    #take the intersection of all the list inside the query_results and make a set
            
    rows_id=queries_results[0]
    for query_result in queries_results:
        temp = query_result.intersection(rows_id)
        rows_id=temp
        
        
        
    #print result depending on the output mode
    
    rows_id=list(rows_id)
    if output_mode=='full':
        retrieve_emails(rows_id)
    else:
        print("Emails ids")
        rows_id=list(rows_id)
        rows_id.sort()
        for element in rows_id:
            
            print(element)
        
    
        
        #if output mode equal brief
            #return set of the intersection
        
        # if output mode equal full
            
      
        #query again for the full record 
        
        
        
def email_adress_queries(query):

   
    DB_File = "em.idx"
    database=db.DB()
    database.open(DB_File,None,db.DB_BTREE)
    curs=database.cursor()
    result=[]
    txt='%s-%s' %(query[0], query[1])
   
    
    value=curs.set(txt.encode("utf-8"))
    if value != None:
        result.append(str(value[1].decode("utf-8")))
        
        dup=curs.next_dup()
        
        while dup!= None:
            result.append(str(dup[1].decode("utf-8")))
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
        
    
main()    
    