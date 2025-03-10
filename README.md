<!DOCTYPE html>
<html>
</head>
    <title>Medication Schedule Input</h1>
    <script>
        let scheduleData = [];

        function addToTable() {
            let table = document.getElementById("scheduleTable");
            let compartment = document.getElementById("compartment").value;
            let date = document.getElementById("date").value;
            let time = document.getElementById("time").value;
            let name = document.getElementById("name").value;

            if (!date || !time || !compartment) {
                alert("Please fill in all fields!");
                return;
            }

            // Store data in an array (not table directly)
            scheduleData.push({ compartment: parseInt(compartment), date, time, name });

            // Sort array based on compartment number
            scheduleData.sort((a, b) => a.compartment - b.compartment);

            // Refresh table display
            updateTable();
        }

        function updateTable() {
            let table = document.getElementById("scheduleTable");
            table.innerHTML = `
                <tr>
                    <th>Compartment</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Medication</th>
                </tr>`;

            scheduleData.forEach(entry => {
                let row = table.insertRow(-1);
                row.insertCell(0).innerHTML = entry.compartment;
                row.insertCell(1).innerHTML = entry.date;
                row.insertCell(2).innerHTML = entry.time;
                row.insertCell(3).innerHTML = entry.name ? entry.name : "N/A";
            });
        }

        function sendData() {
            fetch("http://localhost:5000/sendData", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(scheduleData)
            }).then(response => response.text()).then(data => {
                alert("Data Sent: " + data);
            }).catch(error => {
                alert("Error sending data! Is your Python server running?");
            });
        }
    </script>
</head>
<body>
</h2> Enter Your Medication Schedule </h2>
    
    <label>Compartment (0-14):</label>
    <input type="number" id="compartment" min="0" max="14" required><br><br>

    <label>Date:</label>
    <input type="date" id="date" required><br><br>

    <label>Time:</label>
    <input type="time" id="time" required><br><br>

    <label>Medication Name (if applicable):</label>
    <input type="text" id="name"><br><br>

    <button type="button" onclick="addToTable()"> **Add to Schedule** </button>

    ## Preview Your Medication Schedule
    <table border="1" id="scheduleTable">
        <tr>
            <th>Compartment</th>
            <th>Date</th>
            <th>Time</th>
            <th>Medication</th>
        </tr>
    </table>

    <button type="button" onclick="sendData()"> **Submit Schedule** </button>
</body>
</html>
