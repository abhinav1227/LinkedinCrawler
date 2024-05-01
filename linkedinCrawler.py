from crawler import LinkedinCrawler

def main():
    FirstName = input('Enter you first name:')
    LastName = input('Enter your last name:')

    # don't share the below details with anyone
    username = 'abhiiyadav1227@gmail.com' # your linkedin username
    password = 'Abhin@vy27' # your linkedin password

    crawler = LinkedinCrawler(FirstName=FirstName, LastName=LastName, username=username, password=password)
    output = crawler.crawler()
    
    #saving the dataframe to csv
    output.to_csv('Top10User.csv')
    
    print(output)

if __name__ == '__main__':
    main()
