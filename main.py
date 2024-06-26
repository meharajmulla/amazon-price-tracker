import csv
import time
import multiprocessing

from matplotlib import style

from data import ItemData
from track_price import Tracker
from mail import Communication
from settings import CSV_ITEM_FILE, ITEM_NUM_FILE
import settings

def listItems():
    items = dict()

    with open(CSV_ITEM_FILE, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            items.update({line[1][:20]: line[0]})
        
    return items

def trackerInstance(url):
    item = Tracker(url)
    data = ItemData(url)

    style.use("fivethirtyeight")
    item.graph()
    print(item.price())

    if item.compare_prices() == 'below':
        print(f'{item.price()} < Rs{item.target_price}\n')
        comms = Communication(item.title().strip(), url, item.price(), 'Rs.' + item.target_price)
        
        comms.sendEmail()
    
        data.delFile()

    elif item.compare_prices() == 'above':
        print(f'{item.price()} > Rs{item.target_price}\n')

    elif item.compare_prices() == 'out-of-stock':
        print(f'{item.price()} > Rs{item.target_price} - Item is out of stock\n')

def trackerLoop():
    while True:

        p = multiprocessing.Pool()
        urls = []

        try:
            with open(CSV_ITEM_FILE, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                for line in csv_reader:
                    
                    url = line[0]

                    urls.append(url)
                    
            p.map(trackerInstance, urls)
            p.close()

            time.sleep(settings.check_interval)
        except Exception as e:
            print(e, '\nError! Trying again in 30 seconds..')
            time.sleep(30)
            continue

def addItem():
    url = input('Item URL: ')
    item = Tracker(url)

    if ItemData(url).save() == 'already_exists':
        print('Item is already being tracked!')

    else:
        print(f'\n{item.title().strip()} has been added to the tracking list!')

def delItem():
    url = input('Item URL: ')
    YoN = input('Are you sure you want to stop tracking this item? (Y/N): ').lower()

    if YoN == 'y':
        deleted = ItemData(url).delFile()
        
        if deleted:
            print('Your item was removed from the tracking list.')
        else:
            print('Invalid URL!')
    else:
        print('Item was not deleted.')

def mainLoop():
    while True:
        print("Select an option:")
        print("1. Track item")
        print("2. Add item")
        print("3. Delete item")
        print("4. List items")
        print("5. Exit")
        option = input("Enter your choice: ")

        if option == '1':
            trackerLoop()

        elif option == '2':
            addItem()

        elif option == '3':
            delItem()

        elif option == '4':
            print()
            for item, link in listItems().items():
                print(f'{item}: {link}')

        elif option == '5':
            exit()

        else:
            print('\nThis is not an option!')

if __name__ == "__main__":
    mainLoop()
