import random
import datetime
import time
import keyboard  # type: ignore
import matplotlib.pyplot as plt # type: ignore

LOG_FILE_PATH = "medication_log.txt"

# Global variable for the figure and axis to persist across days
fig, ax = plt.subplots(figsize=(6, 1))

def show_progress_bar(dosesTaken, medsPerDay):
    # Clear the previous plot content
    ax.clear()

    # Set the axis off each time you update
    ax.set_axis_off()

    # Create the outline of the progress bar
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='white'))

    # Calculate the fill proportion based on doses taken
    fill_ratio = dosesTaken / medsPerDay

    # Add the filled section of the progress bar
    ax.add_patch(plt.Rectangle((0, 0), fill_ratio, 1, linewidth=0, edgecolor='none', facecolor='green'))

    # Set the aspect ratio to 'auto' to allow elongation
    ax.set_aspect('auto')

    # Update the plot
    plt.draw()
    plt.pause(0.1)

def dayBasedEncourage(currentDay):
    messages = {
        "Monday": [
            "I know Mondays are terrible, nevertheless... Great job you addict! ",
            "The start to the week is usually sucky but... I'm really proud of you!",
            "Garfield really hates today, however... You're doing a good job buddy!"
        ],
        "Tuesday": [
            "At least it's not Monday, right? Regardless... Dementia who? Good stuff!",
            "We're two days into the week. Hang in there!",
            "Tuesday's can be kinda poopy but...Taking care of yourself, huh? Yay!"
        ],
        "Wednesday": [
            "You've made it to the hump, not much more to go!",
            "Halfway there, you're doing great!",
            "It's the middle of the week, you're basically there!"
        ],
        "Thursday": [
            "Keep pushing, Friday is just around the corner!",
            "The week is almost done, keep at it!",
            "The weekend is nearly here, you gotta lock in brah"
        ],
        "Friday": [
            "Friday! Friyay! I love fries, do you?",
            "You made it through the week!",
            "We going to party hard tonight with all these pills hehe."
        ],
        "Saturday": [
            "We made it to the weekend!",
            "You did a good job, now go and recharge!",
            "Saturdays are the day to really kick back and relax!"
        ],
        "Sunday": [
            "Well, at least we don't have to go to Church, am I right?",
            "It's the last day of the week, Monday is coming...",
            "Time to really rest up today, because come tomorrow, the shit show starts again..."
        ]
    }

    print(random.choice(messages[currentDay]))

def getNextDay(currentDay):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    next_index = (days.index(currentDay) + 1) % 7  # Loops back to Monday after Sunday
    return days[next_index]

def loggingMedicationData(medsTaken, currentDay, medsPerDay):
    """Log medication intake into a file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - Day: {currentDay}, Meds Taken: {medsTaken} / {medsPerDay}\n"
    
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(log_message)

def dailyRoutine():
    global currentDay, medsPerDay, perfectDays  

    while True:

        interactions = 0
        medsTaken = 0
        
        while interactions < medsPerDay:
            print(f"\nInteraction {interactions + 1} / {medsPerDay} for {currentDay}.")
            response = input("Did the patient take their meds? (yes/no): ").strip().lower()

            if response == "yes":
                medsTaken += 1
                dayBasedEncourage(currentDay)
                show_progress_bar(medsTaken, medsPerDay)
            elif response == "no":
                print("Bummer, maybe next time?")
            elif response == "d":
                print("\nDay is being manually changed!")
                dayOfWeek()  
                return  
            elif response == "m":
                print("\nMedication count is being manually changed!")
                setMedsPerDay()  
                return  
            else:
                print("Invalid input. Please enter only 'yes' or 'no'.")
                continue

            interactions += 1

        print(f"\nThat's all for today. You took your meds {medsTaken} / {medsPerDay} times today.")
        if medsTaken == medsPerDay:
            print("\nWoohoo! Perfect Day! Great job, you did phenomenally today 🙂")
            perfectDays += 1  
        else:
            perfectDays = 0  

        loggingMedicationData(medsTaken, currentDay, medsPerDay)

        if perfectDays % 7 == 0 and perfectDays != 0:
            print("\n\nYay, another week done perfectly! You are amazing!")

        time.sleep(0.5)

        # Clear the progress bar and reset it for the next day
        ax.clear()  # Reset the progress bar each day
        ax.set_axis_off()  # Keep the axis off after clearing
        plt.draw()
        plt.pause(0.1)
        
        currentDay = getNextDay(currentDay)
        print(f"Switching to {currentDay}. Hope you're ready for it!")

def setMedsPerDay():
    global medsPerDay

    while True:
        try:
            medsPerDay = int(input("Please enter the number of times the patient takes medicine per day: "))
            if medsPerDay <= 0:
                print("Now that's not really possible, is it?")
                continue

            if medsPerDay > 50:
                response = input("That's kind of ridiculous. Are you sure? (yes/no) \n").strip().lower()
                if response == "yes":
                    break
                if response == "no":
                    print("Please enter the correct value")
                    continue
                else:
                    print("That's not a valid response, please just enter yes or no")
                    continue

            break
        except ValueError:
            print("Please enter a valid number...")

def dayOfWeek():
    global currentDay, medsPerDay, perfectDays  

    perfectDays = 0  

    while True:
        print("\nWhat day of the week is it? Please enter a number from 1-7")  
        try:
            dayNumber = int(input("> "))  
            if dayNumber < 1 or dayNumber > 7:
                print("Please enter a number between 1 and 7.")
                continue

            days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
            currentDay = days[dayNumber]  
            print(f"Today is {currentDay}. Thank you.")

            print("Press 'm' at any time to change the medication count.")
            print("Press 'd' at any time to change the day of the week.")
            dailyRoutine()

        except ValueError:
            print("Please enter an actual number.")

# Start the main program
setMedsPerDay()  
dayOfWeek()
