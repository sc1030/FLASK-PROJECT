$(document).ready(function () {
  $("#search-box").on("keyup", function () {
    let query = $(this).val();
    let resultsContainer = $("#results");
    resultsContainer.empty();

    if (query.length > 0) {
      $.post("/search", { query: query }, function (data) {
        if (data.length > 0) {
          data.forEach((item) => {
            let regex = new RegExp("(" + query + ")", "gi");
            let highlighted = item.replace(
              regex,
              '<mark class="bg-yellow-300 dark:bg-yellow-600 px-1 rounded">$1</mark>'
            );
            resultsContainer.append(
              `<li class="p-3 rounded-lg bg-gray-100 dark:bg-gray-700">${highlighted}</li>`
            );
          });
        } else {
          resultsContainer.append(
            `<li class="p-3 bg-red-100 text-red-700 rounded-lg">No results found</li>`
          );
        }
      });
    }
  });
});
