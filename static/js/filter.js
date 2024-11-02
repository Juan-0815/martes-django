document.addEventListener('DOMContentLoaded', function () {
  const allFilters = document.getElementById('filters');
  const buttons = allFilters.querySelectorAll('button');

  buttons.forEach(button => {
    button.addEventListener('click', function () {
      buttons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');

      const activeFilter = this.dataset.filter;
      const cards = document.querySelectorAll('.card');

      cards.forEach(card => {
        const data = card.querySelector('[data-category]');
        if (data) {
          const category = data.dataset.category;
          //console.log("Active Filter: ", activeFilter);
          //console.log("Product Category: ", category);
          if (activeFilter === 'All') {
            card.classList.remove('d-none');
          } else if (category === activeFilter) {
            card.classList.remove('d-none');
          } else {
            card.classList.add('d-none');
          }
        }
      });
    });
  });
});
