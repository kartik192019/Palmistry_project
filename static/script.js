// Mouse sparkle
document.addEventListener("mousemove", (e) => {
    const sparkle = document.querySelector(".sparkle-cursor");
    sparkle.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
  });
  
  // Randomize floating symbols
  document.querySelectorAll('.symbol').forEach((symbol) => {
    const randX = Math.random() * 100;
    const randY = Math.random() * 100;
    const delay = Math.random() * 10;
    const duration = 10 + Math.random() * 10;
    symbol.style.top = `${randY}%`;
    symbol.style.left = `${randX}%`;
    symbol.style.animationDelay = `${delay}s`;
    symbol.style.animationDuration = `${duration}s`;
  });
  
  // Parallax scrolling
  window.addEventListener('scroll', function () {
    const parallax = document.querySelector('.parallax');
    const speed = parseFloat(parallax.dataset.parallaxSpeed);
    parallax.style.backgroundPositionY = -(window.scrollY * speed) + 'px';
  });
  
  // Hide preloader when loaded
  window.onload = () => {
    document.getElementById('preloader').style.display = 'none';
  };
  
  // Scanning animation on upload
  function startScan() {
    document.getElementById('scanning-indicator').classList.remove('hidden');
    return true;
  }