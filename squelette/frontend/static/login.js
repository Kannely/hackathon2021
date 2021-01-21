"use strict";

window.addEventListener('load', () => {
    const login_form = document.getElementById("login_form");
    login_form.addEventListener("submit", (event) => {
        event.preventDefault();
        event.stopPropagation();
        const form_data = new FormData(login_form);
        fetch(`${SSO_PREFIX}login`, {
            method: "POST",
            body: form_data
        }).then((response) => {
            if (response.status == 200) window.location.replace("/front/synthesis");
            else window.location.reload();
        }).catch((e) => window.location.reload());
    });
});
