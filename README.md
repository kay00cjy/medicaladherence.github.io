<!DOCTYPE html>
<html>
<head>
    <title>Medication Schedule Input</title>
    <script>
        function addToTable() {
            let table = document.getElementById("scheduleTable");
            let row = table.insertRow(-1);

            let date = document.getElementById("date").value;
            let time = document.getElementById("time").value;
            let name = document.getElementById("name").value;
            let compartment = document.getElementById("compartment").value;

            if (!date || !time || !name || !compartment) {
                alert("Please fill in all fields!");
                return;
            }

            row.insertCell(0).innerHTML = compartment;
            row.insertCell(1).innerHTML = date;
            row.insertCell(2).innerHTML = time;
            row.insertCell(3).innerHTML = name;
        }

        function sendData() {
            let table = document.getElementById("scheduleTable");
            let data = [];

            for (let i = 1; i < table.rows.length; i++) {
                let cells = table.rows[i].cells;
                data.push({
                    "compartment": cells[0].innerText,
                    "date": cells[1].innerText,
                    "time": cells[2].innerText,
                    "name": cells[3].innerText
                });
            }

            fetch("http://localhost:5000/sendData", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            }).then(response => response.text()).then(data => {
                alert("Data Sent: " + data);
            }).catch(error => {
                alert("Error sending data! Is your Python server running?");
            });
        }
    </script>
</head>
<body>
    <h2>Enter Medication Schedule</h2>
    
    <label>Recurring Date:</label>
    <input type="date" id="date"><br><br>
    
    <label>Time:</label>
    <input type="time" id="time"><br><br>

    <label>Medication Name:</label>
    <input type="text" id="name"><br><br>

    <label>Compartment (1-14):</label>
    <input type="number" id="compartment" min="1" max="14"><br><br>

    <button type="button" onclick="addToTable()">Add to Schedule</button>

    <h3>Medication Schedule</h3>
    <table border="1" id="scheduleTable">
        <tr>
            <th>Compartment</th>
            <th>Date</th>
            <th>Time</th>
            <th>Medication</th>
        </tr>
    </table>

    <button type="button" onclick="sendData()">Submit Schedule</button>
</body>
</html>
