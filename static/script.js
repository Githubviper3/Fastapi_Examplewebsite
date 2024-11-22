async function openRandomLink() {
    try {
        const response = await fetch('http://127.0.0.1:8000/random-link'); // FastAPI endpoint
        const data = await response.json();
        const randomLink = data.link;
        window.open(randomLink, '_blank');
    } catch (error) {
        console.error("Error fetching the link:", error);
    }
}
