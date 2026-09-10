(() => {
  const scriptUrl = document.currentScript?.src || document.baseURI;
  const assetBase = new URL('.', scriptUrl);
  const flagAssets = {
    en: 'flags/en.svg',
    pl: 'flags/pl.svg',
    uk: 'flags/uk.svg',
    de: 'flags/de.svg',
  };

  document.querySelectorAll('.lang[hreflang]').forEach((link) => {
    const language = link.getAttribute('hreflang');
    const oldFlag = link.querySelector('.flag');

    // Keep Russian intentionally text-only.
    if (language === 'ru') {
      oldFlag?.remove();
      return;
    }

    const asset = flagAssets[language];
    if (!asset) return;

    const flag = document.createElement('img');
    flag.src = new URL(asset, assetBase).href;
    flag.alt = '';
    flag.width = 18;
    flag.height = 12;
    flag.decoding = 'async';
    flag.setAttribute('aria-hidden', 'true');
    flag.style.cssText = 'width:18px;height:12px;flex:0 0 auto;object-fit:cover;border-radius:2px;box-shadow:0 0 0 1px rgba(20,20,20,.12)';

    oldFlag?.remove();
    // Append after the native language label, per the visual language selector design.
    link.append(flag);
  });

  // Keep Russian available, but place it at the far right/end of the selector.
  const languageNav = document.querySelector('.langs');
  const russianLink = languageNav?.querySelector('.lang[hreflang="ru"]');
  if (languageNav && russianLink) languageNav.append(russianLink);

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
