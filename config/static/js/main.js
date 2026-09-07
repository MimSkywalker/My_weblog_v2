(function ($) {
  "use strict";

  $(window).on("load", function () {
    // Hide Preloader
    $("#preloader").fadeOut(500);

    // Isotope Grid Initialization
    const grid = $(".isotope-grid");
    if (grid.length > 0) {
      const iso = grid.isotope({
        itemSelector: ".isotope-item",
        layoutMode: "fitRows",
        isOriginLeft: false,
        percentPosition: true
      });

      // Filtering logic
      $(".filter-btn").on("click", function () {
        const filterValue = $(this).attr("data-filter");
        iso.isotope({ filter: filterValue });

        $(".filter-btn").removeClass("active");
        $(this).addClass("active");
      });
    }
  });

  $(document).ready(function () {
    // WOW.js Initialization
    if (typeof WOW !== 'undefined') {
      new WOW({
        animateClass: "animate__animated",
        offset: 100,
        mobile: true,
        live: true,
      }).init();
    }

    // Theme Management
    const darkToggle = $(".dark-toggle");
    const body = $("body");
    const html = document.documentElement;

    // Check saved theme or system preference
    if (html.classList.contains("dark-theme")) {
      body.addClass("dark-theme");
      updateToggleIcons("dark");
    }

    darkToggle.on("click", function () {
      const isDark = !html.classList.contains("dark-theme");
      html.classList.toggle("dark-theme", isDark);
      body.toggleClass("dark-theme", isDark);
      localStorage.setItem("theme", isDark ? "dark" : "light");
      updateToggleIcons(isDark ? "dark" : "light");
    });

    function updateToggleIcons(theme) {
      if (theme === "dark") {
        darkToggle.find("i").removeClass("fa-moon").addClass("fa-sun");
      } else {
        darkToggle.find("i").removeClass("fa-sun").addClass("fa-moon");
      }
    }

    // Mobile Navigation Toggle
    $(".menu-toggle").on("click", function () {
      $(".mobile-menu-inner").toggleClass("active");
    });

    /*
    ============================================================
    Contact Form Handler
    (Real submission via fetch to the Django backend, not a
    fake setTimeout simulation)
    ============================================================
    */

const contactForm = $("#contact-form");

if (contactForm.length > 0) {

  const formEl = contactForm[0];
  const submitBtn = contactForm.find('button[type="submit"]');
  const originalBtnHtml = submitBtn.html();

  function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");

      for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(
            cookie.substring(name.length + 1)
          );
          break;
        }
      }
    }

    return cookieValue;
  }

  function setButtonState(html, addClass, removeClass, disabled) {
    submitBtn
      .html(html)
      .prop("disabled", disabled)
      .removeClass(removeClass)
      .addClass(addClass);
  }

  contactForm.on("submit", function (e) {

    e.preventDefault();

    const formData = new FormData(formEl);

    const csrfToken =
      formData.get("csrfmiddlewaretoken") || getCookie("csrftoken");

    const actionUrl =
      formEl.getAttribute("action") || window.location.href;

    setButtonState(
      'لطفا صبر کنید... <i class="fa-solid fa-spinner fa-spin ms-2"></i>',
      "",
      "",
      true
    );

    fetch(actionUrl, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest"
      },
      credentials: "same-origin"
    })
      .then((response) => {

        console.log("پاسخ از Django رسید:", response);

        if (!response.ok) {
          throw new Error(
            "Request failed with status " + response.status
          );
        }

        return response.json().catch(() => ({}));
      })

      .then(() => {

        setButtonState(
          'پیام ارسال شد <i class="fa-solid fa-check ms-2"></i>',
          "btn-success",
          "btn-primary",
          true
        );

        formEl.reset();

        setTimeout(function () {
          setButtonState(
            originalBtnHtml,
            "btn-primary",
            "btn-success",
            false
          );
        }, 3000);
      })

      .catch((error) => {

        console.error(
          "Contact form submission failed:",
          error
        );

        setButtonState(
          'خطا در ارسال پیام، دوباره تلاش کنید <i class="fa-solid fa-triangle-exclamation ms-2"></i>',
          "btn-danger",
          "btn-primary",
          false
        );

        setTimeout(function () {
          setButtonState(
            originalBtnHtml,
            "btn-primary",
            "btn-danger",
            false
          );
        }, 3000);
      });
  });
}

    // Blog Dynamic Content Loading
    const loadMoreBtn = $("#load-more-trigger");
    const blogPool = $(".blog-load-more-pool");
    const blogFeed = $("#blog-feed");

    if (loadMoreBtn.length > 0 && blogPool.length > 0) {
      loadMoreBtn.on("click", function (e) {
        e.preventDefault();
        console.log("SUBMIT EVENT");

        const btn = $(this);
        const btnText = btn.find("span");

        // Update button state
        btn.addClass("loading").prop("disabled", true);
        btnText.text("بارگزاری...");

        // Mock processing delay
        setTimeout(function() {
          const items = blogPool.children().detach();

          if (items.length > 0) {
            items.each(function(index) {
              const item = $(this);
              item.removeClass("d-none");

              // Animated reveal sequence
              setTimeout(function() {
                item.addClass("animate__animated animate__fadeInUp");
                blogFeed.append(item);
              }, index * 150);
            });

            // Remove trigger after exhaust
            btn.fadeOut(400, function() {
              $(this).remove();
            });

          } else {
            btnText.text("تمام مقالات بارگزاری شدند");
            btn.removeClass("loading");
          }
        }, 1500);
      });
    }
  });

})(jQuery);