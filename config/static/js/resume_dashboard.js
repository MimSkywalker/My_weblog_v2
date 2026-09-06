document.addEventListener("DOMContentLoaded", () => {

    /*
    ============================================================
    Helpers
    ============================================================
    */

    // Parse a date value coming from Django ("YYYY-MM-DD" is the
    // only format the templates actually render, but we fall back
    // to the native Date parser defensively).
    function parseStoredDate(value) {

        if (!value) {
            return null;
        }

        if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {

            const [year, month, day] = value.split("-").map(Number);
            return new Date(year, month - 1, day);
        }

        const parsed = new Date(value);
        return isNaN(parsed.getTime()) ? null : parsed;
    }

    /*
    ============================================================
    Persian Datepicker
    ============================================================
    */

    function initializePersianDatepicker(container) {

        if (!container) {
            return;
        }

        $(container)
            .find(".jalali-date")
            .each(function () {

                const input = $(this);
                const targetName = input.data("target");

                if (!targetName) {
                    return;
                }

                /*
                 * Scope the hidden-input lookup to the same item
                 * (or the given container) instead of the whole
                 * document, so duplicate name patterns can never
                 * collide across formsets/rows.
                 */
                const scope = input.closest(".item-card").length
                    ? input.closest(".item-card")
                    : $(container);

                const hiddenInput = scope.find(`input[name="${targetName}"]`);

                if (!hiddenInput.length) {
                    return;
                }

                const storedDate = parseStoredDate(hiddenInput.val());

                /*
                 * NOTE ON `initialValue` (deliberately left false):
                 * Feeding the plugin a pre-formatted Jalali string via
                 * `initialValue: true` relies on its *internal* parser
                 * correctly guessing that the string is Persian and not
                 * Gregorian. When that guess is wrong the plugin can
                 * throw during construction — and since this all runs
                 * inside a jQuery `.each()` loop, one uncaught exception
                 * silently aborts every remaining iteration. That is
                 * exactly why some date fields would randomly fail to
                 * open at all, and why some pre-filled rows rendered
                 * with an empty date: the field simply never finished
                 * initializing.
                 *
                 * The reliable, documented way to load an initial date
                 * is the plugin's own `setDate(unixMilliseconds)` API
                 * call, done *after* construction — see below.
                 */
                const datepicker = input.persianDatepicker({

                    format: "YYYY/MM/DD",

                    autoClose: true,

                    initialValue: false,

                    observer: true,

                    onSelect: function (unixDate) {

                        const selectedDate = new persianDate(unixDate);

                        /*
                         * `.toLocale("en")` makes persian-date emit
                         * Latin digits directly, so there is no need
                         * for a manual Persian-to-English digit map.
                         */
                        const gregorianDate = selectedDate
                            .toCalendar("gregorian")
                            .toLocale("en")
                            .format("YYYY-MM-DD");

                        hiddenInput
                            .val(gregorianDate)
                            .trigger("change");
                    }

                });

                /*
                 * Now that construction succeeded, load the existing
                 * value (if any) through the plugin's public API.
                 * `.persianDatepicker()` returns the datepicker instance
                 * itself, and `setDate()` accepts a unix timestamp in
                 * milliseconds — exactly what `Date#getTime()` gives us.
                 *
                 * try/catch here is deliberate: if a single stored value
                 * is somehow malformed, only THIS field is affected —
                 * every other field on the page keeps working.
                 */
                if (storedDate && datepicker && typeof datepicker.setDate === "function") {

                    try {
                        datepicker.setDate(storedDate.getTime());
                    } catch (err) {
                        console.error(`Could not set initial date for "${targetName}":`, err);
                    }
                }

            });
    }


    /*
    ============================================================
    Start / End date range validation
    (end date must not be before start date)
    ============================================================
    */

    function setupDateRangeValidation(container) {

        if (!container) {
            return;
        }

        // Delegated listener: works for rows added later by "+ Add ..." too.
        $(container).on(
            "change",
            'input[name$="-start_date"], input[name$="-end_date"]',
            function () {

                const item = $(this).closest(".item-card");

                if (!item.length) {
                    return;
                }

                const startInput = item.find('input[name$="-start_date"]');
                const endInput = item.find('input[name$="-end_date"]');

                const start = startInput.val();
                const end = endInput.val();

                let errorEl = item.find(".date-range-error");

                if (start && end && end < start) {

                    if (!errorEl.length) {
                        errorEl = $('<small class="error date-range-error"></small>');
                        endInput.closest(".form-group").append(errorEl);
                    }

                    errorEl.text("تاریخ پایان نمی‌تواند قبل از تاریخ شروع باشد.");

                } else {
                    errorEl.remove();
                }
            }
        );
    }


    /*
    ============================================================
    Formset Setup
    ============================================================
    */

    function setupFormset({
        containerId,
        templateId,
        addButtonId,
        prefix,
        itemClass
    }) {

        const container = document.getElementById(containerId);
        const template = document.getElementById(templateId);
        const addButton = document.getElementById(addButtonId);
        const totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`);

        if (!container || !template || !addButton || !totalForms) {
            return;
        }

        /*
        --------------------------------------------------------
        Add new form
        --------------------------------------------------------
        */

        addButton.addEventListener("click", () => {

            const index = parseInt(totalForms.value, 10);

            const html = template.innerHTML.replaceAll("__prefix__", index);

            container.insertAdjacentHTML("beforeend", html);

            const newItem = container.lastElementChild;

            initializePersianDatepicker(newItem);

            totalForms.value = index + 1;

            updateNumbers();
        });

        /*
        --------------------------------------------------------
        Delete form
        --------------------------------------------------------
        */

        container.addEventListener("change", (event) => {

            if (event.target.matches('input[name$="-DELETE"]')) {

                const item = event.target.closest(`.${itemClass}`);

                if (!item) {
                    return;
                }

                item.classList.toggle("deleted", event.target.checked);
            }
        });

        /*
        --------------------------------------------------------
        Update numbers
        --------------------------------------------------------
        */

        function updateNumbers() {

            const items = container.querySelectorAll(`.${itemClass}`);

            items.forEach((item, index) => {

                const number = item.querySelector(".item-number");

                if (number) {
                    number.textContent = index + 1;
                }
            });
        }

        updateNumbers();

        return container;
    }


    /*
    ============================================================
    Experience Formset
    ============================================================
    */

    const experienceContainer = setupFormset({
        containerId: "experience-container",
        templateId: "experience-template",
        addButtonId: "add-experience",
        prefix: "exp",
        itemClass: "experience-item"
    });


    /*
    ============================================================
    Skill Formset
    ============================================================
    */

    setupFormset({
        containerId: "skill-container",
        templateId: "skill-template",
        addButtonId: "add-skill",
        prefix: "skill",
        itemClass: "skill-item"
    });


    /*
    ============================================================
    Education Formset
    ============================================================
    */

    const educationContainer = setupFormset({
        containerId: "education-container",
        templateId: "education-template",
        addButtonId: "add-education",
        prefix: "edu",
        itemClass: "education-item"
    });


    /*
    ============================================================
    Expertise Formset
    ============================================================
    */

    setupFormset({
        containerId: "expertise-container",
        templateId: "expertise-template",
        addButtonId: "add-expertise",
        prefix: "exprt",
        itemClass: "expertise-item"
    });


    /*
    ============================================================
    Degree Select
    ============================================================
    */

    document
        .querySelectorAll(".degree-select")
        .forEach(select => {

            const currentValue = select.dataset.value;

            if (currentValue) {
                select.value = currentValue;
            }
        });


    /*
    ============================================================
    Initialize Datepickers + Range Validation for Existing Forms
    ============================================================
    */

    initializePersianDatepicker(experienceContainer);
    initializePersianDatepicker(educationContainer);

    setupDateRangeValidation(experienceContainer);
    setupDateRangeValidation(educationContainer);


    /*
    ============================================================
    Block submit while an invalid date range is present
    ============================================================
    */

    const resumeForm = document.getElementById("resume-form");

    if (resumeForm) {

        resumeForm.addEventListener("submit", (event) => {

            if (resumeForm.querySelector(".date-range-error")) {

                event.preventDefault();
                alert("لطفاً بازه‌های تاریخ نامعتبر را قبل از ذخیره اصلاح کنید.");
            }
        });
    }

});
