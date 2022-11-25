import random
from tkinter import *

root = Tk()
root.title("Simulasi Penyebaran COVID19 (Proyek Programming 2)")
canvas = Canvas(root, width=1000,height=600, bg='white')

class Main:
    def __init__(self):
        self.window = root
        self.canvas = canvas
        self.canvas.pack()
        self.HumansNumber = 500
        self.human = self.Create__Object_As_Human()
        self.HumanSteps = 0
        self.Dictionary = self.ObjectToObject()
        self.start_the_simulation()

    def Create__Object_As_Human(self):
        list = []
        for i in range(self.HumansNumber):
            n = SpreadingVirus()
            x = random.randint(0, 1000-n.size)
            y = random.randint(0, 600-n.size)
            n.lokasi = [x, y]
            n.velo = [random.randint(-1, 1), random.randint(-1, 1)]
            n.id = self.canvas.create_oval(x, y, x+n.size, y+n.size)
            self.canvas.itemconfigure(n.id, fill=n.color)
            list.append(n)
        list[0].infected= True
        list[0].color = 'red'
        return list

    def start_the_simulation(self):
        ListObject = self.TouchingObjects()
        if ListObject:
            self.Object(ListObject)
        self.Moving()
        self.HumanSteps += 1
        if self.HumanSteps % 200 == 0:
            self.DecreaseTheInfectedPeople()
        self.DoUpdate()
        self.draw()
        self.after_id = self.window.after(10, self.start_the_simulation)

    def draw(self):
        for n in self.human:
            self.canvas.itemconfigure(n.id, fill=n.color)
            y = n.lokasi[1]
            x = n.lokasi[0]
            self.canvas.coords(n.id, x, y, x+n.size, y+n.size)

    def Object(self, Touch):
        for Id1, Id2 in Touch:
            object1 = self.Dictionary[Id1]
            object2 = self.Dictionary[Id2]
            if isinstance(object1, SpreadingVirus):
                if object1.active:
                    if isinstance(object2, SpreadingVirus):
                        object1.interaction(object2)

    def TouchingObjects(self):
        ListTouchingObjects= []
        for n in self.human:
            x1 = n.lokasi[0]
            x2 = x1 + n.size
            y1 = n.lokasi[1]
            y2 = y1 + n.size
            listLocation= self.canvas.find_overlapping(x1, y1, x2, y2)
            if len(listLocation) > 1:
                for i in range(len(listLocation)-1):
                    CO = (listLocation[0], listLocation[i+1])
                    ListTouchingObjects.append(CO)
        return ListTouchingObjects

    def Moving(self):
        for  n in self.human:
            if n.active:
                x = n.lokasi[0] + n.velocity[0]
                y = n.lokasi[1] + n.velocity[1]
                if x <= 0:
                    n.velocity[0] = 1
                if x >= 1000-n.size:
                    n.velocity[0] = -1
                if y <= 0:
                    n.velocity[1] = 1
                if y >= 600-n.size:
                    n.velocity[1] = -1
                n.lokasi[0] = x
                n.lokasi[1] = y

    def DoUpdate(self):
        for n in self.human:
            if n.infected == True:
                n.color = 'red'
            if n.health <= 0:
                n.active = True
                n.infected = False
                n.color = 'black'
            if n.health >= 101:
                n.active = True
                n.color = 'turquoise'
                n.infected = False

    def ObjectToObject(self):
        DictionaryObjek = {}
        for n in self.human:
            DictionaryObjek[n.id] = n
        return DictionaryObjek

    def DecreaseTheInfectedPeople(self):
        for n in self.human:
            if n.active and n.infected:
                n.health -= 20
                if random.randint(0, 1) != 0:
                    n.health += 30


class SpreadingVirus:
    def __init__(self):
        self.size = 10
        self.id = None
        self.infected = False
        self.velocity = [1, 1]
        self.color = 'yellow'
        self.active = True
        self.lokasi = [0, 0]
        self.health = 100

    def always_in_the_environtment(self):
        self.velocity[1] = random.randint(-1, 1)
        self.velocity[0] = random.randint(-1, 1)

    def interaction(self, Otherpeople):
        if self.infected == True and Otherpeople.infected == False:
            Otherpeople.infected = True
            Otherpeople.color = 'red'
        if self.infected == False and Otherpeople.infected== True:
            self.infected = True
            self.color = 'red'
        Otherpeople.always_in_the_environtment()


def RunButton():
    label.pack_forget()
    label1.pack_forget()
    B.pack_forget()
    Main()
label = Label(root, text = "Selamat Datang di Simulasi Sederhana Penyebaran Virus Corona \n\n"
                            "Warna Kuning        = Sehat\n"
                           "Warna Biru Toska    = Sembuh\n"
                           "Warna Merah         = Terinfeksi\n"
                           "Warna Hitam         = Meninggal\n")
label1 = Label(root, text = "Klik RUN Untuk Memulai Simulasi")
label.pack()
label1.pack()
B = Button(root, width=10, height= 5, text = "RUN", command= RunButton)
B.pack()
root.mainloop()