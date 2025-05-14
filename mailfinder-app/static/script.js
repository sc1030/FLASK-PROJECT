document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("full_name");
  const suggestionsList = document.getElementById("suggestions");

  input.addEventListener("input", async () => {
    const query = input.value.trim();
    suggestionsList.innerHTML = "";

    if (query.length > 1) {
      const res = await fetch(`/autocomplete?q=${query}`);
      const suggestions = await res.json();

      suggestions.forEach((name) => {
        const li = document.createElement("li");
        li.textContent = name;
        li.onclick = () => {
          input.value = name;
          suggestionsList.innerHTML = "";
        };
        suggestionsList.appendChild(li);
      });
    }
  });
});
