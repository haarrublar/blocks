const socket = io('http://127.0.0.1:8000');
const actionButton = document.querySelector('.close-btn');
const modal = document.querySelector('.modal');

// Listen for the command from the API
socket.on('ui_state_change', (data) => {
    // 4. Update the visual UI based on API instructions
    if (actionButton) {
        actionButton.style.backgroundColor = data.color;
        actionButton.style.color = 'white'; // Make text readable on green
        actionButton.innerText = data.text;
    }
    
    // Ensure the modal pops up when the state changes
    modal.style.display = 'block';
    document.body.classList.add('active-overlay');
});

function handleClose() {
    modal.style.display = 'none';
    document.body.classList.remove('active-overlay');
}