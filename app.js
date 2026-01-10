// script.js

document.addEventListener("DOMContentLoaded", () => {
  const loader = document.querySelector(".loader");
  const app = document.querySelector(".app");

  // Simulate loading (API, assets, etc.)
  setTimeout(() => {
    // Hide loader
    loader.style.opacity = "0";
    loader.style.pointerEvents = "none";

    // Show main app
    app.style.opacity = "1";

    // Remove loader from DOM (clean UX)
    setTimeout(() => {
      loader.remove();
    }, 1000);
  }, 3000); // 3 seconds loading
});
