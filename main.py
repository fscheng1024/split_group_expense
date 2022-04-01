import os
import csv
from utils.Bills import Bills
import numpy as np
import cv2


def get_all_bills():
    file_dir = "./data/"
    file_ext = ".csv"
    bills = [_ for _ in os.listdir(file_dir) if _.endswith(file_ext)]
    print(bills)

    return bills


def main():
    print("=== Split bills for shared group expenses. ===")

    option = input("Create new bill? (y|n)")
    if option == 'n':
        bills = get_all_bills()
        title = input("Choose a bill that you what to check: ") 
        if title + '.csv' not in bills:
            print("No {} in list!".format(title))
            keep_going = False
        else:
            my_bill = Bills(title)
            keep_going = True
    else:
        title = input("Set a title for your bill: ")
        my_bill = Bills(title)
        keep_going = True

    while keep_going:
        print("\n==================")
        print("1 - get all bills")
        print("2 - get all items in list")
        print("3 - add item to list")
        print("4 - get each member paid item")
        print("5 - get each member balance")
        print("q/Q - Quit")
        print("==================")

        option = input("Choose an option: ")
        if option == '1':
            bills = get_all_bills()

        elif option == '2':
            my_bill.get_all_items()

        elif option == '3' :
            my_bill.add_item()

        elif option == '4':
            my_bill.get_each_member_paid_item()

        elif option == '5':
            my_bill.get_each_balance()
            
        elif option == 'q' or option == 'Q':
            print("Bye!")
            keep_going = False
        
        else:
            print("INVALID option {}!".format(option))


if __name__ == "__main__":
    main()
