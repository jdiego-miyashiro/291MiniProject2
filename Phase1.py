import re

def main():
    print("Phase 1")
    file_found = False

    terms_file = open("terms.txt", "w+")
    emails_file = open("emails.txt", "w+")
    dates_file = open("dates.txt", "w+")
    recs_file = open("recs.txt", "w+")

    while not file_found:
        input_file_name = input("Please enter the name of the input file")
        input_file = open(input_file_name, "r")

        if not input_file:
            print("That input file does not exist")
        else:
            file_found = True

    for line in input_file:
        email = parse_tag("mail", line)
        if email:
            email = replace_symbols(email)
            row = parse_tag("row", email)
            date = parse_tag("date", email)
            sender = parse_tag("from", email)
            reciever = parse_tag("to", email)
            subj = parse_tag("subj", email)
            cc = parse_tag("cc", email)
            bcc = parse_tag("bcc", email)
            body = parse_tag("body", email)

            add_terms(terms_file, row, subj, body)
            add_emails(emails_file, row, sender, reciever, cc, bcc)
            add_dates(dates_file, row, date)
            add_recs(recs_file, row, email)

    terms_file.close()
    emails_file.close()
    dates_file.close()
    recs_file.close()

    print("Phase 1 Finished")

    return

    

def add_terms(terms_file, row, subj, body):
    for term in re.findall("[0-9a-zA-Z_-]{3,}", subj):
        terms_file.write("s-{}:{}\n".format(term, row))

    for term in re.findall("[0-9a-zA-Z_-]{3,}", body):
        terms_file.write("b-{}:{}\n".format(term, row))

    return


def add_emails(emails_file, row, sender, receiever, cc, bcc):

    if sender:
        emails_file.write("from-{}:{}\n".format(sender.lower(), row))

    if receiever:
        for email in receiever.split(","):
            emails_file.write("to-{}:{}\n".format(email.lower(), row))

    if cc:
        for email in cc.split(","):
            emails_file.write("cc-{}:{}\n".format(email.lower(), row))

    if bcc:
        for email in bcc.split(","):
            emails_file.write("bcc-{}:{}\n".format(email.lower(), row))
    
    return

def add_dates(dates_file, row, date):
    dates_file.write("{}:{}\n".format(date,row))
    return

def add_recs(recs_file, row, email):
    recs_file.write("{}:<mail>{}</mail>\n".format(row, email))
    return

def parse_tag(tag, line):
    checkmatch = re.search("(<{}>)(.*)(</{}>)".format(tag, tag), line)
    if checkmatch:
        inner_string = checkmatch.group(2).lower()
        return inner_string
    else:
        return

def replace_symbols(line):
    line = re.sub("&lt;", "<", line)
    line = re.sub("&gt;", ">", line)
    line = re.sub("&amp;", "&", line)
    line = re.sub("&apos;", "'", line)
    line = re.sub("&quot;", '"', line)
    line = re.sub("&#[0-9];", "", line)
    return line

main()