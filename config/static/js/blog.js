
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initBlogFeed();
  });

  function initBlogFeed() {
    var feed = document.getElementById("blog-feed");
    if (!feed) return;

    var loadMoreBtn = document.getElementById("load-more-trigger");
    var loadMoreWrapper = loadMoreBtn
      ? loadMoreBtn.closest(".blog-protocol-container")
      : null;
    var searchInput = document.getElementById("blogSearchInput");
    var filterPills = document.querySelectorAll(".bl-filter-pill");
    var featuredSection = document.getElementById("blogFeaturedSection");

    var baseUrl = feed.getAttribute("data-endpoint") || window.location.pathname;

    var state = {
      q: searchInput ? searchInput.value.trim() : "",
      category: "",
      tag: "",
    };
    var searchTimer = null;

    function buildUrl(page) {
      var params = new URLSearchParams();
      if (state.q) params.set("q", state.q);
      if (state.category) params.set("category", state.category);
      if (state.tag) params.set("tag", state.tag);
      params.set("page", page);
      return baseUrl + "?" + params.toString();
    }

    function isFiltered() {
      return Boolean(state.q || state.category || state.tag);
    }

    function toggleFeaturedVisibility() {
      if (!featuredSection) return;
      featuredSection.classList.toggle("d-none", isFiltered());
    }

    function setLoadMoreState(hasNext, nextPage) {
      if (!loadMoreBtn || !loadMoreWrapper) return;
      if (hasNext) {
        loadMoreWrapper.style.display = "";
        loadMoreBtn.setAttribute("data-next-page", nextPage);
      } else {
        loadMoreWrapper.style.display = "none";
      }
    }

    function fetchPosts(page, append) {
      feed.classList.add("is-loading");
      if (loadMoreBtn) {
        loadMoreBtn.classList.add("loading");
        loadMoreBtn.disabled = true;
      }

      fetch(buildUrl(page), {
        headers: { "X-Requested-With": "XMLHttpRequest" },
        credentials: "same-origin",
      })
        .then(function (response) {
          if (!response.ok) {
            throw new Error("Request failed with status " + response.status);
          }
          return response.json();
        })
        .then(function (data) {
          if (append) {
            feed.insertAdjacentHTML("beforeend", data.html);
          } else {
            feed.innerHTML = data.html;
          }
          setLoadMoreState(data.has_next, data.next_page);
          toggleFeaturedVisibility();
        })
        .catch(function (err) {
          console.error("خطا در بارگذاری پست‌های بلاگ:", err);
        })
        .finally(function () {
          feed.classList.remove("is-loading");
          if (loadMoreBtn) {
            loadMoreBtn.classList.remove("loading");
            loadMoreBtn.disabled = false;
          }
        });
    }

    /* ---------- Load More ---------- */
    if (loadMoreBtn) {
      loadMoreBtn.addEventListener("click", function () {
        var nextPage = parseInt(loadMoreBtn.getAttribute("data-next-page"), 10) || 2;
        fetchPosts(nextPage, true);
      });
    }

    /* ---------- Search (debounced) ---------- */
    if (searchInput) {
      searchInput.addEventListener("input", function () {
        clearTimeout(searchTimer);
        var value = searchInput.value.trim();
        searchTimer = setTimeout(function () {
          state.q = value;
          fetchPosts(1, false);
        }, 400);
      });
    }

    /* ---------- Category / Tag Filter Pills (مستقل و قابل ترکیب) ---------- */
    filterPills.forEach(function (pill) {
      pill.addEventListener("click", function () {
        var type = pill.getAttribute("data-filter-type"); // "category" | "tag"
        var value = pill.getAttribute("data-value") || "";


        document
          .querySelectorAll('.bl-filter-pill[data-filter-type="' + type + '"]')
          .forEach(function (p) {
            p.classList.remove("active");
          });
        pill.classList.add("active");

        if (type === "category") {
          state.category = value;
        } else if (type === "tag") {
          state.tag = value;
        }

        fetchPosts(1, false);
      });
    });
  }
})();