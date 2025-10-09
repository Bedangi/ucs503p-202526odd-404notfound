async function updateStatus(email) {
    const res = await fetch(`/status/${email}`);
    const data = await res.json();

    document.getElementById("status").innerText = data.active ? "Parked" : "Not Parked";
    document.getElementById("elapsed").innerText = data.active ? data.elapsed + " min" : "-";
    document.getElementById("bill").innerText = data.bill;
}

async function leaveNow(email) {
    await fetch(`/leave/${email}`, { method: "POST" });
    // alert("Leave request sent. Please wait 2 minutes...");
}

async function deletePlate(plate) {
    const confirmDelete = confirm(`Delete plate "${plate}"?`);
    if (!confirmDelete) return;

    const res = await fetch("/delete_plate", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ email: "{{ user.email }}", plate })
    });

    location.reload();
}

async function editPlate(oldPlate) {
    const newPlate = prompt("Enter new plate number:", oldPlate);
    if (!newPlate || newPlate === oldPlate) return;

    const res = await fetch("/edit_plate", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
            email: "{{ user.email }}",
            old_plate: oldPlate,
            new_plate: newPlate
        })
    });

    location.reload();
}
