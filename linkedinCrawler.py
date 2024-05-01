from crawler import LinkedinCrawler

def main():
    FirstName = input('Enter you first name:')
    LastName = input('Enter your last name:')

    # don't share the below details with anyone
    username = 'XXXXXXXXXXXXXX' # your linkedin username
    password = 'XXXXXXXXXXXXXX' # your linkedin password

    crawler = LinkedinCrawler(FirstName=FirstName, LastName=LastName, username=username, password=password)
    output = crawler.crawler()
    
    #saving the dataframe to csv
    output.to_csv('Top10User.csv')
    
    print(output)

if __name__ == '__main__':
    main()
