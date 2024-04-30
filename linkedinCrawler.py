from crawler import LinkedinCrawler

def main():
    FirstName = input('Enter you first name:')
    LastName = input('Enter your last name:')

    # don't share the below details with anyone
    username = 'XXXXXXXXXXX' # your linkedin username
    password = 'XXXXXXXXXXX' # your linkedin password

    output = LinkedinCrawler(FirstName=FirstName, LastName=LastName, username=username, password=password)
    print(output)

if __name__ == '__main__':
    main()