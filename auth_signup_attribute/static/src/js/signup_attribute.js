odoo.define("auth_signup_attribute.signup_attribute", function () {
    "use strict";

    $(function () {
        var $form = $("form.oe_signup_form");
        var $companyType = $form.find("input[name='company_type']");
        if (!$companyType.length) {
            return;
        }
        var $birthdayGroup = $form.find(".field-birthday");
        var $birthday = $birthdayGroup.find("input[name='birthday']");
        var $name = $form.find("input[name='name']");
        var $personLabel = $form.find(".o_signup_person_label");
        var $companyLabel = $form.find(".o_signup_company_label");
        var namePlaceholder = $name.attr("placeholder") || "";

        // Offering a future date makes no sense for a date of birth. The bound
        // is the local date, which the ISO string alone would not give.
        var today = new Date();
        today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
        $birthday.attr("max", today.toISOString().slice(0, 10));

        function applyCompanyType() {
            var isCompany = $companyType.filter(":checked").val() === "company";
            // A company has no date of birth. Disabling the field keeps it
            // out of the submission altogether, which also drops it from the
            // browser validation and preserves what was typed if the visitor
            // switches back.
            $birthdayGroup.toggleClass("d-none", isCompany);
            $birthday.prop("disabled", isCompany);
            // The single name field holds the company name for a company.
            $personLabel.toggleClass("d-none", isCompany);
            $companyLabel.toggleClass("d-none", !isCompany);
            $name.attr("placeholder", isCompany ? "" : namePlaceholder);
        }

        $companyType.on("change", applyCompanyType);
        applyCompanyType();
    });
});
