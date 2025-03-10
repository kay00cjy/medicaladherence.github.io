<!DOCTYPE html>
<html>
<head>
    <title>Medication Schedule Input</title>
</head>
<body>
    <h2>Enter Medication Schedule</h2>
    <form id="medForm">
        Current Time (HH:MM:SS): <input type="time" id="currentTime" required><br><br>
        Date: <input type="date" id="date" required><br><br>
        Time: <input type="time" id="time" required><br><br>
        Medication Number (1-14): <input type="number" id="number" min="1" max="14" required><br><br>
        <button type="button" onclick="sendData()">Submit</button>
    </form>

    <script>
    function sendData() {
        let currentTime = document.getElementById("currentTime").value;
        let date = document.getElementById("date").value;
        let time = document.getElementById("time").value;
        let number = document.getElementById("number").value;

        let scheduleData = `${currentTime},${date},${time},${number}`;

        fetch("http://localhost:5000/sendData", {
            method: "POST",
            headers: {"Content-Type": "text/plain"},
            body: scheduleData
        }).then(response => response.text()).then(data => {
            alert("Data Sent: " + data);
        });
    }
    </script>
</body>
</html>

