/*!
 * Project Detail Page — Scoped JS
 * فقط عناصر با data-pd-* رو کنترل می‌کنه؛ هیچ کاری با main.js انجام نمی‌ده
 * و هیچ متغیر/کلاس گلوبالی رو تغییر نمی‌ده.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initGallery();
    initShare();
  });

  /* ============================================================
     Gallery Slider
     ============================================================ */
  function initGallery() {
    const gallery = document.querySelector("[data-pd-gallery]");
    if (!gallery) return;

    const slides = Array.prototype.slice.call(
      gallery.querySelectorAll("[data-pd-slide]")
    );
    const thumbs = Array.prototype.slice.call(
      document.querySelectorAll("[data-pd-thumb]")
    );
    const prevBtn = gallery.querySelector("[data-pd-prev]");
    const nextBtn = gallery.querySelector("[data-pd-next]");
    const counter = gallery.querySelector("[data-pd-current]");

    if (!slides.length) return;

    let currentIndex = slides.findIndex(function (slide) {
      return slide.classList.contains("is-active");
    });
    if (currentIndex < 0) currentIndex = 0;

    function goTo(index) {
      const total = slides.length;
      const nextIndex = ((index % total) + total) % total; // safe wrap

      slides.forEach(function (slide, i) {
        slide.classList.toggle("is-active", i === nextIndex);
      });
      thumbs.forEach(function (thumb, i) {
        thumb.classList.toggle("is-active", i === nextIndex);
      });
      if (counter) counter.textContent = nextIndex + 1;

      currentIndex = nextIndex;
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        goTo(currentIndex - 1);
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        goTo(currentIndex + 1);
      });
    }

    thumbs.forEach(function (thumb) {
      thumb.addEventListener("click", function () {
        const index = parseInt(thumb.getAttribute("data-index"), 10);
        if (!isNaN(index)) goTo(index);
      });
    });

    // Keyboard navigation when the gallery (or its children) has focus/hover
    gallery.setAttribute("tabindex", "0");
    gallery.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") goTo(currentIndex + 1); // RTL: left = next
      if (e.key === "ArrowRight") goTo(currentIndex - 1); // RTL: right = prev
    });

    // Basic touch swipe support
    let touchStartX = 0;
    const viewport = gallery.querySelector(".pd-gallery-viewport");
    if (viewport) {
      viewport.addEventListener(
        "touchstart",
        function (e) {
          touchStartX = e.changedTouches[0].screenX;
        },
        { passive: true }
      );

      viewport.addEventListener(
        "touchend",
        function (e) {
          const touchEndX = e.changedTouches[0].screenX;
          const delta = touchEndX - touchStartX;
          const threshold = 40;

          if (Math.abs(delta) < threshold) return;

          // RTL: swipe right (delta > 0) => previous, swipe left => next
          if (delta > 0) {
            goTo(currentIndex - 1);
          } else {
            goTo(currentIndex + 1);
          }
        },
        { passive: true }
      );
    }
  }

  /* ============================================================
     Share Button
     ============================================================ */
  function initShare() {
    const shareBtn = document.querySelector("[data-pd-share]");
    if (!shareBtn) return;

    shareBtn.addEventListener("click", function () {
      const shareData = {
        title: document.title,
        url: window.location.href,
      };

      if (navigator.share) {
        navigator.share(shareData).catch(function () {
          /* کاربر share رو کنسل کرده؛ نیازی به هندل خاصی نیست */
        });
        return;
      }

      copyToClipboard(window.location.href);
    });
  }

  function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard
        .writeText(text)
        .then(function () {
          showToast("لینک پروژه کپی شد");
        })
        .catch(function () {
          showToast("کپی لینک با خطا مواجه شد");
        });
    } else {
      // Fallback برای مرورگرهای قدیمی‌تر
      const tempInput = document.createElement("input");
      tempInput.value = text;
      document.body.appendChild(tempInput);
      tempInput.select();
      try {
        document.execCommand("copy");
        showToast("لینک پروژه کپی شد");
      } catch (err) {
        showToast("کپی لینک با خطا مواجه شد");
      }
      document.body.removeChild(tempInput);
    }
  }

  function showToast(message) {
    let toast = document.querySelector(".pd-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "pd-toast";
      document.body.appendChild(toast);
    }

    toast.textContent = message;
    toast.classList.add("is-show");

    clearTimeout(showToast._timer);
    showToast._timer = setTimeout(function () {
      toast.classList.remove("is-show");
    }, 2200);
  }
})();