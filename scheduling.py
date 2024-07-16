import matplotlib.pyplot as plt
from IPython.display import Image, display


class Task:
    def __init__(self, id, period, wcet):
        self.id = id
        self.period = period
        self.wcet = wcet
        self.remaining_time = wcet
        self.next_deadline = period

    def __repr__(self):
        return f"Task(id={self.id}, period={self.period}, wcet={self.wcet})"


def input_tasks():
    tasks = []
    num_tasks = int(input("Inserisci il numero di task: "))
    for i in range(num_tasks):
        period = int(input(f"Inserisci il periodo del task {i + 1}: "))
        wcet = int(input(f"Inserisci il WCET del task {i + 1}: "))
        tasks.append(Task(id=i + 1, period=period, wcet=wcet))
    return tasks


def schedule_fps(tasks, duration, preemptive=True):
    tasks = sorted(tasks, key=lambda x: x.period)
    timeline = []
    time = 0
    ready_queue = []
    current_task = None

    while time < duration:
        # Aggiungi nuovi task alla ready_queue
        for task in tasks:
            if time % task.period == 0:
                ready_queue.append(Task(task.id, task.period, task.wcet))

        if preemptive:
            ready_queue = sorted(ready_queue, key=lambda x: x.period)
        else:
            if not current_task or current_task.remaining_time == 0:
                if ready_queue:
                    ready_queue = sorted(ready_queue, key=lambda x: x.period)
                    current_task = ready_queue.pop(0)

        if preemptive:
            if ready_queue:
                current_task = ready_queue[0]
                # Esegui il task corrente
                if current_task.remaining_time > 0:
                    timeline.append(current_task.id)
                    current_task.remaining_time -= 1
                    # Rimuovi il task dalla ready_queue se è completato
                    if current_task.remaining_time == 0:
                        ready_queue.pop(0)
                else:
                    timeline.append(0)
            else:
                timeline.append(0)
        else:
            if current_task:
                timeline.append(current_task.id)
                current_task.remaining_time -= 1
                if current_task.remaining_time == 0:
                    current_task = None
            else:
                timeline.append(0)

        time += 1

    return timeline


def schedule_edf(tasks, duration, preemptive=True):
    timeline = []
    time = 0
    ready_queue = []
    current_task = None

    while time < duration:
        # Aggiungi nuovi task alla ready_queue con la deadline corretta
        for task in tasks:
            if time % task.period == 0:
                new_task = Task(task.id, task.period, task.wcet)
                new_task.next_deadline = time + task.period
                ready_queue.append(new_task)

        # Ordina la ready_queue in base alla deadline
        ready_queue = sorted(ready_queue, key=lambda x: x.next_deadline)

        # Se c'è un task corrente, controlla se deve essere preempted
        if current_task:
            if preemptive and ready_queue and ready_queue[0].next_deadline < current_task.next_deadline:
                # Preempt il task corrente
                ready_queue.append(current_task)
                ready_queue = sorted(ready_queue, key=lambda x: x.next_deadline)
                current_task = ready_queue.pop(0)

        # Esegui il task corrente
        if current_task and current_task.remaining_time > 0:
            timeline.append(current_task.id)
            current_task.remaining_time -= 1
            if current_task.remaining_time == 0:
                current_task = None
        else:
            if ready_queue:
                current_task = ready_queue.pop(0)
                timeline.append(current_task.id)
                current_task.remaining_time -= 1
                if current_task.remaining_time == 0:
                    current_task = None
            else:
                timeline.append(0)

        time += 1

    return timeline


def plot_timeline(timeline, title, filename):
    plt.figure(figsize=(10, 2))
    times = range(len(timeline))
    plt.step(times, timeline, where='post', linestyle='-', marker='|')
    plt.yticks(range(1, max(timeline) + 1))
    plt.xlabel("Time")
    plt.ylabel("Task ID")
    plt.title(title)

    # Aggiungi i valori delle ascisse nei punti di cambio task
    for i in range(len(timeline)):
        if i > 0 and timeline[i] != timeline[i - 1]:
            plt.text(i, timeline[i], str(i), fontsize=8, ha='center', va='bottom')

    # Evidenzia gli idle con linee trasparenti
    for i in range(len(timeline)):
        if timeline[i] == 0:
            plt.axvspan(i, i + 1, color='gray', alpha=0.3)

    plt.savefig(filename)
    plt.show()  # Aggiungi plt.show() per visualizzare il grafico


def main():
    tasks = input_tasks()
    duration = int(input("Inserisci la durata dello scheduling: "))

    print("\nScheduling FPS Preemptive")
    fps_preemptive = schedule_fps(tasks, duration, preemptive=True)
    plot_timeline(fps_preemptive, "FPS Preemptive Scheduling", "fps_preemptive.png")

    print("\nScheduling FPS Non-Preemptive")
    fps_non_preemptive = schedule_fps(tasks, duration, preemptive=False)
    plot_timeline(fps_non_preemptive, "FPS Non-Preemptive Scheduling", "fps_non_preemptive.png")

    print("\nScheduling EDF Preemptive")
    edf_preemptive = schedule_edf(tasks, duration, preemptive=True)
    plot_timeline(edf_preemptive, "EDF Preemptive Scheduling", "edf_preemptive.png")

    print("\nScheduling EDF Non-Preemptive")
    edf_non_preemptive = schedule_edf(tasks, duration, preemptive=False)
    plot_timeline(edf_non_preemptive, "EDF Non-Preemptive Scheduling", "edf_non_preemptive.png")


if __name__ == "__main__":
    main()