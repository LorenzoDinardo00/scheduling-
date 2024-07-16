import matplotlib.pyplot as plt


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

    while time < duration:
        for task in tasks:
            if time % task.period == 0:
                ready_queue.append(Task(task.id, task.period, task.wcet))

        if preemptive:
            ready_queue = sorted(ready_queue, key=lambda x: x.period)

        if ready_queue:
            current_task = ready_queue[0]
            if current_task.remaining_time > 0:
                timeline.append(current_task.id)
                current_task.remaining_time -= 1
                if current_task.remaining_time == 0:
                    ready_queue.pop(0)
            else:
                timeline.append(0)
        else:
            timeline.append(0)

        time += 1

    return timeline


def schedule_edf(tasks, duration, preemptive=True):
    timeline = []
    time = 0
    ready_queue = []

    while time < duration:
        for task in tasks:
            if time % task.period == 0:
                ready_queue.append(Task(task.id, task.period, task.wcet))

        if preemptive:
            ready_queue = sorted(ready_queue, key=lambda x: x.next_deadline)

        if ready_queue:
            current_task = ready_queue[0]
            if current_task.remaining_time > 0:
                timeline.append(current_task.id)
                current_task.remaining_time -= 1
                if current_task.remaining_time == 0:
                    ready_queue.pop(0)
            else:
                timeline.append(0)
        else:
            timeline.append(0)

        time += 1

    return timeline


def plot_timeline(timeline, title):
    plt.figure(figsize=(10, 2))
    plt.plot(timeline, drawstyle='steps-post')
    plt.yticks(range(1, max(timeline) + 1))
    plt.xlabel("Time")
    plt.ylabel("Task ID")
    plt.title(title)
    plt.show()


def main():
    tasks = input_tasks()
    duration = int(input("Inserisci la durata dello scheduling: "))

    print("\nScheduling FPS Preemptive")
    fps_preemptive = schedule_fps(tasks, duration, preemptive=True)
    plot_timeline(fps_preemptive, "FPS Preemptive Scheduling")

    print("\nScheduling FPS Non-Preemptive")
    fps_non_preemptive = schedule_fps(tasks, duration, preemptive=False)
    plot_timeline(fps_non_preemptive, "FPS Non-Preemptive Scheduling")

    print("\nScheduling EDF Preemptive")
    edf_preemptive = schedule_edf(tasks, duration, preemptive=True)
    plot_timeline(edf_preemptive, "EDF Preemptive Scheduling")

    print("\nScheduling EDF Non-Preemptive")
    edf_non_preemptive = schedule_edf(tasks, duration, preemptive=False)
    plot_timeline(edf_non_preemptive, "EDF Non-Preemptive Scheduling")


if __name__ == "__main__":
    main()