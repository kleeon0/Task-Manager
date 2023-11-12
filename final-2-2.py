import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
from datetime import datetime,date, timedelta
import time
import json

###instance vars
i=0 #task counter
filename = "users.json" #file datebase
taskarray=[]            # to store an array of tasks
index = 0               # to store the index of the target task
current_date = date.today() # todays date
print (current_date)    # test




class task_score:
    def __init__(self,duration, priority) -> None:
        self.score = 0
        self.duration = duration
        self. priority = priority
        if duration == "90+":
            if priority == "Urgent":
                self.score = 90*3
            elif priority == "Important":
                self.score = 90*2
            else:
                self.score = 90
            
        else:
            if priority == "Urgent":
                self.score = int(duration)*3
            elif priority == "Important":
                self.score = int(duration)*2
            else:
                self.score = int(duration)

#function to create task score
def t_score(duration, priority):
    score = 0
    if duration == "90+":
        if priority == "Urgent":
            score = 90*3
        elif priority == "Important":
            score = 90*2
        else:
            score = 90
        
    else:
        if priority == "Urgent":
            score = int(duration)*3
        elif priority == "Important":
            score = int(duration)*2
        else:
            score = int(duration)
    return score


        
##### class borrowed from  https://stackoverflow.com/questions/67233714/tkinter-calendar-doesnt-grid-at-the-right-place 
## class to make date entry
class MyDateEntry(DateEntry):
    def __init__(self, root ,**kw):
        DateEntry.__init__(self,root, **kw)
        # add black border around drop-down calendar
        self._top_cal.configure(bg='blue', bd=1)
        # add label displaying today's date below
        tk.Label(self._top_cal, bg='grey', anchor='w',
                 text='Today: %s' % date.today().strftime('%x')).pack(fill='x')

#home screen
def main_screen():
    #page setup
    root = Tk()
    root.geometry("935x500")
    root.title("Home")
    root.configure(bg="white")
    root.resizable(False,False)
    frame=Frame(root,width=500,height=500,bg="white")
    frame.place(x=300,y=70)

    #header title
    heading=Label(frame,text="Task Manager", fg="#57a1f8",bg="white",font=("Calibri",23,"bold"))
    heading.place(x=80,y=5)

    #complete daily task page
    daily_task_b = Button(frame,pady=6, text="Daily task", bg="#57a1f8",fg="white", border=0,cursor="hand2"
                        ,font=("Calibri",20,"bold"), command= daily_task)
    daily_task_b.place(x=0,y=140)

    # add/ task task page
    task_b = Button(frame,pady=6, padx=10, text="Tasks", bg="#57a1f8",fg="white", border=0,cursor="hand2"
                    ,font=("Calibri",20,"bold"), command=task_screen)
    task_b.place(x=250,y=140)

    ## close screen
    close_b=Button(frame,padx=10,text="Exit", bg="#57a1f8",fg="white", border=0,font=("Calibri",20,"bold")
                   ,command=lambda:root.destroy())
    close_b.place(x=130,y=370)


    root.mainloop()


############# printing database values when logging clicking into addtask page or complete task page #######
def printTable(taskarray , table):
    #loop for task array and assign a variable each task parameter
    for i in taskarray:
        id = i[0]
        name = i[1]
        score = i[2]
        duration = i[3]
        due = i[4]
        priority = i[5]
        repeat= i[6]

        # insert variable into tkinter table
        table.insert("",'end',iid=i,
            values=(id,name,score,duration,due, priority, repeat))

###### print table for tasks due on todays date
def printDailytask(taskarray, table, date):
    #loop for task array and assign a variable each task parameter
    for i in taskarray:
        id = i[0]
        name = i[1]
        score = i[2]
        duration = i[3]
        due = i[4]
        priority = i[5]
        repeat= i[6]
        #print ("due",due, "type", type(due))
       # print ("switched" ,datetime.strptime(due,'%Y-%m-%d'))
       # print("date",date, "type" ,type(date))
        # insert variable into tkinter table
        if due == str(date):
            table.insert("",'end',iid=i,
                values=(id,name,score,duration,due, priority, repeat))


### quicksort algorithm ####
# partitioning the sort algorithm
def partition(array, low, high, index):
 
    # choose the rightmost element as pivot
    pivot = array[high][index]
    # pointer for greater element
    i = low - 1
    # compare each element with pivot
    for j in range(low, high):
        if array[j][index] <= pivot:
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
            # Swapping elements
            (array[i], array[j]) = (array[j], array[i])
    # Swapping the pivot element
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    # Return the position from where partition is done
    return i + 1
 
# function to perform quicksort
def quickSort(array, low, high, index):
    if low < high:
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pivot = partition(array, low, high, index)
 
        # Recursive sort on the left of pivot
        quickSort(array, low, pivot - 1, index)
 
        # Recursive sort on the right of pivot
        quickSort(array, pivot + 1, high, index)



####### function to sort the display of task terms of task score
def sort_score(taskarray , table):
    #copy the array of tasks into a another array
    sorttable=taskarray
    size = len(sorttable)
    # sorting the array through quicksort method
    quickSort (sorttable, 0, size-1, 2)

    #removes all current values
    for record in table.get_children():
        table.delete(record)

    #inputs the sortted values back through printTable function
    printTable(sorttable, table)
 

### function to sort date in terms of closest date
def sort_date(taskarray , table):
    sorttable=taskarray
    size = len(sorttable)
    quickSort (sorttable, 0, size-1, 4)



    #removes all current values
    for record in table.get_children():
        table.delete(record)
    #inputs the sortted values back through printTable function
    printTable(sorttable, table)
 


## binary search search function
def binary_search(array, target, index):
    start = 0
    end = len(array) - 1
    while(start <= end):
        mid = (start + end) // 2
        if(int(array[mid][index]) > target):
            end = mid - 1
        elif(int(array[mid][index]) < target):
            start = mid + 1
        else:
            return mid
    return None


##### add task screen page ##########################

def task_screen():
    #page setup
    root = tk.Tk()
    root.title("Tasks")
    root.geometry("1050x500")
    root.resizable(False,False)
    root.configure(bg="white")

    #calling in global variables
    global i, taskarray

    #opening and reading json database file
    with open(filename,"r") as users:
        data = json.load(users)
        taskarray = data['user'][index]['tasks']

    ### table setup #########
    table=ttk.Treeview(root,selectmode='browse',height=16)
    table.grid(row=1,column=1,columnspan=4,padx=20,pady=20)
    table["columns"]=("1","2","3","4","5","6","7")
    table['show']='headings'
    table.column("1",width=50,anchor='c')
    table.column("2",width=200,anchor='c')
    table.column("3",width=80,anchor='c')
    table.column("4",width=70,anchor='c')
    table.column("5",width=80,anchor='c')
    table.column("6",width=100,anchor='c')
    table.column("7",width=100,anchor='c')
    table.heading("1",text="Task ID")
    table.heading("2",text="Name")
    table.heading("3",text="Score", command= lambda: sort_score(taskarray, table))
    table.heading("4",text="Duration")
    table.heading("5",text="Due", command= lambda: sort_date(taskarray, table))
    table.heading("6",text= "Priority")
    table.heading("7",text="Repeat")

    #calling function to print tasks into table
    printTable(taskarray, table)


    # function for convertion of date format
    def convert(date_time):
        format = '%Y-%m-%d'  # The format
        datetime_str = datetime.strptime(date_time, format)
    
        return datetime_str


    #edit task
    def editTask(e):
        
        #emptying entry boxes
        name_text.delete('1.0',END)
        duration_option.set("")
        de.set_date("9/6/16")
        priority_option.set("")
        repeat_option.set("")

        selected= table.focus()
        values= table.item(selected,'values')

        #putting existing task varibles into it
        name_text.insert('1.0',values[1])
        duration_option.set(values[3])

        date_time = values[4]
        de.set_date(convert(date_time))

        priority_option.set(values[5])
        repeat_option.set(values[6])
    
    # remove a task #
    def remove_task(table):
        task = table.selection()[0]  # gete row task that is clicked on
      #  print ("id num",task)
        select = table.focus() 
        values= table.item(select,'values')
        selected_id = int(values[0])
    #    print("id num", selected_id, "type",type(selected_id))
        ## read through file and find task
        with open(filename,"r") as users:
            data = json.load(users)
            taskarray = data['user'][index]['tasks']
         #   print ("id num ta", taskarray[0][0], "type",type(taskarray[0][0]))
            search_id = binary_search(taskarray,selected_id,0)
         #   print ("serach index", search_id)
            # remove task when found
            if (search_id>=0):
                target_task  = taskarray[search_id]
                taskarray.remove(target_task)
                table.delete(task)
            #    print ("successful delete")
            # write the changes in database
            with open(filename, "w") as file:
                json.dump(data, file, indent=4, default=str)

    #change an existing task#
    def update_task():
        # update the table
        name=name_text.get("1.0",END).rstrip()         # read name
        duration=duration_option.get()                 # read duration
        due = de.get_date()                            #read date
        priority=priority_option.get()                 # read imporant/ urgent
        repeat = repeat_option.get()                   # get repeat
        #score = task_score(duration,priority).score    # creating task score
        score = t_score(duration,priority)              # creating task score
        selected = table.focus()    
        values= table.item(selected,'values')
        selected_id = int(values[0])
        table.item(selected, text="", values=(selected_id, name , score , duration , due , priority, repeat))
        duration_option.set("") #reset
        priority_option.set("") #reset
       # print("values", values)
       # print("value id [0]", selected_id)
        #update the database
        with open(filename,"r") as users:
            data = json.load(users)
            taskarray = data['user'][index]['tasks']
            search_id = binary_search(taskarray,selected_id,0)
            if (search_id>=0):
            #for i in taskarray:
                #print("array id num", i[0], type(i[0]))
                #if selected_id == i[0]:
                    target_task  = taskarray[search_id]
                    target_task[0]= selected_id
                    target_task[1]= name
                    target_task[2]= score
                    target_task[3]= duration
                    target_task[4]= due
                    target_task[5]= priority
                    target_task[6]= repeat
           # for i in taskarray:
             #   print("task",i)
             #   print("array id num", i[0], type(i[0]))
              #  if selected_id == i[0]:
                    print ("success")
                    print("new i",target_task)
        #writing the changes into file
            with open(filename, "w") as file:            
                json.dump(data, file, indent=4, default=str)
        #### signify that the task has been added
        complete_label = tk.Label(root,  text="Data updated ", width=10, bg="white" )  
        complete_label.place(x=100,y=400) 
        complete_label.after(3000, lambda: complete_label.destroy()) # remove the message

    ### adding task into the json file
    def add_database(id,name, score, duration, due, priority, repeat):
        with open(filename,"r") as users:
            data = json.load(users)
            if repeat == "Doesn't repeat":
                new_task = [id,name,score, duration, due, priority, repeat ]
            if repeat == "Repeat":
                new_task = [id,name,score, duration, due, priority, repeat,1 ]
            # change to index later
            data['user'][index]["tasks"].append(new_task)
            data['user'][index]["id"] = data['user'][index]["id"]+1
            with open(filename, "w") as file:
                json.dump(data, file, indent=4, default=str)

    ### empty input boxes
    def clear_entry():
         # reset the entry box
            name_text.delete('1.0',END)  
            name_text.focus() 
            duration_option.set("") #reset
            priority_option.set("") #reset
            #### signify that the task has been added
            complete_label = tk.Label(root,  text="Entry Cleared ", width=10 )  
            complete_label.place(x=20,y=370) 
            complete_label.after(3000, lambda: complete_label.destroy()) # remove the message


    #addtask#
    def add_task():
        try: 
            name=name_text.get("1.0",END).rstrip() # read name
            duration=duration_option.get()    # read duration
            due = de.get_date()     #read date
            priority=priority_option.get()      # read imporant/ urgent
            repeat = repeat_option.get()      # get repeat
            if name==''or duration=='' or priority=='' or due =='':
                messagebox.showerror("Error","Entries not filled")
                root.lift()
            else:
                global i

                #create score for object
                #score = task_score(duration,priority).score
                score = t_score(duration,priority)

                #add to database
                add_database(i,name, score, duration, due, priority, repeat)
                table.insert("",'end',values=(i,name,score,duration,due, priority, repeat))
                i=i+1
                # reset the entry box
                name_text.delete('1.0',END)  
                name_text.focus() 
                duration_option.set("") #reset
                priority_option.set("") #reset
                #### signify that the task has been added
                complete_label = tk.Label(root,  text="Data added ", width=10 )  
                complete_label.place(x=20,y=370) 
                complete_label.after(3000, lambda: complete_label.destroy()) # remove the message
        except:
            messagebox.showerror("Error","Entries not filled correctly")
            root.lift()

    #### user interface design for task page

    add_task_label = tk.Label(root,  text='Add Task',
              font=('Helvetica', 14), width=20)  
    add_task_label.place(x=750,y=0)

    #name label
    name_label = tk.Label(root,  text='Name: ', width=10)  
    name_label.place(x=750,y=50)

    # name textbox input
    name_text = tk.Text(root,  height=1, width=10,bg='white') 
    name_text.place(x=820,y=50)

    #duration label
    duration_label = tk.Label(root,  text='Duration: ', width=10 )  
    duration_label.place(x=750,y=100)

    # task duration label
    duration_option = StringVar(root)
    duration_option.set("") # default value

    ### duration optionalmenu input
    option_name_text = OptionMenu(root, duration_option, 30, 60, "90+")
    option_name_text.place(x=820,y=100)

    # task due label
    due_label = tk.Label(root,  text='Due: ', width=10 )  
    due_label.place(x=750,y=150)


    #task due date entry
    de = MyDateEntry(root, year=2023, month=1, day=1,
        selectbackground='gray80',
        selectforeground='black',
        normalbackground='white',
        normalforeground='black',
        background='gray90',
        foreground='black',
        bordercolor='gray90',
        othermonthforeground='gray50',
        othermonthbackground='white',
        othermonthweforeground='gray50',
        othermonthwebackground='white',
        weekendbackground='white',
        weekendforeground='black',
        headersbackground='white',
        headersforeground='gray70')
    de.place(x=820,y=150)

    # task priority label
    priority_label = tk.Label(root,  text='Priority: ', width=10 )  
    priority_label.place(x=750,y=200)

    priority_option = StringVar(root)
    priority_option.set("") # default value

    # task priority options
    priority_om = OptionMenu(root, priority_option,  "Important", "Urgent")
    priority_om.place(x=820,y=200)

    # task repetition label
    repeat_label = tk.Label(root,  text='Repeat: ', width=10 )  
    repeat_label.place(x=750,y=250)

    repeat_option = StringVar(root)
    repeat_option.set("Doesn't repeat") # default value
    
    # task repeat options
    repeat_om = OptionMenu(root, repeat_option, "Doesn't repeat", "Repeat")
    repeat_om.place(x=820,y=250)

    #### area of further development is to repeat in a fixed schedule

    #add task button
    add_task_button = tk.Button(root,  text='Add Record', width=10, 
                command= add_task)  
    add_task_button.place(x=810,y=330)

    ### signify that the task has been added
    my_str = tk.StringVar()
    complete_label = tk.Label(root,  textvariable=my_str, width=10 )  
    complete_label.place(x=100,y=400) 

    ### close window
    close_button = tk.Button(root,  text='Close', width=10, 
                command=root.destroy)  
    close_button.place(x=260,y=400)

    # clear task entry
    clear_button = tk.Button(root,  text='Clear Entry', width=10, 
                command=lambda: clear_entry())  
    clear_button.place(x=810,y=400)

    #edit task
    #edit_button = tk.Button(root,  text='Edit', width=10, 
           #    command= lambda:editTask())  
   # edit_button.place(x=810,y=450)

    #sort by date
    sort_date_button = tk.Button(root,  text='Sort by date', width=10, 
                command= lambda:sort_date(taskarray, table))  
    sort_date_button.place(x=615,y=370)

    #sort by task score
    sort_score_button = tk.Button(root,  text='Sort by score', width=10, 
                command= lambda:sort_score(taskarray, table))  
    sort_score_button.place(x=520,y=370)

    #delete task
    delete_button = tk.Button(root,  text='Delete Task', width=10, 
                command= lambda:remove_task(table))  
    delete_button.place(x=730,y=450)

    #update task
    update_button = tk.Button(root,  text='Update', width=10, 
                command= lambda:update_task())  
    update_button.place(x=880,y=450)


    # binding funciton to tree
    table.bind("<ButtonRelease-1>",editTask)


# Get selected item to Delete
def delete(table):
    selected_item = table.selection()[0]
    table.delete(selected_item)



######## complete task page
def daily_task():

    #Create an instance of tkinter frame
    root = Tk()
    root.geometry('935x500')
    root.title("Daily task")
    root.resizable(False,False)
    #Configure the background
    root.config(bg='white')
    #Create Entry Widgets for HH MM SS
    sec = StringVar(root)
    Entry(root, textvariable=sec, width = 2, font = 'Helvetica 14').place(x=467, y=120)
    sec.set('00')
    mins= StringVar(root)
    Entry(root, textvariable = mins, width =2, font = 'Helvetica 14').place(x=427, y=120)
    mins.set('00')
    hrs= StringVar(root)
    Entry(root, textvariable = hrs, width =2, font = 'Helvetica 14').place(x=389, y=120)
    hrs.set('00')
    #Define the function for the timer
    def delete_task():
        select = table.focus()
        values= table.item(select,'values')
        selected_id = int(values[0])
      #  print(values[6])
        if (values[6] == "Doesn't repeat"):
            with open(filename,"r") as users:
                data = json.load(users)
                taskarray = data['user'][index]['tasks']
              #  for i in taskarray:
              #      print(i[0])
               #     if int(values[0]) == i[0]:
              #          taskarray.remove(i)
                #print ("id num ta", taskarray[0][0], "type",type(taskarray[0][0]))
                search_id = binary_search(taskarray,selected_id,0)
               # print ("serach index", search_id)
                if (search_id>=0):
                #for i in taskarray:
                    #print("array id num", i[0], type(i[0]))
                    #if selected_id == i[0]:
                        target_task  = taskarray[search_id]
                        taskarray.remove(target_task)
                        
                with open(filename, "w") as file:
                    json.dump(data, file, indent=4, default=str)
        #Changing the due date if it is a repeating task
        if (values[6] == "Repeat"):
            with open(filename,"r") as users:
                data = json.load(users)
                taskarray = data['user'][index]['tasks']
                for i in taskarray:
                     if int(values[0]) == i[0]:
                        Begindate = datetime.strptime(i[4], "%Y-%m-%d")
                        i[4] = Begindate + timedelta(days=i[7])
                        i[7] = i[7]*2
                        i[4]=i[4].strftime("%Y-%m-%d")
                with open(filename, "w") as file:
                    json.dump(data, file, indent=4, default=str)

    # countdown timer for task completion
    def countdowntimer():
        ## running the timer ##
        try:
            selected_item = table.selection()[0]
            selected_item
            times = int(hrs.get())*3600+ int(mins.get())*60 + int(sec.get())
            while times > -1:
                minute,second = (times // 60 , times % 60)
                hour =0
                if minute > 60:
                    hour , minute = (minute // 60 , minute % 60)
                sec.set(second)
                mins.set(minute)
                hrs.set(hour)
                #Update the time
                root.update()
                time.sleep(1)
                if(times == 0):
                    sec.set('00')
                    mins.set('00')
                    hrs.set('00')
                times -= 1

                if (times == 0):
                    messagebox.showinfo("Time Countdown", "Time's up ")
                    delete_task()
                    delete(table)
                    root.lift()
        # when there is no task selected error message will show        
        except:
                messagebox.showerror("Error","No task was selected")
                root.lift()

    # window configuration
    Label(root, font =('Helvetica bold',22), text = 'Set the Timer',bg='White').place(x=345,y=70)
    Button(root, text='START', bd ='2', bg = 'White',font =('Helvetica bold',10),
            command = countdowntimer).place(x=407, y=165)
    Button(root, text='Close', bd ='2', bg = 'White',font =('Helvetica bold',10),
            command= root.destroy ).place(x=407, y=465)
    



    #table layout
    table=ttk.Treeview(root,selectmode='browse')
    table["columns"]=("1","2","3","4","5","6","7")
    table['show']='headings'
    table.column("1",width=40,anchor='c')
    table.column("2",width=200,anchor='c')
    table.column("3",width=80,anchor='c')
    table.column("4",width=70,anchor='c')
    table.column("5",width=80,anchor='c')
    table.column("6",width=80,anchor='c')
    table.column("7",width=100,anchor='c')
    table.heading("1",text="Task")
    table.heading("2",text="Name")
    table.heading("3",text="Score")
    table.heading("4",text="Duration")
    table.heading("5",text="Due")
    table.heading("6", text = "Priority")
    table.heading("7",text="Repeat")
    #positioning of the table
    table.place(x=100,y=200)
    table.anchor(CENTER)

    # print task database
    with open(filename,"r") as users:
        data = json.load(users)
        taskarray = data['user'][index]['tasks']
    #printtTables(taskarray,table,current_date)
    printDailytask(taskarray,table,current_date)


    root.mainloop()







# login page screen
def loginpage():

    #login function
    def login():
        ### calling global variables
        global index, i
        username=user.get()
        userpass=password.get()
        ## reading through json database for existing username
        with open(filename,"r") as users:
            data = json.load(users)
            for name in data['user']:
                #name iterates through dictionary of users in the user array
                if username == name['username'] and userpass == name['password']:
                    # setting the index of the user in the json file
                    index = data['user'].index(name)
                    # setting the id to track the number the of tasks the user has
                    i = name['id']
                    root.withdraw() 
                    main_screen()
                else:
                    Label(text="*Invalid username and password*",
                           fg="red",bg="white",font=("Calibri",11)).place(x=360,y=370)
                    password.delete(0,"end")

    ###create an account function page
    def createacc():
        #page layout
        homepage = Toplevel(root)
        homepage.title("Create an account")
        homepage.geometry("935x500+500+200")
        homepage.configure(bg="white")

        frame=Frame(homepage,width=350,height=350,bg="white")
        frame.place(x=300,y=70)

        heading=Label(frame,text="New account", fg="#57a1f8",bg="white",font=("Calibri",23,"bold"))
        heading.place(x=85,y=5)

        # username entry
        def cursor_on(e):
            name=user_entry.get()
            if name=="" or name=="Username":
                user_entry.delete(0,"end")
            

        def cursor_off(e):
            name=user_entry.get()
            if name=="":
                user_entry.insert(0,"Username")

        user_entry= Entry(frame,width=25, border=2,bg="white",font=("Calibri",12,"bold"))
        user_entry.place(x=70,y=90)
        user_entry.insert(0,"Username")
        user_entry.bind("<FocusIn>",cursor_on)
        user_entry.bind("<FocusOut>",cursor_off)

        #password entry
        def cursor_on(e):
            name=password.get()
            if name=="" or name=="Password":
                password.delete(0,"end")

        def cursor_off(e):
            name=password.get()
            if name=="":
                password.insert(0,"Password")
        password= Entry(frame,width=25, border=2,bg="white",font=("Calibri",12,"bold"))
        password.place(x=70,y=150)
        password.insert(0,"Password")
        password.bind("<FocusIn>",cursor_on)
        password.bind("<FocusOut>",cursor_off)

        #reenter password entry
        def cursor_on(e):
            name=reenter_pass.get()
            if name=="" or name=="Re-enter password":
                reenter_pass.delete(0,"end")

        def cursor_off(e):
            name=reenter_pass.get()
            if name=="":
                reenter_pass.insert(0,"Re-enter password")
        reenter_pass= Entry(frame,width=25, border=2,bg="white",font=("Calibri",12,"bold"))
        reenter_pass.place(x=70,y=210)
        reenter_pass.insert(0,"Re-enter password")
        reenter_pass.bind("<FocusIn>",cursor_on)
        reenter_pass.bind("<FocusOut>",cursor_off)


    #validation function
        def verification():
            username = user_entry.get()
            userpass = password.get()
            reenter_password = reenter_pass.get()

            password.delete(0, END)
            reenter_pass.delete(0, END)

            if userpass!=reenter_password:
                messagebox.showwarning("Error", "Invalid submission, please retry.")
                homepage.lift()
            elif username == "" or password == "" or username == "Username":
                messagebox.showwarning("Error", "Username or password not entered, please retry.") 
                homepage.lift()

            else:   

                #### new empty user
                new = {
                        "username":username,
                        "password":userpass,
                        "id" : 1,
                        "tasks":[]
                        }
                #read through json file to see if username already exists
                with open(filename,"r") as users:
                    data = json.load(users)
                    test = False
                    for name in data['user']:
                            #name iterates through dictionary of users in the user array
                            if username == name['username']:
                                messagebox.showwarning("Error", "Username already exists, please retry.") 
                                homepage.lift() 
                                test = True
                                break
                    # write new user
                    if test == False:
                        data['user'].append(new)
                        with open(filename, "w") as file:
                                json.dump(data, file, indent=4)
                        #print (data)
                        messagebox.showinfo("Success", "Account successfuly created.")
                        homepage.destroy()

            

    ##### enter button and create account button
        enter=Button(frame,width=30,pady=6,text="Create", bg="#57a1f8",fg="white", border=0,font=("Calibri",12,"bold"),command=verification)
        enter.place(x=50,y=300)
    ## login page layout
    root=Tk()
    root.title("Sign in")
    root.geometry("935x500+500+200")
    root.configure(bg="white")
    root.resizable(False,False)
    #frame to put the login
    frame=Frame(root,width=350,height=350,bg="white")
    frame.place(x=300,y=70)

    heading=Label(frame,text="Sign in", fg="#57a1f8",bg="white",font=("Calibri",23,"bold"))
    heading.place(x=120,y=5)

    ###### prompt for username
    def cursor_on(e):
        name=user.get()
        if name=="" or name=="Username":
            user.delete(0,"end")


    def cursor_off(e):
        name=user.get()
        if name=="":
            user.insert(0,"Username")

    user= Entry(frame,width=25, border=2,bg="white",font=("Calibri",12,"bold"))
    user.place(x=70,y=90)
    user.insert(0,"Username")
    user.bind("<FocusIn>",cursor_on)
    user.bind("<FocusOut>",cursor_off)

    ########### prompt for password
    def cursor_on(e):
        name=password.get()
        if name=="" or name=="Password":
            password.delete(0,"end")


    def cursor_off(e):
        name=password.get()
        if name=="":
            password.insert(0,"Password")

    password= Entry(frame,width=25, border=2,bg="white",font=("Calibri",12,"bold"))
    password.place(x=70,y=150)
    password.insert(0,"Password")
    password.bind("<FocusIn>",cursor_on)
    password.bind("<FocusOut>",cursor_off)

    ##### enter button and create account button
    enter=Button(frame,width=30,pady=6,text="Sign in", bg="#57a1f8",fg="white", border=0,font=("Calibri",12,"bold"),command=login)
    enter.place(x=50,y=200)
    ##label= Label(frame,text="Create new account", fg="blue",bg="white",font=("Calibri",9)).place(x=120,y=270)

    sign_up= Button(frame,text="Create new account", bg="white",fg="#57a1f8", border=0,cursor="hand2", command=createacc )
    sign_up.place(x=115,y=270)

    root.mainloop()

loginpage()