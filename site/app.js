(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduceMotion && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      }
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('visible'));
  }

  document.querySelectorAll('[data-copy-hash]').forEach((button) => {
    button.addEventListener('click', async () => {
      const hash = button.getAttribute('data-copy-hash');
      const original = button.textContent;
      try {
        await navigator.clipboard.writeText(hash);
        button.textContent = button.dataset.copied || 'Copied';
      } catch {
        button.textContent = hash;
      }
      setTimeout(() => { button.textContent = original; }, 1800);
    });
  });
})();
