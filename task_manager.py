import csv

# Lista in care pastram sarcinile
tasks = []
task_id_counter = 1

def add_task(name, status="nou"):
    # Creaza si adauga o sarcina noua
    global task_id_counter
    task = {"id": task_id_counter, "name": name, "status": status}
    tasks.append(task)
    task_id_counter += 1

def delete_task(task_id):
    # Cauta sarcina dupa ID si o sterge
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]

def edit_task(task_id, new_name, new_status):
    # Gaseste sarcina si ii schimba numele si statusul
    for t in tasks:
        if t["id"] == task_id:
            t["name"] = new_name
            t["status"] = new_status
            break

def get_tasks(status_filter=None):
    # Returneaza lista, aplicand filtrul de status daca exista
    if status_filter and status_filter != "Toate":
        return [t for t in tasks if t["status"] == status_filter]
    return tasks

def export_to_csv(filename, status_filter=None):
    # Exporta sarcinile (filtrate sau nu) in fisier CSV
    filtered_tasks = get_tasks(status_filter)
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Sarcina", "Status"])
        for t in filtered_tasks:
            writer.writerow([t["id"], t["name"], t["status"]])