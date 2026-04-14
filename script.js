async function loadQuotes() {
  const res = await fetch("data/quotes.json");
  const quotes = await res.json();

  const feed = document.getElementById("feed");

  quotes.forEach(q => {
    const div = document.createElement("div");
    div.className = "post";

    div.innerHTML = `
      <img src="images/ObserynX_${q.id}.jpg" alt="quote">
    `;

    feed.appendChild(div);
  });
}

loadQuotes();
