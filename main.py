import requests
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Opens file with Read Write
file = open('cars.csv', 'r+', newline ='', encoding="utf-8")

API_KEY_SENDGRID = 'DONT SHARE THIS'

with file:

    # Request page
    result = requests.get('https://www.mobile.bg/m1olks', headers={'User-Agent': 'Chrome'})

    # If page accessed
    if result.status_code == 200:

        # Process page to HTML
        soup = BeautifulSoup(result.content, "lxml")

        # Finds all car elements
        cars = soup.find_all('table',{'class':'tablereset'}, style=lambda value: value and 'width:660px; margin-bottom:0px; border-top:#008FC6 1px solid;' in value)

        has_new_car = False
        car_listing_html = ''

        for index, car in enumerate(cars):

            # Gets the title HTML element
            name  = car( 'a', {'class':'mmm'} )
            # Price of the car
            price  = car( 'span', {'class':'price'} )
            # Image of car
            image_wrapper = car( 'a', {'class':'photoLink'} )
            image_src = image_wrapper[0]('img')[0]['src']
            image_src = image_src.replace('//', 'https://', 1)

            # Car description
            description = car('td', style=lambda value: value and 'height:50px;padding-left:4px' in value)
            if name[0] :
                link =  name[0]['href']
                title = name[0].text
                # If the first car in list is different from last crawl
                if index == 0 :
                    last_car = file.readline()
                    if last_car != link :
                        has_new_car = True
                        # Save new car's link for next crawl
                        file.write(link)

                car_listing_html += f"""
                    <div style="margin-bottom: 15px; padding-top: 5px; border-top: #008FC6 1px solid;">
                        <img style="width: 100%; height: auto;" src="{image_src}">
                        <div>
                            <a style="font-size: 22px; padding: 10px 0px;" href="{link}">{title}</a>
                            <div>
                                {description}
                            </div>
                            <strong style="font-size: 24px; padding-top: 10px;">
                            {price[0].text}
                            </strong>
                        </div>
                    </div>
                """

        if has_new_car :

            email_html = """
                <html>
                    <body>
                    <div>
                    """ + car_listing_html + """
                    </div>
                    </body>
                </html>
            """


            message = Mail(
                from_email = '###',
                to_emails = '###',
                subject = 'MOBILE.BG | New Honda Civic Found!',
                html_content = email_html)
            try:
                sg = SendGridAPIClient(API_KEY_SENDGRID)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
