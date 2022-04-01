from itertools import count
import os
import csv
import numpy as np
import cv2

class Bills:
    def __init__(self, title):
        self._keep_adding = True
        self._csv_pth = "./data/" + title + ".csv"
        if not os.path.exists(self._csv_pth):
            with open(self._csv_pth, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Name", "Item", "Cost"])

    def add_item(self):
        name, item, cost = input("Add a item to your bill.[ Name | Item | Cost ]: ").split()
        with open(self._csv_pth, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([name, item, cost])

    def get_all_items(self):
        all_items = []
        with open(self._csv_pth, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            all_items = [row for row in reader]

        print(str(len(all_items)) + " items")
        for item in all_items:
            print(item)
            
    def get_each_member_paid_item(self):
        items_by_name = []
        total = 0
        member_list = self.get_members()
        print(member_list)
        name = input("Check items by name: ")
        with open(self._csv_pth, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                member_name, item, paid = row
                if (member_name == name):
                    items_by_name.append({item : int(paid)})
                    total += int(paid)
        print(" ==> " + str(len(items_by_name)) + " items, total:", total, items_by_name)

    def get_members(self):
        member_list = []
        with open(self._csv_pth, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            for member_name, _, _ in reader:
                if (member_name not in member_list):
                    member_list.append(member_name)

        return member_list

    def get_each_member_total_paid(self):
        member_list = self.get_members()
        result = {}
        for member in member_list:
            result.setdefault(member, 0)

        with open(self._csv_pth, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            for row in reader:
                member_name, _, paid = row
                result[member_name] += int(paid) 
            
        return result

    def get_each_balance(self):
        total = 0.0
        member_list = self.get_each_member_total_paid()
        print("paid list:\n", member_list)
        for name, paid in member_list.items():
            total += int(paid)
        
        avg = total / len(member_list)
        for name, paid in member_list.items():
            member_list[name] = paid - avg

        print("\ntotal: {} \navg: {} \npeople: {}".format(total, avg, len(member_list)))
        print("\neach member should pay: \n", member_list)
        self.save_balance_img(member_list)

    def save_balance_img(self, member_list):
        WHITE = (235, 235, 235)
        GREEN = (113, 179, 60)
        RED = (99, 99, 238)
        GREY = (79, 79, 79)
        WINDOW_W = len(member_list)*60
        WINDOW_H = len(member_list)*60
        FONT_SCALE = 1
        FONT_THICKNESS = 2
        img = np.zeros((WINDOW_W, WINDOW_H, 3), np.uint8)
        img[:] = GREY

        count = 0
        name_x, name_y = 10, 40
        paid_init_x, paid_init_y = 130, 40
        bar_init_y = 10
        item_space = 60
        all_paids = member_list.values()
        max_paid = max(all_paids)
        for name, paid in member_list.items():
            bar_w = int((abs(paid) / max_paid)*200)
            bar_h = 45
            balance = str(paid) 
            if paid > 0:
                cv2.rectangle(img, (paid_init_x, bar_init_y + count*item_space), (paid_init_x + bar_w, bar_init_y + bar_h + count*item_space), GREEN, -1)
                balance = "+" + str(paid) 
            else:
                cv2.rectangle(img, (paid_init_x, bar_init_y + count*item_space), (paid_init_x + bar_w, bar_init_y + bar_h + count*item_space), RED, -1)
            
            cv2.putText(img, name, (name_x, name_y + count*item_space), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, WHITE, FONT_THICKNESS, cv2.LINE_AA)
            cv2.putText(img, balance, (paid_init_x, paid_init_y + count*item_space), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, WHITE, FONT_THICKNESS, cv2.LINE_AA)

            count += 1

        cv2.imwrite('balance.png', img)
        print("Image saved!")
