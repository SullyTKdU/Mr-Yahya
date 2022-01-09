    for items in item:
      for j in range(len(items)):
        e = ttk.Entry(self.window, width=10, foreground='blue',justify="center" )
        e.grid(row=i, column=j)
        e.insert(END,items[j])
      i=i+1