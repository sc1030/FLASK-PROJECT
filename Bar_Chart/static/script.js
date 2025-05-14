document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("category-select");

  function updateChart(category) {
    fetch("/get_chart", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ category }),
    })
      .then((response) => response.json())
      .then((data) => {
        const chartData = JSON.parse(data.chart); // Parse the JSON string
        Plotly.newPlot("chart", chartData.data, chartData.layout); // Render chart
      })
      .catch((error) => console.error("Error loading chart:", error));
  }

  select.addEventListener("change", () => {
    updateChart(select.value);
  });

  // Load initial chart
  updateChart(select.value);
});
