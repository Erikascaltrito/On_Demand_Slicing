import tkinter as tk
from PIL import ImageTk, Image
import subprocess

class Application:
    def __init__(self, master, images):
        self.master = master
        self.images = images
        self.current_index = 0

        self.image_label = tk.Label(master)
        self.image_label.configure(background='white')
        self.image_label.pack(side = tk.TOP)
        
        self.buttons_frame1 = tk.Frame(master)
        self.buttons_frame1.pack(side=tk.BOTTOM)
        self.buttons_frame1.configure(background='white')
        self.button_states = [True, True, True, True, False, True, False]
        self.buttons = []
        
        self.label_frame = tk.Frame(master)
        self.label_frame.pack(side=tk.BOTTOM)
        self.label_frame.configure(background='white')
        self.labels = []
        
        for i in range(4):
            button = tk.Button(self.buttons_frame1, width=10,height=1, text=f"SLICE {i+1} OFF", command=lambda idx=i: self.toggle_button(idx))
            if i == 0 :
                button.grid(row=1, column=0, padx=10, pady=5)
                label = tk.Label(self.label_frame, width=30,height=1,text="NORTH OFFICES ACTIVE")
                label.grid(row=5, column=0, padx=10, pady=5)
            if i == 1 :
                button.grid(row=1, column=2, padx=10, pady=5)
                label = tk.Label(self.label_frame,width=30,height=1, text="CONFERENCE ROOM ACTIVE")
                label.grid(row=5, column=1, padx=10, pady=5)
            if i == 2 :
                button.grid(row=2, column=0, padx=10, pady=5)
                label = tk.Label(self.label_frame,width=30,height=1, text="EAST OFFICES ACTIVE")
                label.grid(row=5, column=2, padx=10, pady=5)
            if i == 3 :
                button.grid(row=2, column=2, padx=10, pady=5)  
                label = tk.Label(self.label_frame,width=30,height=1, text="WEST OFFICES ACTIVE")
                label.grid(row=5, column=3, padx=10, pady=5)
            self.buttons.append(button)
            self.labels.append(label)
        button = tk.Button(self.buttons_frame1,width=20,height=1, text="HACK MODE ON", command=self.hack)
        button.grid(row=4, column=1, padx=10, pady=5)
        buttonaof = tk.Button(self.buttons_frame1,width=10,height=1, text="ALL ON", command=self.all_on)
        buttonaof.grid(row=3, column=0, padx=10, pady=5)
        buttonaon = tk.Button(self.buttons_frame1,width=10,height=1,text="ALL OFF", command=self.all_off)
        buttonaon.grid(row=3, column=2, padx=10, pady=5)
        self.buttons.append(button)
        self.buttons.append(buttonaof)
        self.buttons.append(buttonaon)
        label = tk.Label(self.label_frame,width=30,height=1, text="IT SERVICES ACTIVE")
        label.grid(row=5, column=4, padx=10, pady=5)
        self.labels.append(label)
        self.show_image()

    def show_image(self):
        img = Image.open(self.images[self.current_index])
        img = img.resize((840, 520), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
    def toggle_button(self, idx):
        if not self.button_states[4]:
            self.button_states[idx] = not self.button_states[idx]
            if self.button_states[idx]:
                self.buttons[idx]["text"] = f"SLICE {idx+1} OFF"
                if idx == 0:
                    self.labels[idx].configure(text="NORTH OFFICES ACTIVE")
                if idx == 1:
                    self.labels[idx].configure(text="CONFERENCE ROOM ACTIVE")
                if idx == 2:
                    self.labels[idx].configure(text="EAST OFFICES ACTIVE")
                if idx == 3:
                    self.labels[idx].configure(text="WEST OFFICES ACTIVE")                
            else:
                self.buttons[idx]["text"] = f"SLICE {idx+1} ON"  
                if idx == 0:
                    self.labels[idx].configure(text="NORTH OFFICES DEACTIVATED")
                if idx == 1:
                    self.labels[idx].configure(text="CONFERENCE ROOM DEACTIVATED")
                if idx == 2:
                    self.labels[idx].configure(text="EAST OFFICES DEACTIVATED")
                if idx == 3:
                    self.labels[idx].configure(text="WEST OFFICES DEACTIVATED")         
            self.update_image()
        else:
            self.current_index = 16 
            self.show_image()
            self.execute(self.current_index)            
   
    def hack(self):
        self.button_states[4] = not self.button_states[4]
        if self.button_states[4]:
            self.buttons[4]["text"] = "HACK MODE OFF"
            self.current_index = 16
            self.labels[4].configure(text = "IT SERVICES DEACTIVATED")
            for idx in range(4):
                self.buttons[idx]["text"] = f"SLICE {idx+1} OFF"
                self.button_states[idx] = True
                if idx == 0:
                    self.labels[idx].configure(text="NORTH OFFICES DEACTIVATED")
                if idx == 1:
                    self.labels[idx].configure(text="CONFERENCE ROOM DEACTIVATED")
                if idx == 2:
                    self.labels[idx].configure(text="EAST OFFICES DEACTIVATED")
                if idx == 3:
                    self.labels[idx].configure(text="WEST OFFICES DEACTIVATED") 
        else:
            self.buttons[4]["text"] = "HACK MODE ON"  
            self.current_index = 15
            self.labels[4].configure(text = "IT SERVICES ACTIVE")
            for idx in range(4):
                self.buttons[idx]["text"] = f"SLICE {idx+1} ON"
                self.button_states[idx] = False
                if idx == 0:
                    self.labels[idx].configure(text="NORTH OFFICES DEACTIVATED")
                if idx == 1:
                    self.labels[idx].configure(text="CONFERENCE ROOM DEACTIVATED")
                if idx == 2:
                    self.labels[idx].configure(text="EAST OFFICES DEACTIVATED")
                if idx == 3:
                    self.labels[idx].configure(text="WEST OFFICES DEACTIVATED") 
        self.show_image()
        self.execute(self.current_index)
    def all_on(self):
        if not self.button_states[4]:
            self.current_index = 0
            for idx in range(4):
                self.buttons[idx]["text"] = f"SLICE {idx+1} OFF"
                self.button_states[idx] = True
                if idx == 0:
                    self.labels[idx].configure(text="NORTH OFFICES ACTIVE")
                if idx == 1:
                    self.labels[idx].configure(text="CONFERENCE ROOM ACTIVE")
                if idx == 2:
                    self.labels[idx].configure(text="EAST OFFICES ACTIVE")
                if idx == 3:
                    self.labels[idx].configure(text="WEST OFFICES ACTIVE") 
        else:
            self.current_index = 16
        self.show_image()
        self.execute(self.current_index)
    def all_off(self):
        if not self.button_states[4]:
            self.current_index = 15
            for idx in range(4):
                self.buttons[idx]["text"] = f"SLICE {idx+1} ON"
                self.button_states[idx] = False
                if idx == 0:
                    self.labels[idx].configure(text="NORTH OFFICES DEACTIVATED")
                if idx == 1:
                    self.labels[idx].configure(text="CONFERENCE ROOM DEACTIVATED")
                if idx == 2:
                    self.labels[idx].configure(text="EAST OFFICES DEACTIVATED")
                if idx == 3:
                    self.labels[idx].configure(text="WEST OFFICES DEACTIVATED") 
        else:
            self.current_index = 16         
        self.show_image()
        self.execute(self.current_index)            
    def update_image(self):
        self.understand()
        self.show_image()
        self.execute(self.current_index)
    def understand(self):
        if not self.button_states[4]:
            if self.button_states[0] and self.button_states[1] and self.button_states[2] and self.button_states[3] :
                self.current_index = 0
            elif not self.button_states[0] and self.button_states[1] and self.button_states[2] and self.button_states[3] :
                self.current_index = 1
            elif self.button_states[0] and not self.button_states[1] and self.button_states[2] and self.button_states[3] :
                self.current_index = 2
            elif self.button_states[0] and self.button_states[1] and not self.button_states[2] and self.button_states[3] :
                self.current_index = 3
            elif self.button_states[0] and self.button_states[1] and self.button_states[2] and not self.button_states[3] :
                self.current_index = 4
            elif not self.button_states[0] and not self.button_states[1] and self.button_states[2] and self.button_states[3] :
                self.current_index = 5
            elif not self.button_states[0] and self.button_states[1] and not self.button_states[2] and self.button_states[3] :
                self.current_index = 6
            elif not self.button_states[0] and self.button_states[1] and self.button_states[2] and not self.button_states[3] :
                self.current_index = 7
            elif self.button_states[0] and not self.button_states[1] and not self.button_states[2] and self.button_states[3] :
                self.current_index = 8
            elif self.button_states[0] and not self.button_states[1] and self.button_states[2] and not self.button_states[3] :
                self.current_index = 9
            elif self.button_states[0] and self.button_states[1] and not self.button_states[2] and not self.button_states[3] :
                self.current_index = 10
            elif not self.button_states[0] and not self.button_states[1] and not self.button_states[2] and self.button_states[3] :
                self.current_index = 11
            elif not self.button_states[0] and not self.button_states[1] and self.button_states[2] and not self.button_states[3] :
                self.current_index = 12
            elif not self.button_states[0] and self.button_states[1] and not self.button_states[2] and not self.button_states[3] :
                self.current_index = 13
            elif self.button_states[0] and not self.button_states[1] and not self.button_states[2] and not self.button_states[3] :
                self.current_index = 14     
            elif not self.button_states[0] and not self.button_states[1] and not self.button_states[2] and not self.button_states[3] :
                self.current_index = 15   
        else:
            self.current_index = 16
    def execute(self, index):
        if index == 0:
            subprocess.call("./Slicing/total_activity.sh")
    
        elif index == 1:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice1.sh")
       
        elif index == 2:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice2.sh")
       
        elif index == 3:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice3.sh")
   
        elif index == 4:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice4.sh")
       
        elif index == 5:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice1.sh")
            subprocess.call("./Slicing/slice2.sh")
   
        elif index == 6:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice1.sh")
            subprocess.call("./Slicing/slice3.sh")
         
        elif index == 7:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice1.sh")
            subprocess.call("./Slicing/slice4.sh")
        
        elif index == 8:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice2.sh")
            subprocess.call("./Slicing/slice3.sh")
       
        elif index == 9:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice2.sh")
            subprocess.call("./Slicing/slice4.sh")
       
        elif index == 10:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice3.sh")
            subprocess.call("./Slicing/slice4.sh")
       
        elif index == 11:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice1.sh")
            subprocess.call("./Slicing/slice2.sh")
            subprocess.call("./Slicing/slice3.sh")
       
        elif index == 12:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice1.sh")
            subprocess.call("./Slicing/slice2.sh")
            subprocess.call("./Slicing/slice4.sh")
          
        elif index == 13:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice1.sh")
            subprocess.call("./Slicing/slice3.sh")
            subprocess.call("./Slicing/slice4.sh")
        
        elif index == 14:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice2.sh")
            subprocess.call("./Slicing/slice3.sh")
            subprocess.call("./Slicing/slice4.sh")

        elif index == 15:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/slice1.sh")
            subprocess.call("./Slicing/slice2.sh")
            subprocess.call("./Slicing/slice3.sh")  
            subprocess.call("./Slicing/slice4.sh")  
            
        elif index == 16:
            subprocess.call("./Slicing/total_activity.sh")
            subprocess.call("./Slicing/hacker_mod.sh")
        
def main():
    root = tk.Tk()
    root.title("On-Demand SDN Slicing")
    root.configure(background='white')
    images = [
              "Slicing_scenarios/All_Active.jpeg", "Slicing_scenarios/Slice1_off.jpeg", "Slicing_scenarios/Slice2_off.jpeg", "Slicing_scenarios/Slice3_off.jpeg", "Slicing_scenarios/Slice4_off.jpeg", 
              "Slicing_scenarios/Slice1_2_off.jpeg", "Slicing_scenarios/Slice1_3_off.jpeg", "Slicing_scenarios/Slice1_4_off.jpeg", "Slicing_scenarios/Slice2_3_off.jpeg",
              "Slicing_scenarios/Slice2_4_off.jpeg", "Slicing_scenarios/Slice3_4_off.jpeg", "Slicing_scenarios/Slice1_2_3_off.jpeg", "Slicing_scenarios/Slice1_2_4_off.jpeg", 
              "Slicing_scenarios/Slice1_3_4_off.jpeg", "Slicing_scenarios/Slice2_3_4_off.jpeg", "Slicing_scenarios/Slice1_2_3_4_off.jpeg", "Slicing_scenarios/Hack_mod.jpeg"
              ]

    app = Application(root, images)

    root.mainloop()

if __name__ == "__main__":
    main()