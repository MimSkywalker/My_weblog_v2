/*-----------------------------------------------------------------------------------
    Blog Detail Page — page-specific behaviour
    Loaded only on the blog detail page via {% block extra_js %}.
    Theme toggle, WOW.js and the floating nav dock are already handled globally
    by main.js / header.html / navigation.html, so this file only covers the
    behaviour unique to the article view.
-----------------------------------------------------------------------------------*/
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    /* ---------------------------------------------------------------------
       Reading progress bar
    --------------------------------------------------------------------- */
    var progressFill = document.getElementById("bdProgressFill");
    var article = document.querySelector(".bd-article");

    function updateProgress() {
      if (!progressFill || !article) return;

      var rect = article.getBoundingClientRect();
      var total = rect.height - window.innerHeight;
      var scrolled = Math.min(Math.max(-rect.top, 0), total);
      var pct = total > 0 ? (scrolled / total) * 100 : 0;

      progressFill.style.width = pct + "%";
    }

    if (progressFill && article) {
      document.addEventListener("scroll", updateProgress, { passive: true });
      window.addEventListener("resize", updateProgress);
      updateProgress();
    }

    /* ---------------------------------------------------------------------
       Table of contents — built from the article's own h2 elements,
       so there is a single source of truth (no duplicate list to maintain)
    --------------------------------------------------------------------- */
    var tocNav = document.getElementById("bdToc");
    var headings = Array.prototype.slice.call(
      document.querySelectorAll(".bd-article h2")
    );

    function buildToc() {
      if (!tocNav || !headings.length) return;

      tocNav.innerHTML = "";

      headings.forEach(function (h2, index) {
        // Assign an id automatically if the heading doesn't already have one
        if (!h2.id) {
          h2.id = "s" + (index + 1);
        }

        // Read the visible heading text, excluding the small "۰۱" number span
        var numSpan = h2.querySelector(".bd-h-num");
        var text = numSpan
          ? h2.textContent.replace(numSpan.textContent, "").trim()
          : h2.textContent.trim();

        var link = document.createElement("a");
        link.href = "#" + h2.id;
        link.setAttribute("data-target", h2.id);
        link.textContent = text;
        tocNav.appendChild(link);
      });
    }

    buildToc();

    var tocLinks = Array.prototype.slice.call(
      document.querySelectorAll("#bdToc a")
    );

    if ("IntersectionObserver" in window && headings.length && tocLinks.length) {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            var link = document.querySelector(
              '#bdToc a[data-target="' + entry.target.id + '"]'
            );
            if (!link) return;

            if (entry.isIntersecting) {
              tocLinks.forEach(function (l) {
                l.classList.remove("active");
              });
              link.classList.add("active");
            }
          });
        },
        { rootMargin: "-20% 0px -70% 0px" }
      );

      headings.forEach(function (h) {
        observer.observe(h);
      });
    }

    /* ---------------------------------------------------------------------
       Copy link
    --------------------------------------------------------------------- */
    var copyBtn = document.getElementById("bdCopyLinkBtn");
    var toast = document.getElementById("bdToast");
    var toastTimer;

    if (copyBtn && toast) {
      copyBtn.addEventListener("click", function () {
        var url = window.location.href;

        var showToast = function () {
          toast.classList.add("show");
          clearTimeout(toastTimer);
          toastTimer = setTimeout(function () {
            toast.classList.remove("show");
          }, 2200);
        };

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(showToast).catch(showToast);
        } else {
          showToast();
        }
      });
    }
  });
})();
