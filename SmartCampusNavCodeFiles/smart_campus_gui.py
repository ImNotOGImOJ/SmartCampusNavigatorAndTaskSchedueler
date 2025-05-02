import tkinter as tk
from tkinter import messagebox, ttk
from campus_logic import campus_graph, building_names, dijkstra, get_path, kmp_search

def show_shortest_path():
    start = start_var.get()
    end = end_var.get()

    if start == end:
        messagebox.showinfo("Info", "Start and end buildings are the same.")
        return

    distances, previous = dijkstra(campus_graph, start)
    path = get_path(previous, end)
    if distances[end] < float('inf'):
        result = f"Shortest path: {' -> '.join(path)}\nDistance: {distances[end]}"
    else:
        result = "No path found."
    result_label.config(text=result)

def search_building():
    pattern = search_entry.get().strip().lower()
    combined_names = ' '.join(building_names).lower()
    matches = kmp_search(combined_names, pattern)
    if matches:
        messagebox.showinfo("Search Result", f"Building name '{pattern}' found!")
    else:
        messagebox.showinfo("Search Result", f"'{pattern}' not found in building names.")

# GUI Setup
root = tk.Tk()
root.title("Smart Campus Navigator")
root.geometry("400x300")

tk.Label(root, text="Select Start Building:").pack()
start_var = tk.StringVar(value=building_names[0])
ttk.Combobox(root, textvariable=start_var, values=building_names).pack()

tk.Label(root, text="Select End Building:").pack()
end_var = tk.StringVar(value=building_names[1])
ttk.Combobox(root, textvariable=end_var, values=building_names).pack()

tk.Button(root, text="Find Shortest Path", command=show_shortest_path).pack(pady=10)
result_label = tk.Label(root, text="", fg="blue")
result_label.pack()

tk.Label(root, text="Search for Building Name:").pack(pady=10)
search_entry = tk.Entry(root)
search_entry.pack()
tk.Button(root, text="Search", command=search_building).pack()

root.mainloop()
