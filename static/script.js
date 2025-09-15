async function updateStatus(plate) {
    const res = await fetch(`/status/${plate}`);
    const data = await res.json();

    document.getElementById("status").innerText = data.active ? "Parked" : "Not Parked";
    document.getElementById("elapsed").innerText = data.active ? data.elapsed + " min" : "-";
    document.getElementById("bill").innerText = data.bill;
}

async function leaveNow(plate) {
    await fetch(`/leave/${plate}`, { method: "POST" });
    // alert("Leave request sent. Please wait 2 minutes...");
}
