---
layout: default
title: Files
permalink: /files/
---

{% assign REPO = "https://github.com/devtalent2030/procurement-audit-automation" %}
{% assign BRANCH = "main" %}

<div class="files404">
  <div class="files404__inner">
    <div class="files404__badge">Files are hosted on GitHub</div>

    <a class="ghbtn" href="{{ REPO }}/tree/{{ BRANCH }}" target="_blank" rel="noopener">
      <span class="ghbtn__icon" aria-hidden="true">
        <!-- simple github mark -->
        <svg viewBox="0 0 16 16" width="18" height="18" fill="currentColor">
          <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8Z"></path>
        </svg>
      </span>

      <span class="ghbtn__text">
        <span class="ghbtn__title">Open Files on GitHub</span>
        <span class="ghbtn__sub">{{ REPO }}</span>
      </span>

      <span class="ghbtn__arrow" aria-hidden="true">↗</span>
    </a>

    <div class="downArrow" aria-hidden="true">
      <span class="downArrow__shaft"></span>
      <span class="downArrow__head"></span>
      <span class="downArrow__glow"></span>
    </div>

    <div class="files404__hint">
      Click the button to browse <code>/data</code>, <code>/src</code>, <code>/docs</code> and evidence outputs.
    </div>
  </div>
</div>
