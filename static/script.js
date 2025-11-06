async function updateStatus(userEmail) {
    const res = await fetch(`/status/${userEmail}`);
    const data = await res.json();

    document.getElementById("plate").innerText = data.active ? data.active_plate : "-";
    document.getElementById("status").innerText = data.active ? "Parked" : "Not Parked";
    document.getElementById("elapsed").innerText = data.active ? data.elapsed + " min" : "-";
    document.getElementById("bill").innerText = data.bill;
}

let redirected = false;
async function checkParkingStatus(userEmail) {
    try {
    const res = await fetch(`/status/${userEmail}`);
    const data = await res.json();

    if (!data.active && data.amount_due > 0 && !redirected) {
        redirected = true; // prevent double redirects
        window.location.href = `/bill/${userEmail}`;
    }
    } catch (err) {
    console.error("Error checking status:", err);
    }
}
// async function leaveNow(email) {
//     try {
//         const response = await fetch(`/leave/${email}`, { method: "POST" });

//         let data;
//         const contentType = response.headers.get("content-type");
//         if (contentType && contentType.includes("application/json")) {
//             data = await response.json();
//         } else {
//             data = await response.text(); // fallback
//             throw new Error(data);
//         }

//         // If success, redirect
//         window.location.href = `/bill/${email}`;
//     } catch (error) {
//         console.error("Error leaving:", error);
//         alert(error.message || "Failed to process leave request.");
//     }
// }

async function deletePlate(plate) {
    const email = currUserEmail;
    const confirmDelete = confirm(`Delete plate "${plate}"?`);
    if (!confirmDelete) return;

    const formData = new FormData();
    formData.append("email", email);
    formData.append("plate", plate);

    const res = await fetch("/delete_plate", {
        method: "POST",
        body: formData
    });

    location.reload();
}

async function editPlate(oldPlate) {
    const email = currUserEmail;
    const newPlate = prompt("Enter new plate number:", oldPlate);
    if (!newPlate || newPlate === oldPlate) return;

    const formData = new FormData();
    formData.append("email", email);
    formData.append("old_plate", oldPlate);
    formData.append("new_plate", newPlate);

    const res = await fetch("/edit_plate", {
        method: "POST",
        body: formData
    });

    location.reload();
}

async function addPlate() {
    const plateInput = document.getElementById("plateNumber");
    const plateNumber = plateInput.value.trim();
    if (!plateNumber) {
        alert("Please enter a plate number.");
        return;
    }

    const formData = new FormData();
    formData.append("email", currUserEmail);
    formData.append("plateNumber", plateNumber);

    const res = await fetch(`/plates/${currUserEmail}`, {
        method: "POST",
        body: formData
    });

    if (res.ok) {
        location.reload();
        plateInput.value = "";
    } else {
        alert("Failed to add plate.");
    }
}
