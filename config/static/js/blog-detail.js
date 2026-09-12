/*!
 * Blog Detail Page — Scoped JS
 * فقط با عناصر bd-* و data-bd-* کار می‌کند؛ هیچ متغیر/کلاس گلوبالی
 * را تغییر نمی‌دهد و به main.js/project-detail.js وابسته نیست.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initTocAndProgress();
    initShare();
    initReplyToggle();
  });

  /* ============================================================
     TOC (از h2های article ساخته می‌شود) + نوار پیشرفت مطالعه
     ============================================================ */
  function initTocAndProgress() {
    const article = document.getElementById("bdArticleBody");
    const tocEl = document.getElementById("bdToc");
    const progressFill = document.getElementById("bdProgressFill");
    const articleCard = article ? article.closest(".bd-article-card") : null;

    if (!article) return;

    /* ---------- ساخت TOC ---------- */
    const headings = Array.prototype.slice.call(
      article.querySelectorAll("h2")
    );

    const tocLinks = [];

    if (tocEl) {
      if (!headings.length) {
        tocEl.innerHTML = '<span class="bd-toc-empty">فهرستی موجود نیست</span>';
      } else {
        headings.forEach(function (heading, index) {
          if (!heading.id) {
            heading.id = "bd-section-" + (index + 1);
          }

          const link = document.createElement("a");
          link.href = "#" + heading.id;
          link.textContent = heading.textContent.trim();

          link.addEventListener("click", function (e) {
            e.preventDefault();
            heading.scrollIntoView({ behavior: "smooth", block: "start" });
          });

          tocEl.appendChild(link);
          tocLinks.push({ heading: heading, link: link });
        });
      }
    }

    /* ---------- هایلایت TOC هنگام اسکرول + نوار پیشرفت ---------- */
    function onScroll() {
      // نوار پیشرفت مطالعه بر اساس ارتفاع کارت مقاله
      if (progressFill && articleCard) {
        const rect = articleCard.getBoundingClientRect();
        const total = rect.height - window.innerHeight;
        const scrolled = Math.min(
          Math.max(-rect.top, 0),
          Math.max(total, 1)
        );
        const percent = total > 0 ? (scrolled / total) * 100 : 0;
        progressFill.style.width = Math.min(Math.max(percent, 0), 100) + "%";
      }

      // فعال کردن آیتم TOC مربوط به heading جاری
      if (tocLinks.length) {
        let activeIndex = 0;
        const scrollPos = window.scrollY + 140;

        tocLinks.forEach(function (item, index) {
          if (item.heading.offsetTop <= scrollPos) {
            activeIndex = index;
          }
        });

        tocLinks.forEach(function (item, index) {
          item.link.classList.toggle("is-active", index === activeIndex);
        });
      }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ============================================================
     Share Button (همان الگوی project-detail.js: Web Share API +
     fallback کپی به کلیپ‌بورد)
     ============================================================ */
  function initShare() {
    const copyBtn = document.getElementById("bdCopyLinkBtn");
    if (!copyBtn) return;

    copyBtn.addEventListener("click", function () {
      const url = window.location.href;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard
          .writeText(url)
          .then(function () {
            showToast("لینک کپی شد");
          })
          .catch(function () {
            showToast("کپی لینک با خطا مواجه شد");
          });
        return;
      }

      const tempInput = document.createElement("input");
      tempInput.value = url;
      document.body.appendChild(tempInput);
      tempInput.select();
      try {
        document.execCommand("copy");
        showToast("لینک کپی شد");
      } catch (err) {
        showToast("کپی لینک با خطا مواجه شد");
      }
      document.body.removeChild(tempInput);
    });
  }

  function showToast(message) {
    const toast = document.getElementById("bdToast");
    if (!toast) return;

    toast.textContent = message;
    toast.classList.add("is-show");

    clearTimeout(showToast._timer);
    showToast._timer = setTimeout(function () {
      toast.classList.remove("is-show");
    }, 2200);
  }

  /* ============================================================
     Reply Toggle
     هر دکمهٔ «پاسخ» فرم ریپلای مخصوص همان کامنت را باز/بسته می‌کند؛
     همزمان فقط یک فرم ریپلای باز می‌ماند.
     ============================================================ */
  function initReplyToggle() {
    const toggleButtons = document.querySelectorAll("[data-bd-reply-toggle]");
    if (!toggleButtons.length) return;

    let openWrapper = null;

    toggleButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        const commentId = btn.getAttribute("data-comment-id");
        const wrapper = document.getElementById("reply-form-" + commentId);
        if (!wrapper) return;

        const isOpen = !wrapper.classList.contains("d-none");

        if (openWrapper && openWrapper !== wrapper) {
          openWrapper.classList.add("d-none");
        }

        wrapper.classList.toggle("d-none", isOpen);
        openWrapper = isOpen ? null : wrapper;

        if (!isOpen) {
          const firstInput = wrapper.querySelector(".vx-input");
          if (firstInput) firstInput.focus();
        }
      });
    });
  }
})();
