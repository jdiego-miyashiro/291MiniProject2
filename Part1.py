import re

def main():
    print("Phase 1")
    file_found = False

    terms_file = open("terms.txt", "w+")
    emails_file = open("emails.txt", "w+")
    dates_file = open("dates.txt", "w+")
    recs_file = open("recs.txt", "w+")

    while not file_found:
        #input_file_name = input("Please enter the name of the input file")
        input_file_name = "smallboi.xml"
        input_file = open(input_file_name, "r")

        if not input_file:
            print("That input file does not exist")
        else:
            file_found = True

    for line in input_file:
        email = parse_tag("mail", line)
        if email:
            row = parse_tag("row", email)
            date = parse_tag("date", email)
            sender = parse_tag("from", email)
            reciever = parse_tag("to", email)
            subject = parse_tag("sibj", email)
            cc = parse_tag("cc", email)
            bcc = parse_tag("bcc", email)
            body = parse_tag("body", email)

            add_terms(terms_file, row, subj, body)
            add_emails(emails_file, row, _from, to, cc, bcc)
            add_dates(dates_file, row, date)
            add_recs(recs_file, row, email)

    terms_file.close()
    emails_file.close()
    dates_file.close()
    recs_file.close()

    

def add_terms(terms_file, row, sibj, body):
    pass

def add_emails(emails_file, row, sender, receiever, cc, bcc):
    pass

def add_dates(dates_file, row, date):
    pass

def add_recs(recs_file, row, email):
    pass

def parse_tag(tag, input_str):
    pass


main()
