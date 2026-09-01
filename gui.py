import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import task_manager


def refresh_list(tree, filter_var):
    # Goleste tabelul actual
    for row in tree.get_children():
        tree.delete(row)

    # Preia sarcinile si le afiseaza in tabel
    current_filter = filter_var.get()
    for t in task_manager.get_tasks(current_filter):
        tree.insert("", "end", iid=t["id"], values=(t["name"], t["status"]))


def handle_add(entry_name, status_var, tree, filter_var):
    # Preia textul si adauga sarcina
    name = entry_name.get()
    status = status_var.get()
    if name:
        task_manager.add_task(name, status)
        entry_name.delete(0, tk.END)
        refresh_list(tree, filter_var)
    else:
        messagebox.showwarning("Eroare", "Introdu un nume pentru sarcina!")


def handle_delete(tree, filter_var):
    # Sterge randul selectat
    selected = tree.selection()
    if selected:
        task_id = int(selected[0])
        task_manager.delete_task(task_id)
        refresh_list(tree, filter_var)
    else:
        messagebox.showwarning("Eroare", "Selecteaza o sarcina!")


def handle_edit(entry_name, status_var, tree, filter_var):
    # Modifica randul selectat cu datele noi
    selected = tree.selection()
    if selected:
        task_id = int(selected[0])
        new_name = entry_name.get()
        new_status = status_var.get()
        if new_name:
            task_manager.edit_task(task_id, new_name, new_status)
            refresh_list(tree, filter_var)
        else:
            messagebox.showwarning("Eroare", "Introdu un nume nou!")
    else:
        messagebox.showwarning("Eroare", "Selecteaza o sarcina pentru editare!")


def handle_export(filter_var):
    # Alege locatia si exporta fisierul
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filename:
        current_filter = filter_var.get()
        task_manager.export_to_csv(filename, current_filter)
        messagebox.showinfo("Succes", "Export finalizat!")


def setup_gui(root):
    # Configurare fereastra
    root.title("ToDo List")
    root.geometry("600x500")

    # Sectiunea de input (Nume si Status)
    frame_input = tk.Frame(root)
    frame_input.pack(pady=10)

    tk.Label(frame_input, text="Nume Sarcina:").grid(row=0, column=0, padx=5)
    entry_name = tk.Entry(frame_input, width=20)
    entry_name.grid(row=0, column=1, padx=5)

    tk.Label(frame_input, text="Status:").grid(row=0, column=2, padx=5)
    status_var = tk.StringVar(value="nou")
    status_combo = ttk.Combobox(frame_input, textvariable=status_var, values=["nou", "in progres", "finalizat"],
                                state="readonly")
    status_combo.grid(row=0, column=3, padx=5)

    # Butoanele principale de actiune
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=5)
    tk.Button(frame_buttons, text="Adauga", command=lambda: handle_add(entry_name, status_var, tree, filter_var)).grid(
        row=0, column=0, padx=5)
    tk.Button(frame_buttons, text="Editeaza",
              command=lambda: handle_edit(entry_name, status_var, tree, filter_var)).grid(row=0, column=1, padx=5)
    tk.Button(frame_buttons, text="Sterge", command=lambda: handle_delete(tree, filter_var)).grid(row=0, column=2,
                                                                                                  padx=5)

    # Sectiunea de filtrare si export
    frame_filter = tk.Frame(root)
    frame_filter.pack(pady=15)
    tk.Label(frame_filter, text="Filtreaza:").grid(row=0, column=0, padx=5)

    filter_var = tk.StringVar(value="Toate")
    filter_combo = ttk.Combobox(frame_filter, textvariable=filter_var,
                                values=["Toate", "nou", "in progres", "finalizat"], state="readonly")
    filter_combo.grid(row=0, column=1, padx=5)

    tk.Button(frame_filter, text="Aplica Filtru", command=lambda: refresh_list(tree, filter_var)).grid(row=0, column=2,
                                                                                                       padx=5)
    tk.Button(frame_filter, text="Export CSV (Lista Curenta)", command=lambda: handle_export(filter_var)).grid(row=0,
                                                                                                               column=3,
                                                                                                               padx=5)

    # Tabelul in care afisam sarcinile
    tree = ttk.Treeview(root, columns=("Nume", "Status"), show="headings")
    tree.heading("Nume", text="Sarcina")
    tree.heading("Status", text="Status")
    tree.pack(expand=True, fill="both", padx=20, pady=10)

    # Afiseaza initial lista goala
    refresh_list(tree, filter_var)